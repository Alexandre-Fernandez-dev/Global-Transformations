class Instance():
    def __init__(self, rule, occ): # privé à GT
        self.stared = False
        self.closed = False
        self.rule = rule
        self.nb_dep = rule.cunder
        self.istop = False
        # print("init nbdep", self.nb_dep)
        self.occ = occ          # C[rule.lhs, X]
        self.overins = []
    
    def decrNbDep(self): # privé à GT ?
        self.nb_dep -= 1
        if self.nb_dep <= 0:
            return True # should remove ins
        return False

    def __repr__(self):
        return "Instance : [" + " occ : " + str(self.occ) + "]"

class InstanceInc():
    def get_lhs(self):
        pass

    def get_rhs(self):
        pass
    
    def __repr__(self):
        pass

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

class Result():
    @staticmethod
    def multi_merge_2(lm, uins_rhs, uins_col, CD, in_place):
        # TODO remove
        # CONVERTER
        uins_res = {}
        l_rhs = []
        l_col = []
        res_col = None
        res_rhs = None
        for ins in lm:
            l_rhs.append(uins_rhs[ins])
            l_col.append(uins_col[ins])
            if res_rhs is None:
                res_rhs = uins_rhs[ins].cod #ins.rhs_result
            if res_col is None:
                res_col = uins_col[ins].cod

        # END CONVERTER
        if len(l_col) == 0:
            return [], []
        if not in_place:
            obj, on_col, on_rhs = CD.multi_merge(l_col, l_rhs)
            res = obj
            for ins in uins_col.keys():
                #TODO identity None
                uins_res[ins] = on_col if uins_col[ins] is None else uins_col[ins].compose(on_col)
            res_col.obs_by = None
            res_col.object = None
        else:
            res = res_col
            obj, on_rhs = CD.multi_merge_2_in_1(l_col, l_rhs)
        for ins in uins_rhs.keys():
            uins_res[ins] = on_rhs if uins_rhs[ins] is None else uins_rhs[ins].compose(on_rhs)
        res_rhs.obs_by = None
        res_rhs.object = None
        return res, uins_res
