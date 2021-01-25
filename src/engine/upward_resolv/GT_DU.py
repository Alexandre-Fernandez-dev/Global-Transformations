from .Memory import Instance, InstanceInc, Result

class GT_DU:
    def __init__(self, pfunctor):
        self.pfunctor = pfunctor

    def __call__(self, X):
        return self.extend(X)

    def extend(self, X):
        matches = {}
        bigresult = None
        fifo = []
        depth = 0
        cpt = 0

        def add_instance(ins):
            assert ins.occ not in matches
            matches[ins.occ] = ins
            ins.auto = False
            # for s_occ, get_s_ins, _ in self.pfunctor.iter_self_inclusions(ins):
            #     # if s_occ in matches:
            #     #     s_ins = matches[s_occ]
            #     # else:
            #     assert s_occ not in matches
            #     s_ins = get_s_ins()
            #     # ins_inc = get_ins_inc(s_ins)
            #     matches[s_occ] = s_ins

        def add_result(ins):
            res = Result(ins.rhs(), True)
            # results.add(res)
            res.c = cpt
            ins.observe(res, None)
            # for s_occ, get_s_ins, get_ins_inc in self.pfunctor.iter_self_inclusions(ins):
            #     if s_occ in matches:
            #         s_ins = matches[s_occ]
            #     else:
            #         s_ins = get_s_ins()
            #     ins_inc = get_ins_inc(s_ins)
            #     s_ins.observe(res, ins_inc.rhs)
        
        def close(ins):
            nonlocal depth, bigresult
            # print("  " * depth, "close ", ins)
            lm = []
            under = []
            for u_occ, get_u_ins, get_ins_inc in self.pfunctor.iter_under(ins, matches): # iter under
                if u_occ in matches: # instance already encountered
                    u_ins = matches[u_occ]
                    ins_inc = get_ins_inc(u_ins)
                else: # new instance
                    u_ins = get_u_ins()
                    ins_inc = get_ins_inc(u_ins)
                    add_instance(u_ins)
                    if self.pfunctor.is_small(u_ins):
                        fifo.insert(0, u_ins)
                if u_ins.result != None: # already visited by close
                    if u_ins.result.c != cpt: # other wave
                        lm += [u_ins]
                        u_ins.alt_subresult = u_ins.subresult
                        u_ins.alt_result = u_ins.result
                        if u_ins.alt_result != bigresult:
                            print("FUCK")
                        add_result(u_ins)
                else:
                    depth -= 1
                    lm += close(u_ins)
                    depth += 1
                under += [(u_ins, ins_inc)]
            add_result(ins)
            for u_ins, ins_inc in under: # update subresults under
                # if u_ins.result.c != cpt: # store other result
                #     u_ins.alt_subresult = u_ins.subresult
                #     u_ins.alt_result = u_ins.result
                #     # u_ins.result.obs_by.remove(u_ins)
                #     add_result(u_ins) # work with this one
                #     # print(u_ins.alt_result.rhs, u_ins.result.rhs)
                #     # assert u_ins.alt_result.rhs == u_ins.result.rhs
                if u_ins.subresult == None:
                    print(">>>")
                    print(u_ins.result.object)
                    print("----")
                    for i in u_ins.result.obs_by:
                        print(i.subresult.cod if i.subresult != None else None)
                    print(">>>")
                    new_subresult = ins_inc.rhs() if ins.subresult == None else ins_inc.rhs().compose(ins.subresult)
                    print("ns", new_subresult)
                    for u_u_ins in u_ins.result.obs_by:
                        if u_ins != u_u_ins:
                            assert u_u_ins.result == u_ins.result
                            u_u_ins.observe(ins.result, new_subresult if u_u_ins.subresult == None else u_u_ins.subresult.compose(new_subresult))
                    u_ins.observe(ins.result, new_subresult)
            for s_occ, get_s_ins, get_ins_inc in self.pfunctor.iter_self_inclusions(ins, matches): # add siblings
                if s_occ not in matches:
                    s_ins = get_s_ins()
                    ins_inc = get_ins_inc(s_ins)
                    try:
                        rhs = ins_inc.rhs()
                        add_instance(s_ins)
                        s_ins.auto = True
                        new_subresult = rhs if ins.subresult == None else rhs.compose(ins.subresult)
                        s_ins.observe(ins.result, new_subresult)
                    except:
                        pass # here some symetry is broken
            # print("  " * depth, "close ret ", lm)
            return lm
        
        def star(ins):
            nonlocal depth, bigresult
            top = True
            uppercone = []
            for o_occ, get_o_ins, _ in self.pfunctor.pmatch_up(ins, matches):
                top = False
                if o_occ in matches:
                    o_ins = matches[o_occ]
                else:
                    o_ins = get_o_ins()
                    add_instance(o_ins)
                uppercone.append(o_ins)
                if not o_ins.black:
                    depth += 1
                    uppercone += star(o_ins)
                    depth -= 1
                else:
                    uppercone += o_ins.uppercone
            ins.uppercone = uppercone
            ins.black = True
            if top:# and not ins.auto: # on oublie les automorphismes des tops
                if not ins.auto:
                    lm = close(ins)
                    print("lol")
                    print(lm)
                    print(type(lm))
                    if len(lm) > 0:
                        assert len(lm) > 0
                        # print(lm)
                        r_new, _ = Result.multi_merge_2(lm, self.pfunctor.CD, matches)
                        if len(r_new) > 0:
                            bigresult = r_new[0]
                            r_new[0].c = cpt - 1
                    elif bigresult == None:
                        bigresult = ins.result
                        bigresult.c = cpt - 1
            return uppercone

        for get_s_ins in self.pfunctor.next_small(X):
            s_ins = get_s_ins()
            add_instance(s_ins)
            fifo.insert(0, s_ins)
            break

        while len(fifo) > 0:
            small_ins = fifo.pop()
            # print()
            # print("FIFO POP")
            # print()
            star(small_ins)
            # for match in matches:
            #     print(matches[match])
            #     print(matches[match].result)
            # print()
            for dep_ins in small_ins.uppercone:
                if dep_ins.decrNbDep():
                    # if len(dep_ins.result.obs_by) == 0:
                    #     assert False # should remove result
                    del matches[dep_ins.occ]
            # small_ins.result.obs_by.remove(small_ins)
            del matches[small_ins.occ]
            cpt += 1
        
        return bigresult