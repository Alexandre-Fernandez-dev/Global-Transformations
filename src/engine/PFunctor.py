import networkx as nx
from .Memory import Instance, PrimeInstanceInc

class FlatPFunctor:
    class Rule:
        def __init__(self, lhs, rhs):
            self.lhs = lhs
            self.rhs = rhs
            self.self_inclusions = set()
        
        def get_rhs(self, underincs):
            if hasattr(self.rhs, 'eval'):
                return self.rhs.eval(underincs)
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

        def get_rhs(self, over_rhs):
            if hasattr(self.rhs, 'eval'):
                return self.rhs.eval(over_rhs)
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
            self.l_to_r = {}
            self.G = nx.MultiDiGraph()

        def add_rule(self, l, r):
            rule = FlatPFunctor.Rule(l, r)
            self.G.add_node(rule)
            self.l_to_r[l] = rule
            return rule

        def add_inclusion(self, g_a, g_b, l, r):
            inc = FlatPFunctor.Inclusion(g_a, g_b, l, r)
            if g_a == g_b:
                g_a.self_inclusions.add(inc)
            else:
                self.G.add_edge(g_a, g_b, key = inc)
            return (g_a, g_b, inc)

        def get(self):
            return FlatPFunctor(self.CS, self.CD, self.G, self.l_to_r)
        
    def __init__(self, CS, CD, G, l_to_r):
        self.CS = CS
        self.CD = CD
        self.G = G
        self.l_to_r = l_to_r
        self.smalls = set()
        self.small_pred = nx.MultiDiGraph()
        # replace by union find like datastructure or set ?
        def f(g): # TODO replace by smaller function that only computes nb_small
            if g in self.small_pred.nodes():
                return [ r for _, _, r in self.small_pred.in_edges(g, keys = True) ]
            self.small_pred.add_node(g)
            l = []
            for s, _, inc in self.G.in_edges(g, keys = True):
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
        return self.l_to_r[ins.rule.lhs] in self.smalls

    def nb_small(self, ins): # could be a bool in ins
        return len(self.small_pred.in_edges(self.l_to_r[ins.rule.lhs]))

    def next_small(self, X):
        for small_rule in self.smalls:
            for small_match in self.CS.pattern_match(small_rule.lhs, X):
                small_match.clean()
                get_s_ins = lambda : Instance(small_rule, len(self.small_pred.in_edges(small_rule)), small_match)
                yield get_s_ins
    
    def iter_under(self, ins, matches):
        for u_rule, _, u_inc in self.G.in_edges(self.l_to_r[ins.rule.lhs], keys = True):
            u_occ = u_inc.lhs.compose(ins.occ)
            get_u_ins = lambda : Instance(u_rule, len(self.small_pred.in_edges(u_rule)), u_occ)
            get_ins_inc = lambda u_ins : PrimeInstanceInc(u_inc, u_ins, ins)
            yield u_occ, get_u_ins, get_ins_inc
    
    def pmatch_up(self, ins, matches):
        for _, o_rule, o_inc in self.G.out_edges(self.l_to_r[ins.rule.lhs], keys = True):
            for o_occ in self.CS.pattern_match(o_inc.lhs, ins.occ):
                get_o_ins = lambda : Instance(o_rule, len(self.small_pred.in_edges(o_rule)), o_occ)
                get_ins_inc = lambda o_ins : PrimeInstanceInc(o_inc, ins, o_ins)
                yield o_occ, get_o_ins, get_ins_inc
    
    def iter_self_inclusions(self, ins, matches):
        rule = self.l_to_r[ins.rule.lhs]
        for inc in rule.iter_self_inclusions():
            s_occ = inc.lhs.compose(ins.occ)
            get_s_ins = lambda : Instance(rule, len(self.small_pred.in_edges(rule)), s_occ)
            get_ins_inc = lambda u_ins : PrimeInstanceInc(inc, u_ins, inc)
            yield s_occ, get_s_ins, get_ins_inc