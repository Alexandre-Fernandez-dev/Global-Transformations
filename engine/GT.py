from .Memory import Result

class GT:
    def __init__(self, pfunctor):
        self.pfunctor = pfunctor

    def __call__(self, X):
        return self.extend(X)

    def extend(self, X):
        matches = {}
        bigresult = None
        fifo = []

        def add_instance(ins):
            assert ins.occ not in matches
            matches[ins.occ] = ins
            ins.auto = False
        
        def close(ins):
            # print("CLOSE", ins)
            nonlocal bigresult
            lm = []
            underincs = [] # change to list ?
            print("close", ins)
            for s_occ, get_s_ins, get_ins_inc in self.pfunctor.iter_self_inclusions(ins): # add siblings
                # assert s_occ not in matches
                if s_occ not in matches:
                    print("NEW AUTO")
                    s_ins = get_s_ins()
                    ins_inc = get_ins_inc(s_ins)
                    add_instance(s_ins)
                    s_ins.auto = True
                    s_ins.closed = True
                    print(s_ins)
                    underincs.append(ins_inc) # added to fix bug -> not fixed remove if not necessary
                else:
                    print("ALREADY KNOWN AUTO")
                    s_ins = matches[s_occ]
                    assert s_ins.auto and s_ins.closed
                    print(s_ins)
                    assert False
                    ins_inc = get_ins_inc(s_ins)
                    underincs.append(ins_inc)
            print(">>>>>>end for")
            for u_occ, get_u_ins, get_ins_inc in self.pfunctor.iter_under(ins):# iter under
                # print(u_occ in matches.keys())
                if u_occ in matches: # instance already encountered
                    # print(matches[u_occ])
                    # print(matches[u_occ].closed)
                    # ancienne instance n'a peut être pas encore ses auto
                    u_ins = matches[u_occ]
                    ins_inc = get_ins_inc(u_ins)
                else: # new instance
                    # nouvelle instance n'a pas encore ses auto
                    u_ins = get_u_ins()
                    u_ins.closed = False
                    ins_inc = get_ins_inc(u_ins)
                    add_instance(u_ins)
                    if self.pfunctor.is_small(u_ins):
                        fifo.insert(0, u_ins)
                underincs.append(ins_inc)
                if not u_ins.closed:
                    acc_lm, acc_ui = close(u_ins)
                    for ii in acc_ui:
                        underincs.append(ii.compose(ins_inc))
                    lm += acc_lm
                    print("   edit lm acc")#, [ i.occ for i in acc_lm ])
                elif not u_ins.auto and u_ins.new_result is not None: # already visited by other close
                    lm += [u_ins]
                    print("   edit lm init", u_ins.occ)
            ins.closed = True
            return lm, underincs
        
        def star(ins):
            nonlocal bigresult
            top = True
            uppercone = []
            for o_occ, get_o_ins, _ in self.pfunctor.pmatch_up(ins):
                top = False
                if o_occ in matches:
                    o_ins = matches[o_occ]
                else:
                    o_ins = get_o_ins()
                    add_instance(o_ins)
                uppercone.append(o_ins)
                if not o_ins.stared:
                    uppercone += star(o_ins)
                else:
                    uppercone += o_ins.uppercone
            ins.uppercone = uppercone
            ins.stared = True
            if top:
                print("TOP", ins)
                if not ins.auto:
                    lm, underincs = close(ins)
                    ins.underincs = underincs
                    ins.compute_result()
                    if len(lm) > 0:
                        bigresult = Result.multi_merge_2(lm, self.pfunctor.CD)
                    elif bigresult is None:
                        bigresult = ins.new_result
                        print("FIRST RESULT :")
                        print(bigresult.object)
                        print("--")
            return uppercone

        for get_s_ins in self.pfunctor.next_small(X):
            s_ins = get_s_ins()
            add_instance(s_ins)
            fifo.insert(0, s_ins)
            break

        while len(fifo) > 0:
            small_ins = fifo.pop()
            print("new small ins: ", small_ins)
            star(small_ins)
            print("exit star")
            for dep_ins in small_ins.uppercone:
                if dep_ins.decrNbDep():
                    del matches[dep_ins.occ]
            del matches[small_ins.occ]

        return bigresult
