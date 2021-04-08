class Instance():
    def __init__(self, rule, nb_dep, occ): # privé à GT
        self.stared = False
        self.closed = False
        self.rule = rule
        self.nb_dep = nb_dep
        self.occ = occ          # C[rule.lhs, X]
        self.old_result = None      # Result or None
        self.old_subresult = None   # C[rule.rhs, self.result.object] or None
        self.new_result = None
        self.new_subresult = None
        self.uppercone = []
        self.underincs = []
    
    def observe(self, res, m): # privé à GT ?
        if self.new_result is not None:
            if self.new_result == res:
                return
            self.old_result = self.new_result
            self.old_subresult = self.new_subresult
        self.new_result = res
        self.new_subresult = m
        res.obs_by.append(self)

    def decrNbDep(self): # privé à GT ?
        self.nb_dep -= 1
        if self.nb_dep == 0:
            return True # should remove ins
        return False

    def __repr__(self):
        return "Instance : [" + " occ : " + str(self.occ) + " | new_result : " + str(self.new_result) + " | new_subresult : " + str(self.new_subresult) + " | old_result : " + str(self.old_result) + " | old_subresult : " + str(self.old_subresult) + "]"

class InstanceInc():
    def get_lhs(self):
        pass

    def get_rhs(self):
        pass
    
    def __repr__(self):
        pass

    def compose(self, other):
        return CompInstanceInc(self, other)

class PrimeInstanceInc(InstanceInc):
    def __init__(self, rule_inc, s, t):
        self.rule_inc = rule_inc
        self.s = s
        self.t = t
        self.result = None
    
    def get_lhs(self):
        return self.rule_inc.lhs
    
    def get_rhs(self):
        return self.rule_inc.rhs

    def __repr__(self):
        return "PrimeInsInc : [" + " lhs : " + str(self.rule_inc.lhs) + " ]"

class CompInstanceInc(InstanceInc):
    def __init__(self, f, g):
        # assert f.t == g.s
        self.lhs = None
        self.s = f.s
        self.f = f
        assert isinstance(g, InstanceInc)
        self.g = g
        self.t = g.t
        self.rhs = None
    
    def get_lhs(self):
        if self.lhs == None:
            self.lhs = self.f.get_lhs().compose(self.g.get_lhs())
        return self.lhs
    
    def get_rhs(self):
        if self.rhs == None: 
            self.rhs = self.f.get_rhs().compose(self.g.get_rhs())
        return self.rhs
    
    def __repr__(self):
        return "CompInsInc : [" + " lhs : " + str(self.lhs) + " ]"

class ColimInc(InstanceInc):
    def __init__(self, rhs, s, t):
        self.rhs = rhs
        self.s = s
        self.t = t

    def get_lhs(self):
        raise "Not implemented"
    
    def get_rhs(self):
        return self.rhs
    
    def __repr__(self):
        return "ColimInc : [" + " rhs : " + str(self.rhs) + " ]"

class Result():
    def __init__(self, obj, is_rhs):
        self.object = obj
        self.is_rhs = is_rhs
        self.obs_by = []
    
    @staticmethod
    def multi_merge_2(lm, CD):
        # CONVERTER
        l_new = []
        l_old = []
        res_old = None
        res_new = None
        for ins in lm:
            l_new.append(ins.new_subresult.get_rhs())
            l_old.append(ins.old_subresult.get_rhs())
            if res_old is None:
                res_old = ins.old_result
            if res_new is None:
                res_new = ins.new_result

        # END CONVERTER
        if len(l_old) == 0:
            return [], []
        if res_old.is_rhs:
            assert res_new.is_rhs
            obj, on_old, on_new = CD.multi_merge(l_old, l_new)
            on_old = ColimInc(on_old, res_old, obj)
            on_new = ColimInc(on_new, res_old, obj)
            res = Result(obj, False)
            for ins in res_old.obs_by:
                if ins.new_result == res_old:
                    ins.observe(res, on_old if ins.new_subresult is None else ins.new_subresult.compose(on_old))
                elif ins.old_result == res_old:
                    ins.observe(res, on_old if ins.old_subresult is None else ins.old_subresult.compose(on_old))
                else:
                    assert False
            res_old.obs_by = None
            res_old.object = None
            for ins in res_new.obs_by:
                if ins.new_result != res: # already set ?
                    if ins.new_result == res_new:
                        ins.observe(res, on_new if ins.new_subresult is None else ins.new_subresult.compose(on_new))
                    elif ins.old_result == res_new:
                        assert False
                    else:
                        assert False
            res_new.obs_by = None
            res_new.object = None
            return res
        obj, on_new = CD.multi_merge_2_in_1(l_old, l_new)
        on_new = ColimInc(on_new, res_new, obj)
        for ins in res_new.obs_by:
            if ins.new_result != res_old:
                if ins.new_result == res_new:
                    ins.observe(res_old, on_new if ins.new_subresult is None else ins.new_subresult.compose(on_new))
                elif ins.old_result == res_new:
                    assert False
                else:
                    assert False
        res_new.obs_by = None
        res_new.object = None
        return res_old
