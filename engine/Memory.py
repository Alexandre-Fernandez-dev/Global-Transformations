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
    
    def compute_result(self):
        if hasattr(self.rule.rhs, 'eval'):
            # assert self.new_result is None
            rhs = self.rule.rhs.eval(self.underincs)
        else:
            rhs = self.rule.rhs
        res = Result(rhs, True)
        self.observe(res, None) # effet de bord
        for ins_inc in self.underincs: # return span ?
            sub = ins_inc.compute_result() # when ensure observe is safe, make this as a lazy lambda (run when needed in merge)
            ins_inc.s.observe(res, sub) # effet de bord
        return res
    
    def observe(self, res, m): # privé à GT ?
        # assert m is None or m.cod == res.object
        if self.new_result is not None:
            # ons, ins = self.new_subresult
            # om, im = m
            # print(ons.ev[ins])
            # print(om.ev[im])
            # assert ons.ev[ins].dom == om.ev[im].dom
            if self.new_result == res:
                # assert self.new_subresult == m
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
    
    def get_result(self):
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
    
    def compute_result(self):
        if hasattr(self.rule_inc.rhs, 'eval'):
            assert self.result == None
            self.result = self.rule_inc.rhs.eval(self.t.new_result.object)
            return self.result
        return self.rule_inc.rhs

    def __repr__(self):
        return "PrimeInsInc : [" + " lhs : " + str(self.rule_inc.lhs) + " ]"

class CompInstanceInc(InstanceInc):
    def __init__(self, f, g):
        assert f.t == g.s
        self.lhs = f.get_lhs().compose(g.get_lhs()) # lazy ?
        self.s = f.s
        self.f = f
        self.g = g
        self.t = g.t
        self.result = None
        self.rhs = None
    
    def get_lhs(self):
        return self.lhs
    
    def get_rhs(self):
        if self.rhs == None: 
            self.rhs = self.f.get_rhs().compose(self.g.get_rhs())
        return self.rhs
    
    def compute_result(self):
        # assert self.rhs == None
        if hasattr(self.rhs, 'eval'):
            return self.rhs.eval(self.t.new_result.object)
        else:
            return self.rhs
        # # if self.result is None:
        # assert self.result is None
        # print(over_result)
        # oi_result = self.g.compute_result(over_result)
        # ui_result = self.f.compute_result(oi_result.dom)
        # # self.result = ui_result.compose(oi_result)
        # comp = ui_result.compose(oi_result)
        # # comp.name = "(" + ui_result.name + " ; " + oi_result.name + ")"
        # self.result = comp
        # return comp
        # return self.result
    
    def __repr__(self):
        return "CompInsInc : [" + " lhs : " + str(self.lhs) + " ]"

class Result():
    def __init__(self, obj, is_rhs):
        self.object = obj
        self.is_rhs = is_rhs
        self.obs_by = []
    
    @staticmethod
    def multi_merge_2(lm, CD): # TODO remove this converter -> modify multi_merge
        l_new = []
        l_old = []
        res_old = None
        res_new = None
        for ins in lm:
            l_new.append(ins.new_subresult)
            l_old.append(ins.old_subresult)
            if res_old is None:
                res_old = ins.old_result
            if res_new is None:
                res_new = ins.new_result
        return Result.multi_merge(l_old, l_new, res_old, res_new, CD)
    
    @staticmethod
    def multi_merge(l_old, l_new, res_old, res_new, CD):
        if len(l_old) == 0:
            return [], []
        if res_old.is_rhs:
            assert res_new.is_rhs
            obj, on_old, on_new = CD.multi_merge(l_old, l_new)
            res = Result(obj, False)
            for ins in res_old.obs_by:
                # print(type(ins.new_result.object), type(ins.old_result.object), type(res_old.object))
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
