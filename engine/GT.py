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
            nonlocal bigresult
            lm = []
            underincs = [] # change to list ?
            for u_occ, get_u_ins, get_ins_inc in self.pfunctor.iter_under(ins):# iter under
                if u_occ in matches: # instance already encountered
                    u_ins = matches[u_occ]
                    ins_inc = get_ins_inc(u_ins)
                else: # new instance
                    u_ins = get_u_ins()
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
                elif u_ins.new_result is not None: # already visited by other close
                    lm += [u_ins]
            ins.closed = True
            for s_occ, get_s_ins, get_ins_inc in self.pfunctor.iter_self_inclusions(ins): # add siblings
                if s_occ not in matches:
                    s_ins = get_s_ins()
                    ins_inc = get_ins_inc(s_ins)
                    add_instance(s_ins)
                    s_ins.auto = True
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
                if not ins.auto:
                    lm, underincs = close(ins)
                    if len(lm) > 0:
                        ins.compute_result(underincs)
                        r_new, _ = Result.multi_merge_2(lm, self.pfunctor.CD)
                        if len(r_new) > 0:
                            bigresult = r_new[0]
                    elif bigresult is None:
                        ins.compute_result(underincs)
                        bigresult = ins.new_result
            return uppercone

        for get_s_ins in self.pfunctor.next_small(X):
            s_ins = get_s_ins()
            add_instance(s_ins)
            fifo.insert(0, s_ins)
            break

        while len(fifo) > 0:
            small_ins = fifo.pop()
            star(small_ins)
            for dep_ins in small_ins.uppercone:
                if dep_ins.decrNbDep():
                    del matches[dep_ins.occ]
            del matches[small_ins.occ]

        return bigresult
