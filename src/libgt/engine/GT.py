from .Memory import Result

class GT:
    def __init__(self, pfunctor):
        self.pfunctor = pfunctor

    def __call__(self, X):
        return self.extend(X)

    def extend(self, X):
        matches = {}
        rhs = True
        bigresult = None
        uins_bigresult = {}
        fifo = []

        def add_instance(ins):
            assert ins.occ not in matches
            matches[ins.occ] = ins
            ins.auto = False
        
        def close(ins):
            lm = []
            underincs = {}
            # print("close", ins)
            for s_occ, get_s_ins, get_ins_inc in self.pfunctor.iter_self_inclusions(ins): # add siblings
                assert s_occ not in matches
                s_ins = get_s_ins()
                ins_inc = get_ins_inc(s_ins)
                add_instance(s_ins)
                s_ins.auto = True
                s_ins.closed = True
                s_ins.overins = ins.overins
                underincs[s_ins] = ins_inc.get_rhs() # necessary ? added for equiv underincs matches
            for u_occ, get_u_ins, get_ins_inc in self.pfunctor.iter_under(ins):# iter under
                if u_occ in matches: # instance already encountered
                    u_ins = matches[u_occ]
                    ins_inc = get_ins_inc(u_ins)
                else: # new instance
                    u_ins = get_u_ins()
                    u_ins.closed = False
                    ins_inc = get_ins_inc(u_ins)
                    add_instance(u_ins)
                    if self.pfunctor.is_small(u_ins):
                        fifo.insert(0, u_ins)
                underincs[u_ins] = ins_inc.get_rhs()
                if not u_ins.closed:
                    acclm, accui = close(u_ins)
                    lm += acclm
                    for ui in accui:
                        underincs[ui] = accui[ui].compose(ins_inc.get_rhs())
                elif not u_ins.auto and u_ins in uins_bigresult.keys(): # already visited by other close
                    lm += [u_ins]
            ins.closed = True
            return lm, underincs
        
        def star(ins):
            nonlocal bigresult, uins_bigresult, rhs
            top = True
            for o_occ, get_o_ins, _ in self.pfunctor.pmatch_up(ins):
                top = False
                if o_occ in matches:
                    o_ins = matches[o_occ]
                else:
                    o_ins = get_o_ins()
                    add_instance(o_ins)
                ins.overins.append(o_ins)
                if not o_ins.stared and not o_ins.auto:
                    star(o_ins)
            ins.stared = True
            if top:
                if not ins.auto:
                    lm, underincs = close(ins)
                    underincs[ins] = None # not necessary, added for equiv underincs matches
                    if len(lm) > 0:
                        bigresult, acc_uins_big_result = Result.multi_merge_2(lm, underincs, uins_bigresult, self.pfunctor.CD, not rhs)
                        uins_bigresult.update(acc_uins_big_result)
                        rhs = False
                    elif bigresult is None:
                        bigresult = ins.rule.rhs
                        uins_bigresult = underincs

        for get_s_ins in self.pfunctor.next_small(X):
            s_ins = get_s_ins()
            add_instance(s_ins)
            fifo.insert(0, s_ins)
            break
            
        def mem_cl(ins):
            # print("before ", ins.nb_dep)
            if ins.decrNbDep():
                del matches[ins.occ]
                del uins_bigresult[ins]
                for oi in ins.overins:
                    mem_cl(oi)
            # print("after ", ins.nb_dep)

        while len(fifo) > 0:
            small_ins = fifo.pop()
            star(small_ins)
            mem_cl(small_ins)
            print(len(matches), len(uins_bigresult))

        return bigresult
