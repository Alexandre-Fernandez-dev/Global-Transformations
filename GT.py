import networkx as nx
import PFunctor

depth = 0

class GT:
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
                for small_rule, inc_l in self.pfunctor.iter_small(rule):
                    small_match = inc_l.compose(ins)
                    # print("NEW small match ", small_match)
                    # for mins in matches:
                    #     print(mins)
                    #     print(id(mins))
                    #     print(mins == small_match)
                    #     print(type(mins))
                    #     print(type(small_match))
                    if small_match not in matches:
                        # print("NOT IN MATCHES")
                        small_ins = add_instance(small_rule, small_match, False)
                        fifo.insert(0, small_ins)
                    else:
                        # print("IN MATCHES")
                        small_ins = matches[small_match]
                    small_ins.uppercone.append(self_)

            def observe(self, res, m):
                # assert m == None or (m.dom == self.rule.rhs and m.cod == res.object)
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
                for ins in u_res.obs_by:
                    ins.observe(res, on_u if ins.subresult == None else ins.subresult.compose(on_u))
                u_res.obs_by = None
                u_res.object = None
                results.remove(u_res)

        def multi_merge(l_merges):
            if len(l_merges) == 0:
                return
            res_old, res_new = None, None
            mult_merge_arg1 = []
            mult_merge_arg2 = []
            for res_old_i, h_old, res_new_i, h_new in l_merges:
                if res_new == None:
                    res_new = res_new_i
                else:
                    assert(res_new == res_new_i)
                if res_old == None:
                    res_old = res_old_i
                else:
                    # print(res_old.object)
                    # print(res_old_i.object)
                    assert(res_old == res_old_i)
                mult_merge_arg1.append(h_old) #TODO improve
                mult_merge_arg2.append(h_new)
            assert res_old != None and res_new != None
            if res_old.is_rhs:
                assert res_new.is_rhs #FIXME fail in some gmap
                obj, on_old, on_new = self.pfunctor.CD.multi_merge(mult_merge_arg1, mult_merge_arg2)
                res = Result(obj, False)
                results.add(res)
                for ins in res_old.obs_by:
                    ins.observe(res, on_old if ins.subresult is None else
                                ins.subresult.compose(on_old))
                res_old.obs_by = None
                res_old.object = None
                results.remove(res_old)
                for ins in res_new.obs_by:
                    ins.observe(res, on_new if ins.subresult is None else
                                ins.subresult.compose(on_new))
                res_new.obs_by = None
                res_new.object = None
                results.remove(res_new)
            else:
                obj, on_new = self.pfunctor.CD.multi_merge_2_in_1(mult_merge_arg1, mult_merge_arg2)
                for ins in res_new.obs_by:
                    ins.observe(res_old, on_new if ins.subresult is None else
                                ins.subresult.compose(on_new))
                res_new.obs_by = None
                res_new.object = None
                results.remove(res_new)

            def __repr__(self):
                return str(self.object) + ", observed by " + str(-1 if self.obs_by is None else len(self.obs_by)) + " instance(s)"

        matches = {}
        results = set()
        fifo = []
        depth = 0

        def add_instance(rule, match, black):
            global depth
            res = Result(rule.rhs, True)
            results.add(res)
            ins = Instance(rule, match, black)
            ins.observe(res, None)
            matches[match] = ins
            for auto in self.pfunctor.iter_self_inclusions(rule):
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
                ins_.observe(res,auto.rhs)
                matches[match_] = ins_
            return ins

        def close(ins):
            global depth
            # print("  " * depth, "CLOSE", ins)
            l = []
            for get_u_rule, get_u_inc, under_match in self.pfunctor.iter_under(ins):
                if under_match not in matches:
                    under_match.clean()
                    under_ins = add_instance(get_u_rule(), under_match, False)
                else:
                    under_ins = matches[under_match]
                u_inc = get_u_inc(under_ins.rule)
                depth -= 1
                l += close_aux(under_ins, u_inc, ins)
                depth += 1
            return l

        def close_aux(ins, inc, pins):
            global depth
            # print("  " * depth, "COMPOSE")
            # print(ins, pins)
            new_subresult = inc.rhs if pins.subresult == None else inc.rhs.compose(pins.subresult)
            if ins.subresult is None: # no subresult new one -> easy merge
                Result.triv_merge(pins.result, new_subresult, ins.result, ins.subresult)
                return close(ins)
            else: # there is a subresult
                if not pins.result is ins.result: # not same result, different wave, accumulate
                    return [(ins.result, ins.subresult, pins.result, new_subresult)]
                else: # same result, same wave
                    return []

        def star(ins):
            global depth
            # print("len result", len(results), len(matches))
            # print("  " * depth, "STAR ", ins)
            top = True
            for over_rule, over_match in self.pfunctor.pmatch_up(ins):
                # print("MATCH !!!")
                # print("match_up", over_rule, over_match)
                top = False
                if over_match in matches:
                    over_ins = matches[over_match]
                else:
                    over_match.clean()
                    over_ins = add_instance(over_rule, over_match, False)
                if not over_ins.black:
                    depth += 1
                    star(over_ins)
                    depth -= 1
            ins.black = True
            if top:
                multi_merge(close(ins))

        for small_rule, small_match in self.pfunctor.next_small(X):
            fifo.insert(0, add_instance(small_rule, small_match, False))
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
