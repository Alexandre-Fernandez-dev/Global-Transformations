import networkx as nx
import PFunctor

depth = 0

class GT_DU:
    """
    A global transformation T extends a partial functor

    Methods
    -------
    extend(X)
        compute T(X)

    """

    def __init__(self, pfunctor):
        self.pfunctor = pfunctor


    def extend(self, X):
        """
        compute T(X)

        Parameters
        ----------
        X : CS.O
            the input object

        Returns
        -------
        CD.O
            the result
        """

        class Instance():
            def __init__(self_, rule, ins, black):
                # assert isinstance(rule, PFunctor.Rule)
                # print()
                # print("ins", ins.dom)
                # print("rule", rule.lhs)
                assert ins.dom == rule.lhs
                assert ins.cod == X
                self_.black = black
                self_.rule = rule
                self_.nb_dep = self.pfunctor.nb_small(rule)
                self_.ins = ins          # C[rule.lhs, X]
                self_.result = None      # Result or None
                self_.subresult = None   # C[rule.rhs, self.result.object] or None
                self_.uppercone = []
                # for small_rule, inc_l in self.pfunctor.iter_small(rule):
                #     small_match = inc_l.compose(ins)
                #     # print("NEW small match ", small_match)
                #     # for mins in matches:
                #     #     print(mins)
                #     #     print(id(mins))
                #     #     print(mins == small_match)
                #     #     print(type(mins))
                #     #     print(type(small_match))
                #     if small_match not in matches:
                #         # print("NOT IN MATCHES")
                #         small_ins = add_instance(small_rule, small_match, Result(None, True), False)
                #         fifo.insert(0, small_ins)
                #     else:
                #         # print("IN MATCHES")
                #         small_ins = matches[small_match]
                #     small_ins.uppercone.append(self_)

            def observe(self, res, m):
                # assert m == None or (m.dom == self.rule.rhs and m.cod == res.object)
                # print("obs_by", res.obs_by)
                # for i in res.obs_by:
                #     print(i.result.object)
                assert self not in res.obs_by
                self.result = res
                self.subresult = m
                res.obs_by.append(self)

            def decrNbDep(self):
                self.nb_dep -= 1
                # print("nb_dep", self.nb_dep)
                if self.nb_dep == 0:
                    self.result.obs_by.remove(self)
                    # print("  len_obs_by", len(self.result.obs_by))
                    if len(self.result.obs_by) == 0:
                        assert False
                        results.remove(self.result)
                        self.result = None
                        self.subresult = None
                    self.rule = None
                    # print(">>>>>>>>>>>>>>>>>>>>>>>>>>start list matches")
                    # for i in matches:
                    #     print(i, matches[i])
                    #     print(id(i))
                    #     print()
                    # print(id(self.ins))
                    # if self.ins in matches:
                    # print(">>>>>>>>>>>>>>>>>>>>>>>>> del ", self.ins)
                    # print(id(self.ins))
                    del matches[self.ins]
                    # print("WORKED !")

            def __repr__(self):
                return "Instance : [" + " rule : " + str(self.rule) + " | match : " + str(self.ins) + " | result : " + str(self.result) + " | subresult : " + str(self.subresult) + "]"

        class Result():
            def __init__(self,obj,isrhs):
                self.object = obj     # C.Object
                self.is_rhs = isrhs
                self.obs_by = []      # List of ins:Instance with  ins/result = self

            @staticmethod
            def triv_merge(res, h, u_res, u_h):
                assert u_h == None
                # assert h.dom == u_res.object
                on_u = h
                print(h)
                print(u_h)
                for ins in u_res.obs_by:
                    print()
                    print(ins.subresult)
                    print(on_u)
                    old_sb = ins.subresult
                    def new_f():
                        if old_sb == None:
                            return on_u()
                        else:
                            print(old_sb)
                            print(on_u)
                            print("TEST")
                            print(old_sb())
                            print(on_u())
                            return old_sb().compose(on_u())
                    # ins.observe(res, (lambda self : on_u(None)) if ins.subresult == None else (lambda self : ins.subresult(None).compose(on_u(None))))
                    ins.observe(res, new_f)
                u_res.obs_by = None
                u_res.object = None
                results.remove(u_res)

        def multi_merge(l_merges):
            # for res_old_i, h_old, res_new_i, h_new in l_merges:
            #     print("l_merge_i:")
            #     print(res_old_i.object)
            #     print(h_old)
            #     print(res_new_i.object)
            #     print(h_new)
            #     print()
            if len(l_merges) == 0:
                # print("l_merges empty")
                return
            res_old, res_new = None, None
            mult_merge_arg1 = []
            mult_merge_arg2 = []
            for res_old_i, h_old, res_new_i, h_new in l_merges:
                if res_new == None:
                    res_new = res_new_i
                else:
                    print()
                    print(h_new)
                    print(res_new)
                    print(res_new_i)
                    print(res_new.object)
                    print(res_new_i.object)
                    assert(res_new == res_new_i)
                if res_old == None:
                    res_old = res_old_i
                else:
                    # print(res_old.object)
                    # print(res_old_i.object)
                    assert(res_old == res_old_i)
                # import inspect
                # print(inspect.getsource(h_old))
                mult_merge_arg1.append(h_old) #TODO improve
                mult_merge_arg2.append(h_new)
            assert res_old != None and res_new != None
            if res_old.is_rhs:
                assert res_new.is_rhs #FIXME fail in some gmap
                print(mult_merge_arg1)
                print(mult_merge_arg2)
                obj, on_old, on_new = self.pfunctor.CD.multi_merge(mult_merge_arg1, mult_merge_arg2)
                res = Result(obj, False)
                results.add(res)
                for ins in res_old.obs_by:
                    ins.observe(res, (lambda : on_old()) if ins.subresult is None else
                                (lambda : ins.subresult().compose(on_old())))
                res_old.obs_by = None
                res_old.object = None
                results.remove(res_old)
                for ins in res_new.obs_by:
                    ins.observe(res, (lambda : on_new()) if ins.subresult is None else
                                (lambda : ins.subresult().compose(on_new())))
                res_new.obs_by = None
                res_new.object = None
                results.remove(res_new)
            else:
                obj, on_new = self.pfunctor.CD.multi_merge_2_in_1(mult_merge_arg1, mult_merge_arg2)
                for ins in res_new.obs_by:
                    ins.observe(res_old, (lambda : on_new()) if ins.subresult is None else
                                (lambda : ins.subresult().compose(on_new())))
                res_new.obs_by = None
                res_new.object = None
                results.remove(res_new)

            def __repr__(self):
                return str(self.object) + ", observed by " + str(-1 if self.obs_by is None else len(self.obs_by)) + " instance(s)"

        matches = {}
        results = set()
        fifo = []
        depth = 0
        # dummy_result = 

        def add_instance(rule, match, result, black):
            global depth
            # res = Result(rule.rhs, True)
            res = result
            results.add(res)
            ins = Instance(rule, match, black)
            # print("RES", res)
            ins.observe(res, None)
            matches[match] = ins
            for auto in self.pfunctor.iter_self_inclusions(ins, matches):
                # print("FOUND SELF INCLUSION")
                # print("ITER AUTO")
                # print("autolhs", auto.lhs)
                # print("compose")
                # print("match", match)
                # print("result comp")
                # print(auto.lhs.compose(match))
                match_ = auto.lhs.compose(match)
                # print(type(auto))
                ins_ = Instance(auto.g_a, match_, black)
                assert auto.g_b.rhs == ins.rule.rhs
                ins_.observe(res, auto.rhs) # changed auto.rhs to None hope it works
                matches[match_] = ins_
            return ins
        
        def close(ins):
            global depth
            print("  " * depth, "CLOSE", ins)
            l = []
            todo = []
            for u_inc in self.pfunctor.iter_under(ins, matches):
                # print("  " * depth, "under :", u_inc)
                under_match = u_inc.lhs.compose(ins.ins)
                if under_match not in matches:
                    under_match.clean()
                    u_rule = u_inc.g_a
                    under_ins = add_instance(u_rule, under_match, Result(None, True), False)
                    print("  " * depth, "NEW INSTANCE", under_ins)
                    if self.pfunctor.is_small(u_rule):
                        # print("  " * depth, "SMALL")
                        fifo.insert(0, under_ins)
                        # under_ins.result.object = under_ins.rule.rhs
                    # else:
                        # print("  " * depth, "NOT SMALL")
                else:
                    under_ins = matches[under_match]
                    print("  " * depth, "KNOWN INSTANCE", under_ins)
                # u_inc = u_inc(under_ins.rule)
                todo += [(under_ins, u_inc)]
                if under_ins.subresult is None:
                    depth += 1
                    l += close(under_ins)
                    print("  " * depth, "under CLOSE returned", [(a.object, c.object) for a,b,c,d in l])
                    depth -= 1
            print("  " * depth, "ALL under CLOSE returned", [(a.object, c.object) for a,b,c,d in l])

            for under_ins, u_inc in todo:
                print("  " * depth, "TODO ", ins.result, under_ins.result)
                print("  " * depth, ins.rule, under_ins.rule)
                print("  " * depth, u_inc)
                # assert ins.result == dummy_result
                # if ins.result.object == None:
                #     print("  " * depth, "INIT RHS A")
                #     ins.result.object = ins.rule.rhs()
                # if under_ins.result.object == None:
                #     print("  " * depth, "INIT RHS B")
                #     under_ins.result.object = under_ins.rule.rhs()
                # new_subresult = u_inc.rhs if ins.subresult == None else u_inc.rhs.compose(ins.subresult)
                # assert ins.subresult == None
                # print("u_inc.rhs")
                assert under_ins.rule.rhs == u_inc.g_a.rhs
                assert ins.rule.rhs == u_inc.g_b.rhs
                new_subresult = (lambda : u_inc.rhs()) if ins.subresult == None else (lambda : u_inc.rhs().compose(ins.subresult()))
                # print("new subresult", new_subresult)
                if under_ins.subresult is None: # no subresult new one -> easy merge
                    print("  " * depth, ">>>>> triv_merge")
                    # print(new_subresult.cod, under_ins.subresult.cod)
                    l = [ (a, b, c, d) for a, b, c, d in l if c is not under_ins.result ]
                    Result.triv_merge(ins.result, new_subresult, under_ins.result, under_ins.subresult)
                else: # there is a subresult
                    # print(">>>>>>>results", ins.result, under_ins.result)
                    # print("  " * depth, ins.subresult(), under_ins.subresult())
                    # print("  " * depth, new_subresult(), under_ins.subresult())
                    if ins.result is not under_ins.result: # not same result, different wave, accumulate
                        print("\n\n")
                        print("  " * depth, ">>>>>>>>>>>> ", ins.result.object)
                        print("\n\n")
                        l += [(under_ins.result, under_ins.subresult(), ins.result, new_subresult())]
            
            print("\n\n")
            print("  " * depth, "close", ins)
            print("  " * depth, "close returns ", [(a.object, c.object) for a,b,c,d in l])
            print("\n\n")
            return l

        # def close_aux(ins, inc, pins):
        #     global depth
        #     # print("  " * depth, "COMPOSE")
        #     # print(inc.rhs)
        #     # print(inc.auto)
        #     new_subresult = inc.rhs if pins.subresult == None else inc.rhs.compose(pins.subresult)
        #     if ins.subresult is None: # no subresult new one -> easy merge
        #         Result.triv_merge(pins.result, new_subresult, ins.result, ins.subresult)
        #         return close(ins)
        #     else: # there is a subresult
        #         if not pins.result is ins.result: # not same result, different wave, accumulate
        #             return [(ins.result, ins.subresult, pins.result, new_subresult)]
        #         else: # same result, same wave
        #             return []

        def star(ins):
            global depth
            # print("len result", len(results), len(matches))
            print("  " * depth, "STAR ", ins)
            uppercone = []
            assert not ins.black
            top = True
            for over_rule, over_match in self.pfunctor.pmatch_up(ins, matches):
                # print("  " * depth, "match_up", over_rule, over_match)
                top = False
                if over_match in matches:
                    over_ins = matches[over_match]
                else:
                    over_match.clean()
                    over_ins = add_instance(over_rule, over_match, Result(None, True), False)
                uppercone.append(over_ins)
                if not over_ins.black:
                    depth += 1
                    uppercone += star(over_ins)
                    depth -= 1
                else:
                    uppercone += over_ins.uppercone
            ins.uppercone = uppercone
            ins.black = True
            if top:
                # print("  " * depth, "TOP")
                # multi_merge(close(ins))
                l = close(ins)
                print("CLOSE RETURNED ")
                for a, b, c, d in l:
                    print(a, b)
                    print(c, d)
                    print()
                multi_merge(l)
            return uppercone

        for small_rule, small_match in self.pfunctor.next_small(X):
            fifo.insert(0, add_instance(small_rule, small_match, Result(None, True), False))
            break

        while len(fifo) > 0:
            depth = 0
            small_ins = fifo.pop()
            # print("SMALL", small_ins)
            assert not small_ins.black
            star(small_ins)
            for dep_ins in small_ins.uppercone:
                #print(dep_ins)
                dep_ins.decrNbDep()
            small_ins.result.obs_by.remove(small_ins)
            small_ins.ins.rule = None
            # print(">>>>>>>>>>>>>>>>>>>>>>>>> del ", small_ins.ins, id(small_ins.ins))
            #for ins in matches:
            #    print(ins)
            #    print(id(ins))
            #    print(ins == small_ins.ins)
            #    print(type(small_ins.ins))
            #    print(type(ins))
            del matches[small_ins.ins]
            # print("DELETED")
            # for ins in matches:
            #     print(ins)
            #     print(id(ins))

        # print(len(results), len(matches))
        # for result in results:
        #     print(result.object)
        return results
