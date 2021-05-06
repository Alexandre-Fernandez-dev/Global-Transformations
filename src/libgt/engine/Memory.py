class Instance():
    """
    Represents an instance, ie. a match of a lhs in the object to rewrite

    Attributes
    ----------
    stared : bool
        the star function of the engine have been finished over this instance
    closed : bool
        the close function of the engine have been finished over this instance
    rule : Rule
        the associated rule
    nb_dep : int
        the number of direct subrules under this instance
    overins : List[Instance]
        the list of known instances directly over this instance
    
    Methods
    ----------
    decrNbDep(): bool
        called when one of his minimal sub-instances have been fully processed
        the boolean return says this insance can be remove from memory
    """
    def __init__(self, rule, occ): # privé à GT
        self.stared = False
        self.closed = False
        self.rule = rule
        self.nb_dep = rule.cunder
        self.occ = occ          # C[rule.lhs, X]
        self.overins = []
    
    def decrNbDep(self):
        self.nb_dep -= 1
        if self.nb_dep <= 0:
            return True
        return False

    def __repr__(self):
        return "Instance : [" + " occ : " + str(self.occ) + "]"

class InstanceInc:
    """
    Represents the inclusion between two instances

    Attributes
    ----------
    s : Instance
        the source instance
    t : Instance
        the target instance

    Methods
    ----------
    get_lhs(): CS.TM()
        get the inclusion between the lhs of the instances
    get_rhs(): CS.TM()
        get the inclusion between the rhs of the instances
    """
    def __init__(self, rule_inc, s, t):
        self.rule_inc = rule_inc
        self.s = s
        self.t = t
    
    def get_lhs(self):
        return self.rule_inc.lhs
    
    def get_rhs(self):
        return self.rule_inc.rhs

    def __repr__(self):
        return "InstanceInc : [" + " lhs : " + str(self.rule_inc.lhs) + " ]"

class Result():
    """
    Static Methods
    ----------
    multi_merge_2(lm, uins_rhs, uins_col, CD, in_place): (CD.TO(), Dict[Instance, CD.TM()])
        compute the generalizedPushout of all spans in lm
        lm is a list of spans
        uins_rhs contains all arrows to the new rhs
        uins_col contains all arrows (cocone) to the old colimit
        CD is the datastructure of destination used to compute the generalizedpushout
        in_place says if the old result should be directly modified (vs a copy)
        the first return is the new result computed
        the second return is the cocone from the instances to the new result
    """
    @staticmethod
    def multi_merge_2(lm, uins_rhs, uins_col, CD, in_place):
        # TODO REMOVE CONVERTER
        uins_res = {}
        l_rhs = []
        l_col = []
        res_col = None
        res_rhs = None
        for ins in lm:
            l_rhs.append(uins_rhs[ins])
            l_col.append(uins_col[ins])
            if res_rhs is None:
                res_rhs = uins_rhs[ins].cod
            if res_col is None:
                res_col = uins_col[ins].cod

        # END CONVERTER
        if len(l_col) == 0:
            return [], []
        if not in_place:
            obj, on_col, on_rhs = CD.multi_merge(l_col, l_rhs)
            res = obj
            for ins in uins_col.keys():
                uins_res[ins] = uins_col[ins].compose(on_col)
        else:
            res = res_col
            obj, on_rhs = CD.multi_merge_2_in_1(l_col, l_rhs)
        for ins in uins_rhs.keys():
            uins_res[ins] = uins_rhs[ins].compose(on_rhs)
        return res, uins_res
