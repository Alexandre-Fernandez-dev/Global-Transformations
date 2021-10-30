from .Memory import Result

class GT:
    """
    The class for a given global transformation
    
    Attributes
    ----------
    pfunctor: PFunctor
        the partial functor of local rules
    
    Methods
    ----------
    extend(X): pfunctor.CD.TO()
        compute the global transformation of X
    """
    def __init__(self, pfunctor):
        self.pfunctor = pfunctor
        self.draw_step = None
        self.draw_merge = None
        self.collect_comma_arrow = None
        self.collect_comma_object = None

    def __call__(self, X):
        return self.extend(X)

    def extend(self, X):
        matches = {}            # pfunctor.CS.TO() -> Instance : given a known match morphism get his associated Instance
        rhs = True              # is the result a rhs or a composite object ?
        bigresult = None        # the partial / final result of the computation
        uins_bigresult = {}     # Instance -> pfunctor.CD.TM() : the cocone says how a known instance result is included in bigresult
        fifo = []               # The fifo of small instances to treat
        
        # dummy class to represent an identity morphism, only used once in a computation
        class Identity(): # TODO given by datastructure ?
            def __init__(self):
                pass

            def compose(self, h):
                return h

        def add_instance(ins, auto = False):  # add a known instance in matches
            assert ins.occ not in matches
            if self.collect_comma_object != None and not auto:
                self.collect_comma_object(ins)
            matches[ins.occ] = ins
            ins.auto = auto

        # recursively finds and add in memory all new sub-instances under an instance
        # when a minimal instance is found, adds it in the fifo of small instances to treat
        # returns the suture (list of instances) between the big_result with the new rhs
        # and all inclusions to the new rhs
        def close(ins): 
            lm = []
            underincs = {}
            for s_occ, get_s_ins, get_ins_inc in self.pfunctor.iter_self_inclusions(ins): # add siblings
                assert s_occ not in matches
                s_ins = get_s_ins()
                ins_inc = get_ins_inc(s_ins)
                add_instance(s_ins, auto=True)
                s_ins.closed = True
                s_ins.overins = ins.overins
                underincs[s_ins] = ins_inc.get_rhs() # TODO not necessary, added for equiv underincs matches
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
                if self.collect_comma_arrow != None:
                    self.collect_comma_arrow(ins_inc, False)
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
        
        # recursively finds and add in memory all new super-instances over an instance
        # when a maximal instance is found, calls close on it and then merges his result whith the actual big_result
        def star(ins):
            nonlocal bigresult, uins_bigresult, rhs
            top = True
            for o_occ, get_o_ins, get_ins_inc in self.pfunctor.pmatch_up(ins):
                top = False
                if o_occ in matches:
                    o_ins = matches[o_occ]
                else:
                    o_ins = get_o_ins()
                    add_instance(o_ins)
                if self.collect_comma_arrow != None:
                    self.collect_comma_arrow(get_ins_inc(o_ins), True)
                ins.overins.append(o_ins)
                if not o_ins.stared and not o_ins.auto:
                    star(o_ins)
            ins.stared = True
            if top:
                if not ins.auto:
                    lm, underincs = close(ins)
                    underincs[ins] = Identity() # TODO not necessary, added for bijection underincs <=> matches
                    if len(lm) > 0:
                        if(self.draw_merge != None):
                            self.draw_merge(lm, underincs, uins_bigresult)
                        bigresult, acc_uins_big_result = Result.multi_merge_2(lm, underincs, uins_bigresult, self.pfunctor.CD, not rhs)
                        if(self.draw_step != None):
                            self.draw_step(bigresult)
                        uins_bigresult.update(acc_uins_big_result)
                        rhs = False
                    elif bigresult is None:
                        bigresult = ins.rule.rhs
                        if(self.draw_step != None):
                            self.draw_step(bigresult)
                        uins_bigresult = underincs

        # finds a first small match to start the algorithm
        for get_s_ins in self.pfunctor.next_small(X):
            s_ins = get_s_ins()
            add_instance(s_ins)
            fifo.insert(0, s_ins)
            break
            
        # clear memory over an treated instance
        def mem_cl(ins):
            if ins.decrNbDep():
                del matches[ins.occ]
                del uins_bigresult[ins]
                for oi in ins.overins:
                    mem_cl(oi)

        # while there is small instances to treat in the fifo call star on it to continue computation
        while len(fifo) > 0:
            small_ins = fifo.pop()
            star(small_ins)
            mem_cl(small_ins)
            # print(len(matches), len(uins_bigresult))

        return bigresult
