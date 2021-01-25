import networkx as nx
from .Memory import Instance, InstanceInc

class FlatPFunctor:
    class Rule:
        def __init__(self, lhs, rhs):
            self.lhs = lhs
            self.rhs = rhs
            self.self_inclusions = set()
            # self.is_small
            # self.nb_smalls 
        
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
            get_ins_inc = lambda u_ins : InstanceInc(u_inc, u_ins, ins)
            yield u_occ, get_u_ins, get_ins_inc
    
    def pmatch_up(self, ins, matches):
        for _, o_rule, o_inc in self.G.out_edges(self.l_to_r[ins.rule.lhs], keys = True):
            for o_occ in self.CS.pattern_match(o_inc.lhs, ins.occ):
                get_o_ins = lambda : Instance(o_rule, len(self.small_pred.in_edges(o_rule)), o_occ)
                get_ins_inc = lambda o_ins : InstanceInc(o_inc, ins, o_ins)
                yield o_occ, get_o_ins, get_ins_inc
    
    def iter_self_inclusions(self, ins, matches):
        rule = self.l_to_r[ins.rule.lhs]
        for inc in rule.iter_self_inclusions():
            s_occ = inc.lhs.compose(ins.occ)
            get_s_ins = lambda : Instance(rule, len(self.small_pred.in_edges(rule)), s_occ)
            get_ins_inc = lambda u_ins : InstanceInc(inc, u_ins, inc)
            yield s_occ, get_s_ins, get_ins_inc

class OPFunctor:
    class Choices:
        def __init__(self, lhs, results):
            self.results = results
            self.lhs = lhs # redundant may be removed keeped for the assert
            self.f_alpha_inv = {}
            self.f_beta = {}
            self.under = {}

        def add_under_choice(self, linc, uchoice, rincs):
            assert linc.dom == uchoice.lhs
            self.under[linc] = uchoice
            j = 0
            for rinc in rincs:
                print("j", j)
                if rinc == None:
                    continue
                assert rinc.cod in self.results
                #if rinc.dom == rinc.cod:
                #    self.f_beta[(linc, rinc.cod)] = rinc
                #else:
                self.f_beta[(linc, rinc.cod)] = rinc
                fiber = self.f_alpha_inv.setdefault(linc, {})
                rfiber = fiber.setdefault(rinc.dom, [])
                rfiber.append(rinc.cod)
                print("------")
                print(rinc, rinc.name if rinc.name != None else None)
                # self.checkChoices(self)
                j+=1

        @staticmethod
        def checkChoices(ch):
            for li, unc in ch.under.items():
                if unc == ch:
                    continue
                print("li", li)
                i = 0
                for unr in unc.results:
                    print(" i : ", i)
                    # print(ch.f_alpha_inv)
                    if unr in ch.f_alpha_inv[li]:
                        for upr in ch.f_alpha_inv[li][unr]:
                            m = ch.f_beta[(li, upr)]
                            print(m.dom, unr, m.name)
                            assert m.dom == unr
                    i += 1
            

    class ORule:
        def __init__(self, lhs, rhs_choice, rhs_run):
            self.lhs = lhs
            self.rhs_choice = rhs_choice
            self.rhs_run = rhs_run
            self.self_inclusions = set()
        
        def __eq__(self, other):
            if not isinstance(other,OPFunctor.ORule):
                return False
            return self.lhs == other.lhs

        def __hash__(self):
            return hash(self.lhs)

        def __repr__(self):
            return str(self.lhs) + " => " + str(self.rhs_choice)

        def iter_self_inclusions(self):
            yield from self.self_inclusions

    class OInclusion():
        def __init__(self, g_a, g_b, lhs):
            self.g_a = g_a
            self.g_b = g_b
            self.lhs = lhs

        def __eq__(self, other):
            if not isinstance(other, OPFunctor.OInclusion):
                return False
            return self.lhs == other.lhs

        def __hash__(self):
            return hash(self.lhs)

        def __repr__(self):
            return str(self.lhs) + ' => ...' #+ str(self.rhs)

    class Maker():
        def __init__(self, CS, LCD):
            self.CS = CS
            self.CD = LCD
            self.l_to_r = {}
            self.G = nx.MultiDiGraph()

        def add_o_rule(self, l, rc, rr):
            rule = OPFunctor.ORule(l, rc, rr)
            self.G.add_node(rule)
            self.l_to_r[l] = rule
            return rule

        def add_o_inclusion(self, g_a, g_b, l):
            inc = OPFunctor.OInclusion(g_a, g_b, l)
            if g_a == g_b:
                g_a.self_inclusions.add(inc)
            else:
                self.G.add_edge(g_a, g_b, key = inc)
            return (g_a, g_b, inc)

        def get(self):
            return OPFunctor(self.CS, self.CD, self.G, self.l_to_r)

    def __init__(self, CS, CD, G, l_to_r):
        self.CS = CS
        self.CD = CD
        self.G = G
        self.l_to_r = l_to_r
        self.smalls = set()
        self.small_pred = nx.MultiDiGraph()
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

    class RuleInst:
        def __init__(self, o_rule, auto = None):
            self.o_rule = o_rule
            self.lhs = o_rule.lhs
            self.incs_in = { linc : None for linc in o_rule.rhs_choice.under if linc.dom != o_rule.lhs }
            self.r = None
            self.auto = auto

        def get_rhs(self):
            return self.rhs()
        
        def rhs(self):
            if self.r != None:
                return self.r
            else:
                if self.auto == None:
                    # print("incs_in", self.incs_in)
                    # print(self.o_rule.rhs_choice.under)
                    self.r = self.o_rule.rhs_run(self.o_rule.rhs_choice, self.incs_in)
                    # print(self.incs_in)
                    # print("got ", self.r)
                    # DEBUG CHECK !
                    # for i in self.incs_in.items():
                    #     print(i)
                    for linc, incinst in self.incs_in.items():
                        # print(linc, incinst)
                        # print(incinst.g_a.rhs())
                        # print(self.o_rule.rhs_choice.f_alpha_inv[incinst.g_a.rhs()])
                        # print("rkfjg", type(self.o_rule.rhs_choice.f_alpha_inv[incinst.lhs][incinst.g_a.rhs()]))
                        # print(self.r)
                        # print(self.o_rule.rhs_choice.f_alpha_inv[incinst.lhs][incinst.g_a.rhs()])
                        assert self.r in self.o_rule.rhs_choice.f_alpha_inv[incinst.lhs][incinst.g_a.rhs()]
                    return self.r
                else:
                    incl, over_rule = self.auto 
                    self.r = over_rule.rhs().restrict(over_rule.o_rule.rhs_choice.f_beta[(incl, over_rule.rhs())]).dom # SHOUD be a equal to the over rhs or this rhs must have been specified in the choices
                    return self.r

        def __eq__(self, other):
            if not isinstance(other,OPFunctor.RuleInst):
                return False
            return self.lhs == other.lhs and self.r == other.r

        def __hash__(self):
            return hash(self.lhs)

        def __repr__(self):
            return str(self.lhs)# + " => " + str(self.rhs)

    class InclusionInst():
        def __init__(self, o_inc, g_a, g_b, auto = False):
            self.o_inc = o_inc
            self.g_a = g_a
            self.g_b = g_b
            self.lhs = o_inc.lhs
            self.r = None
            self.auto = auto
            if not auto:
                assert self.g_b.incs_in[self.lhs] == None
                self.g_b.incs_in[self.lhs] = self
        
        def get_rhs(self):
            return self.rhs()

        def rhs(self):
            # print("called")
            if self.r != None:
                return self.r
            else:
                # print(type(self.lhs), type(self.g_b.rhs))
                self.r = self.g_b.o_rule.rhs_choice.f_beta[(self.lhs, self.g_b.rhs())]
                return self.r

        def __repr__(self):
            return str(self.lhs)# + " => " + str(self.rhs)

    def is_small(self, ins):
        return self.l_to_r[ins.rule.lhs] in self.smalls

    def nb_small(self, ins):
        return len(self.small_pred.in_edges(self.l_to_r[ins.rule.lhs]))

    def next_small(self, X):
        for small_o_rule in self.smalls:
            for small_match in self.CS.pattern_match(small_o_rule.lhs, X):
                small_match.clean()
                small_rule = self.RuleInst(small_o_rule)
                get_s_ins = lambda : Instance(small_rule, len(self.small_pred.in_edges(small_o_rule)), small_match)
                yield get_s_ins

    def iter_under(self, ins, matches):
        for u_o_rule, _, u_o_inc in self.G.in_edges(self.l_to_r[ins.rule.lhs], keys = True):
            # u_rule = self.RuleInst(u_o_rule)
            # u_inc = self.InclusionInst(u_o_inc, u_rule, rule)
            u_occ = u_o_inc.lhs.compose(ins.occ)
            # if u_occ not in matches:
            def get_u_ins():
                u_rule = self.RuleInst(u_o_rule)
                return Instance(u_rule, len(self.small_pred.in_edges(u_o_rule)), u_occ)
            get_ins_inc = lambda u_ins : InstanceInc(self.InclusionInst(u_o_inc, u_ins.rule, ins.rule), u_ins, ins)
            yield u_occ, get_u_ins, get_ins_inc
            # else:
            #     # print("RECOVERED RULEINST under")
            #     u_ins = matches[u_occ]
            #     u_rule = u_ins.rule
            #     get_u_ins = lambda : u_ins
            #     get_ins_inc = lambda u_ins : InstanceInc(self.InclusionInst(u_o_inc, u_rule, ins.rule), u_ins, ins)
            #     yield u_occ, get_u_ins, get_ins_inc

    def pmatch_up(self, ins, matches):
        for _, over_o_rule, inc_o in self.G.out_edges(self.l_to_r[ins.rule.lhs], keys = True):
            for over_occ in self.CS.pattern_match(inc_o.lhs, ins.occ):
                # if over_occ in matches: # redundant check with GT_DU
                #     # print("RECOVERED RULEINST up")
                #     over_ins = matches[over_occ]
                #     over_rule = over_ins.rule
                #     get_o_ins = lambda : over_ins
                #     get_ins_inc = lambda o_ins : InstanceInc(self.InclusionInst(inc_o, ins.rule, over_rule), ins, o_ins)
                #     yield over_occ, get_o_ins, get_ins_inc
                # else:
                def get_o_ins():
                    over_rule = self.RuleInst(over_o_rule)
                    return Instance(over_rule, len(self.small_pred.in_edges(over_o_rule)), over_occ)
                get_ins_inc = lambda o_ins : InstanceInc(self.InclusionInst(inc_o, ins.rule, o_ins.rule), ins, o_ins)
                yield over_occ, get_o_ins, get_ins_inc

    def iter_self_inclusions(self, ins, matches):
        for inc_o in ins.rule.o_rule.iter_self_inclusions():
            s_occ = inc_o.lhs.compose(ins.occ)
            # if s_occ not in matches:
            def get_s_ins():
                self_rule = self.RuleInst(ins.rule.o_rule, (inc_o.lhs, ins.rule))
                return Instance(self_rule, len(self.small_pred.in_edges(self_rule.o_rule)), s_occ)
            get_ins_inc = lambda u_ins : InstanceInc(self.InclusionInst(inc_o, u_ins.rule, ins.rule, True), u_ins, ins)
            yield s_occ, get_s_ins, get_ins_inc
            # else:
            #     # print("RECOVERED RULEINST self")
            #     self_ins = matches[s_occ]
            #     self_rule = self_ins.rule
            #     get_s_ins = lambda : self_ins
            #     get_ins_inc = lambda u_ins : InstanceInc(self.InclusionInst(inc_o, self_rule, ins.rule, True), u_ins, ins)
            #     yield s_occ, get_s_ins, get_ins_inc

    