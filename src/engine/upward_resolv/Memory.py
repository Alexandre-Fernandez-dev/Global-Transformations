class Instance():
    def __init__(self, rule, nb_dep, occ): # privé à GT
        self.black = False
        self.rule = rule
        self.nb_dep = nb_dep
        self.occ = occ          # C[rule.lhs, X]
        self.result = None      # Result or None
        self.alt_result = None
        self.subresult = None   # C[rule.rhs, self.result.object] or None
        self.alt_subresult = None
        self.uppercone = []
    
    def rhs(self):
        return self.rule.get_rhs()
    
    def observe(self, res, m): # privé à GT ?
        #if self in res.obs_by:
        #    return
        # assert not self in res.obs_by # removed because of alt_result / result, instance associated to two result
        assert m == None or m.cod == res.object
        self.result = res
        self.subresult = m
        res.obs_by.append(self)

    def decrNbDep(self): # privé à GT ?
        self.nb_dep -= 1
        if self.nb_dep == 0:
            # self.result.obs_by.remove(self)
            return True # should remove ins
        return False

    def __repr__(self):
        return "Instance : [" + " occ : " + str(self.occ) + " | result : " + str(self.result) + " | subresult : " + str(self.subresult) + "]"

class InstanceInc():
    def __init__(self, rule_inc, s, t):
        self.rule_inc = rule_inc
        self.s = s
        self.t = t
    
    def rhs(self):
        return self.rule_inc.get_rhs()
    
    def __repr__(self):
        return "InsInc : [" + " lhs : " + str(self.rule_inc.lhs) + " ]"

class Result():
    def __init__(self, obj, is_rhs):
        self.object = obj
        self.is_rhs = is_rhs
        self.obs_by = []
    
    @staticmethod
    def triv_merge(res, h, u_res):
        for ins in u_res.obs_by:
            ins.observe(res, h if ins.subresult == None else ins.subresult.compose(h))
        for i in res.obs_by:
            assert i.subresult == None or i.subresult.cod == res.object
        u_res.obs_by = None
        u_res.object = None
        return u_res # to remove of results
    
    @staticmethod
    def multi_merge_2(lm, CD, m):
        l_new = []
        l_old = []
        res_old = None
        res_new = None
        for ins in lm:
            # print(ins.alt_subresult)
            # print(ins.alt_result)
            # print(ins.subresult)
            # print(ins.result)
            l_old.append(ins.alt_subresult)
            l_new.append(ins.subresult)
            if res_old == None:
                res_old = ins.alt_result
                res_new = ins.result
            # else:
            #     print(res_new)
            #     print(ins.alt_result)
            #     assert res_new == ins.alt_result
            #     assert res_old == ins.result
        return Result.multi_merge(l_old, l_new, res_old, res_new, CD, m)
    
    @staticmethod
    def multi_merge(l_old, l_new, res_old, res_new, CD, m):
        # print("MULTI MERGE", len(l_old), len(l_new))
        # print("res", res_old, res_new)
        # all l_old must refer to an instance with result res_old, same for res_new
        # for i in m:
        #     print(m[i].result)
        if len(l_old) == 0:
            return [], []
        if res_old.is_rhs:
            assert res_new.is_rhs
            obj, on_old, on_new = CD.multi_merge(l_old, l_new)
            res = Result(obj, False)
            print("----")
            print(on_old)
            print([i.subresult for i in res_old.obs_by])
            print("----")
            for ins in res_old.obs_by:
                if ins.result == res_old:
                    ins.observe(res, on_old if ins.subresult is None else ins.subresult.compose(on_old))
                elif ins.alt_result == res_old:
                    ins.observe(res, on_old if ins.alt_subresult is None else ins.alt_subresult.compose(on_old))
                else:
                    assert False
            res_old.obs_by = None
            res_old.object = None
            for ins in res_new.obs_by:
                if ins.result != res: # already set ?
                    if ins.result == res_new:
                        ins.observe(res, on_new if ins.subresult is None else ins.subresult.compose(on_new))
                    elif ins.alt_result == res_new:
                        assert False
                        ins.observe(res, on_new if ins.alt_subresult is None else ins.alt_subresult.compose(on_new))
                    else:
                        assert False
            for i in res.obs_by:
                i.alt_result = None
                i.alt_subresult = None
            res_new.obs_by = None
            res_new.object = None
            # print()
            # for i in m:
            #     print(m[i].result)
            return [res], [res_old, res_new]
        else:
            obj, on_new = CD.multi_merge_2_in_1(l_old, l_new)
            for ins in res_new.obs_by:
                if ins.result != res_old:
                    if ins.result == res_new:
                        ins.observe(res_old, on_new if ins.subresult is None else ins.subresult.compose(on_new))
                    elif ins.alt_result == res_new:
                        assert False
                        ins.observe(res_old, on_new if ins.alt_subresult is None else ins.alt_subresult.compose(on_new))
                    else:
                        assert False
            for i in res_old.obs_by:
                i.alt_result = None
                i.alt_subresult = None
            res_new.obs_by = None
            res_new.object = None
            return [], [res_new]