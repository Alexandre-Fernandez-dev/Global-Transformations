import networkx as nx
from .Memory import Instance, PrimeInstanceInc

class FlatPFunctor:
    class Rule:
        def __init__(self, lhs, rhs):
            self.lhs = lhs
            self.rhs = rhs
            self.cunder = 0
            self.self_inclusions = set()
        
        def get_rhs(self):
            return self.rhs

        def __eq__(self, other):
            if not isinstance(other,FlatPFunctor.Rule):
                return False
            return self.lhs == other.lhs

        def __hash__(self):
            return hash(self.lhs)

        def __repr__(self):
            return str(self.lhs) + " => " + str(self.rhs)

        def iter_self_inclusions(self):
            for i in self.self_inclusions:
                yield i

    class Inclusion:
        def __init__(self, g_a, g_b, lhs, rhs):
            self.g_a = g_a
            self.g_b = g_b
            self.lhs = lhs
            self.rhs = rhs

        def get_rhs(self):
            return self.rhs

        def __eq__(self, other):
            if not isinstance(other, FlatPFunctor.Inclusion):
                return False
            return self.lhs == other.lhs

        def __hash__(self):
            return hash(self.lhs)

        def __repr__(self):
            return str(self.lhs) + ' => ...' #+ str(self.rhs)

    class Maker():
        def __init__(self, CS, CD):
            self.CS = CS
            self.CD = CD
            self.G = nx.MultiDiGraph()

        def add_rule(self, l, r):
            rule = FlatPFunctor.Rule(l, r)
            self.G.add_node(rule)
            return rule

        def add_inclusion(self, g_a, g_b, l, r):
            inc = FlatPFunctor.Inclusion(g_a, g_b, l, r)
            if g_a == g_b:
                assert l.dom == g_a.lhs
                g_a.self_inclusions.add(inc)
            else:
                g_b.cunder += 1
                self.G.add_edge(g_a, g_b, key = inc)
            return (g_a, g_b, inc)

        def get(self):
            return FlatPFunctor(self.CS, self.CD, self.G)
        
    def __init__(self, CS, CD, G):
        self.CS = CS
        self.CD = CD
        self.G = G
        self.smalls = set()
        self.small_pred = nx.MultiDiGraph()
        # replace by union find like datastructure or set ?
        def f(g): # TODO replace by smaller function that only computes nb_small
            if g in self.small_pred.nodes():
                return [ r for _, _, r in self.small_pred.in_edges(g, keys = True) ]
            self.small_pred.add_node(g)
            l = []
            for s, _, _ in self.G.in_edges(g, keys = True):
                r = f(s)
                if r == []:
                    l.append(s)
                else:
                    l = l + [ sp for sp in r ]
            if l == []:
                self.smalls.add(g)
            for s in l:
                self.small_pred.add_edge(s, g, None)
            return l
        for g in self.G.nodes:
            f(g)
    
    def is_small(self, ins): # could be a bool in ins
        return ins.rule in self.smalls

    def nb_small(self, ins): # could be a bool in ins
        return len(self.small_pred.in_edges(ins.rule))

    def next_small(self, X):
        for small_rule in self.smalls:
            for small_match in self.CS.pattern_match(small_rule.lhs, X):
                small_match.clean()
                get_s_ins = lambda : Instance(small_rule, small_match)
                yield get_s_ins
    
    def iter_under(self, ins):
        for u_rule, _, u_inc in self.G.in_edges(ins.rule, keys = True):
            u_occ = u_inc.lhs.compose(ins.occ)
            get_u_ins = lambda : Instance(u_rule, u_occ)
            get_ins_inc = lambda u_ins : PrimeInstanceInc(u_inc, u_ins, ins)
            yield u_occ, get_u_ins, get_ins_inc
    
    def pmatch_up(self, ins):
        for _, o_rule, o_inc in self.G.out_edges(ins.rule, keys = True):
            for o_occ in self.CS.pattern_match(o_inc.lhs, ins.occ):
                get_o_ins = lambda : Instance(o_rule, o_occ)
                get_ins_inc = lambda o_ins : PrimeInstanceInc(o_inc, ins, o_ins)
                yield o_occ, get_o_ins, get_ins_inc
    
    def iter_self_inclusions(self, ins):
        rule = ins.rule
        for inc in rule.iter_self_inclusions():
            s_occ = inc.lhs.compose(ins.occ)
            get_s_ins = lambda : Instance(rule, s_occ)
            get_ins_inc = lambda u_ins : PrimeInstanceInc(inc, u_ins, ins)
            yield s_occ, get_s_ins, get_ins_inc

class FamPFunctor:
    class FamRule:
        def __init__(self, lhs, rhs):
            self.lhs = lhs
            self.rhs = rhs
            self.cunder = 0
            self.self_fam_inclusions = set()

        def __eq__(self, other):
            if not isinstance(other,FamPFunctor.FamRule):
                return False
            return self.lhs == other.lhs

        def __hash__(self):
            return hash(self.lhs)

        def __repr__(self):
            return str(self.lhs) + " as X => (lambda X -> ...)"

        def iter_self_inclusions(self):
            for i in self.self_fam_inclusions:
                yield i

    class FamInclusion:
        def __init__(self, g_a, g_b, lhs, rhs):
            self.g_a = g_a
            self.g_b = g_b
            self.lhs = lhs
            self.rhs = rhs

        def __eq__(self, other):
            if not isinstance(other, FamPFunctor.FamInclusion):
                return False
            return self.lhs == other.lhs

        def __hash__(self):
            return hash(self.lhs)

        def __repr__(self):
            return str(self.lhs) + ' => (lambda S T -> ...)'

        def compose(self, other):
            def rhs(lps, lpo, rs, ro):
                lpm = lpo.restrict(other.lhs).dom
                rm = self.g_b.rhs(lpm)
                return self.rhs(lps, lpm, rs, rm).compose(other.rhs(lpm, lpo, rm, ro))
            return FamPFunctor.FamInclusion(self.g_a, other.g_b, self.lhs.compose(other.lhs), rhs)

    class Maker():
        def __init__(self, CS, CD):
            self.CS = CS
            self.CD = CD
            self.G = nx.MultiDiGraph()

        def add_fam_rule(self, l, r):
            rule = FamPFunctor.FamRule(l, r)
            self.G.add_node(rule)
            return rule

        def add_fam_inclusion(self, g_a, g_b, l, r):
            inc = FamPFunctor.FamInclusion(g_a, g_b, l, r)
            if g_a == g_b:
                g_a.self_fam_inclusions.add(inc)
            else:
                g_b.cunder += 1
                self.G.add_edge(g_a, g_b, key = inc)
            return (g_a, g_b, inc)

        def get(self):
            return FamPFunctor(self.CS, self.CD, self.G)

    def __init__(self, CS, CD, G):
        self.CS = CS
        self.CD = CD
        self.G = G
        self.smalls = set()
        self.small_pred = nx.MultiDiGraph()
        def f(g):
            if g in self.small_pred.nodes():
                return [ r for _, _, r in self.small_pred.in_edges(g, keys = True) ]
            self.small_pred.add_node(g)
            l = []
            for s, _, inc in self.G.in_edges(g, keys = True):
                r = f(s)
                if r == []:
                    l.append(inc)
                else:
                    l = l + [ incp.compose(inc) for incp in r ]
            if l == []:
                self.smalls.add(g)
            for inc in l:
                self.small_pred.add_edge(inc.g_a, g, inc)
            return l
        for g in self.G.nodes:
            f(g)

    #TODO rewrite
    class Rule:
        def __init__(self, fam_rule, lp):
            assert fam_rule.lhs == lp.naked()
            self.fam = fam_rule
            self.cunder = fam_rule.cunder
            self.lhs = lp
            self.rhs = fam_rule.rhs(lp)
        
        def get_rhs(self, underincs):
            if hasattr(self.rhs, 'eval'):
                return self.rhs.eval(underincs)
            return self.rhs

        def __eq__(self, other):
            if not isinstance(other, FamPFunctor.Rule):
                return False
            return self.fam == other.fam and self.lhs == other.lhs

        def __hash__(self):
            return hash(self.fam) ^ 31 * hash(self.lhs)

        def __repr__(self):
            return "r(fam : " + str(self.fam) + ", lhs " + str(self.lhs) + ", rhs " + str(self.rhs) + ")"

    #TODO rewrite
    class Inclusion:
        def __init__(self, fam_inc, g_a, g_b, lhs):
            assert fam_inc.lhs == lhs.naked()
            self.fam = fam_inc
            self.g_a = g_a
            self.g_b = g_b
            self.lhs = lhs
            self.rhs = fam_inc.rhs(g_a.lhs, g_b.lhs, g_a.rhs, g_b.rhs)

        def get_rhs(self, over_rhs):
            if hasattr(self.rhs, 'eval'):
                return self.rhs.eval(over_rhs)
            return self.rhs

        def __eq__(self, other):
            if not isinstance(other, FamPFunctor.Inclusion):
                return False
            return self.fam == other.fam and self.g_a == other.g_a and self.g_b == other.g_b and self.lhs == other.lhs

        def __hash__(self):
            return hash(self.fam) ^ 31 * hash(self.lhs) ^ 31 * hash(self.g_a) ^ 31 * hash(self.g_b)

        def __repr__(self):
            return "i(fam: " + str(self.fam) + ", g_a " + str(self.g_a) + " g_b " + str(self.g_b) + ", lhs " + str(self.lhs) + ", rhs " + str(self.rhs) + ")"

    def is_small(self, ins): # could be a bool in ins
        return ins.rule.fam in self.smalls

    def nb_small(self, ins):
        return len(self.small_pred.in_edges(ins.rule.fam))

    def next_small(self, X):
        for small_rule_fam in self.smalls:
            for small_occ in self.CS.pattern_match(small_rule_fam.lhs, X):
                small_occ.clean()
                small_rule = self.Rule(small_rule_fam, small_occ.dom)
                get_s_ins = lambda : Instance(small_rule, small_occ)
                yield get_s_ins

    def iter_under(self, ins):
        for u_rule_fam, _, u_inc_fam in self.G.in_edges(ins.rule.fam, keys=True):
            u_inc_lhs = ins.rule.lhs.restrict(u_inc_fam.lhs)
            u_occ = u_inc_lhs.compose(ins.occ)
            def get_u_ins():
                u_rule = self.Rule(u_rule_fam, u_inc_lhs.dom)
                return Instance(u_rule, u_occ)
            def get_ins_inc(u_ins):
                u_inc = self.Inclusion(u_inc_fam, u_ins.rule, ins.rule, u_inc_lhs)
                return PrimeInstanceInc(u_inc, u_ins, ins)
            yield u_occ, get_u_ins, get_ins_inc

    def pmatch_up(self, ins):
        for _, o_rule_fam, o_inc_fam in self.G.out_edges(ins.rule.fam, keys = True):
            for o_occ in self.CS.pattern_match(o_inc_fam.lhs, ins.occ):
                def get_o_ins():
                    o_rule = self.Rule(o_rule_fam, o_occ.dom)
                    return Instance(o_rule, o_occ)
                def get_ins_inc(o_ins):
                    o_inc_lhs = o_ins.rule.lhs.restrict(o_inc_fam.lhs)
                    o_inc = self.Inclusion(o_inc_fam, ins.rule, o_ins.rule, o_inc_lhs)
                    return PrimeInstanceInc(o_inc, ins, o_ins)
                yield o_occ, get_o_ins, get_ins_inc
    
    def iter_self_inclusions(self, ins):
        for s_inc_fam in ins.rule.fam.iter_self_inclusions():
            s_inc_lhs = ins.rule.lhs.restrict(s_inc_fam.lhs)
            s_occ = s_inc_lhs.compose(ins.occ)
            def get_s_ins():
                s_rule = self.Rule(ins.rule.fam, s_occ.dom)
                return Instance(s_rule, s_occ)
            def get_ins_inc(s_ins):
                s_inc = self.Inclusion(s_inc_fam, s_ins.rule, ins.rule, s_inc_lhs)
                return PrimeInstanceInc(s_inc, s_ins, ins)
            yield s_occ, get_s_ins, get_ins_inc
