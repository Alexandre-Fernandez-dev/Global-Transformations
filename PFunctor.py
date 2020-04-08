import networkx as nx

class PFunctor:
    def nb_small(self, rule):
        pass

    def iter_small(self, rule):
        pass

    def iter_under(self, rule):
        pass

    def pmatch_up(self, rule, match):
        pass

    def iter_self_inclusions(self, rule):
        pass

    def next_small(self, X):
        pass


class FlatPFunctor(PFunctor):
    """
    Attributes
    ----------
    CS : DataStructure (TODO use Datatype/DataStructure as category)
        the source Datatype

    CD : DataStructure
        the destination Datatype

    G : nx.MultiDiGraph
        the MultiDiGraph of the rules and rules inclusions of the GT

    smalls : Set
        the set of bottom rules

    small_pred : nx.MultiDiGraph (TODO hide ?)
        the graph associating to each rule the bottom rules under it

    Methods
    -------
    add_rule(l, r)
        add a new rule with lhs l and rhs r in G and returns it

    add_inclusion(g_a, g_b, l, r)
        add a new rule inclusion from g_a to g_b with l the inclusion of lhs and r the inclusion of rhs

    compute_small_rules(g) (TODO hide ?)
        initialize small_pred for the given rule g
    """

    class Rule:
        """
        A rule of a global transformation.

        Attributes
        ----------
        lhs : ??.Object
            the left hand side of the rule
        rhs : ??.Object
            the right hand side of the rule
        self_inclusions : Inclusion
            inclusions of the rule in itself (automorphisms)
        """

        def __init__(self, lhs, rhs):
            """
            Parameters
            ----------
            lhs : ??.Object
                the left hand side of the rule
            rhs : ??.Object
                the right hand side of the rule
            """

            self.lhs = lhs
            self.rhs = rhs
            self.self_inclusions = set()

        def __eq__(self, other):
            """
            Parameters
            ----------
            other : Rule
                an other rule
            """

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

    class Inclusion():
        """
        A rule inclusion

        Attributes
        ----------
        g_a : Rule
            source rule
        g_b : Rule
            destination rule
        lhs : ??.Morphism
            a morphism that includes g_a.lhs in g_b.lhs
        rhs : ??.Morphism
            a morphism that includes g_a.rhs in g_b.rhs

        Methods
        -------
        compose(other)
            composes the inclusion with the other inclusions if domain and codomains matches (TODO self . other or other . self)
        """

        def __init__(self, g_a, g_b, lhs, rhs):
            self.g_a = g_a
            self.g_b = g_b
            self.lhs = lhs
            self.rhs = rhs

        def __eq__(self, other):
            if not isinstance(other, FlatPFunctor.Inclusion):
                return False
            return self.lhs == other.lhs

        def __hash__(self):
            return hash(self.lhs)

        def __repr__(self):
            return str(self.lhs) + ' => ...' #+ str(self.rhs)

        def compose(self, other):
            """
            composes the inclusion with the other inclusions if domain and codomains matches (TODO self . other or other . self)

            Parameters
            ----------
            other : Inclusion
                an other inclusion with matching domain (TODO ?)

            Returns
            -------
            Inclusion
                the composition

            """
            return FlatPFunctor.Inclusion(self.g_a, other.g_b, self.lhs.compose(other.lhs), self.rhs.compose(other.rhs))

    class Maker():
        def __init__(self, CS, CD):
            self.CS = CS
            self.CD = CD
            self.G = nx.MultiDiGraph()

        def add_rule(self, l, r):
            """
            creates and add a new rule with lhs l and rhs r in G and returns it

            Parameters
            ----------
            l : CS.O
                the left hand side of the rule

            r : CD.O
                the right hand side of the rule

            Returns
            -------
            Rule
                the new rule
            """
            rule = FlatPFunctor.Rule(l, r)
            self.G.add_node(rule)
            return rule

        def add_inclusion(self, g_a, g_b, l, r):
            """
            creates and add a new inclusion of rules from g_a to g_b and returns it

            Parameters
            ----------
            g_a : Rule
                the source rule

            g_b : Rule
                the destination rule

            l : CS.M
                the inclusions of the left hand sides g_a.lhs -> g_b.lhs

            r : CD.M
                the inclusions of the right hand sides g_a.rhs -> g_b.rhs

            Returns
            -------
            Inclusion
                the new inclusion
            """
            assert g_a.lhs == l.dom
            assert g_b.lhs == l.cod
            assert g_a.rhs == r.dom
            assert g_b.rhs == r.cod
            inc = FlatPFunctor.Inclusion(g_a, g_b, l, r)
            if g_a == g_b:
                g_a.self_inclusions.add(inc)
            else:
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

    def nb_small(self, rule):
        return len(self.small_pred.in_edges(rule))

    def iter_small(self, rule):
        for small_rule, _, inc in self.small_pred.in_edges(rule, keys = True):
            yield small_rule, inc.lhs

    def iter_under(self, match):
        for u_rule, _, u_inc in self.G.in_edges(match.rule, keys=True):
            yield (lambda: u_rule), (lambda _: u_inc), u_inc.lhs.compose(match.ins)

    def pmatch_up(self, match):
        for _, over_rule, inc in self.G.out_edges(match.rule, keys = True):
            # print("over_rule", over_rule)
            # print("inc", inc)
            # print()
            for over_match in self.CS.pattern_match(inc.lhs, match.ins):
                yield over_rule, over_match

    def iter_self_inclusions(self, rule):
        return rule.iter_self_inclusions()

    def next_small(self, X):
        for small_rule in self.smalls:
            for small_match in self.CS.pattern_match(small_rule.lhs, X):
                small_match.clean()
                yield small_rule, small_match


"""
  x => (fun (s: s.naked == x) -> ... s ...)

  1     =>      (fun (s: s.naked == 1) -> SequenceO([s[0] + 1]))

  0>0>1 =>      (fun (i: i.naked == 0>0>1) (s: s.naked == 0) (t: s.naked == 1) -> i)

  0>1>1 =>      (fun (i: i.naked == 0>1>1) (s: s.naked == 0) (t: s.naked == 1) -> i)

  0     =>      (fun (s: s.naked == 1) -> SequenceO([]))

"""

class FamPFunctor(PFunctor):
    class FamRule:
        def __init__(self, lhs, rhs):
            self.lhs = lhs
            self.rhs = rhs
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
                # print("COMPOSE", self.rhs(lps, lpm, rs, rm).compose(other.rhs(lpm, lpo, rm, ro)))
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

        def add_fam_inclusion(self, g_a, g_b,l, r):
            inc = FamPFunctor.FamInclusion(g_a, g_b, l, r)
            if g_a == g_b:
                g_a.self_fam_inclusions.add(inc)
            else:
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

    # dRules = {}
    # def rule(self, fam_rule, lp):
    #     if (fam_rule, lp) not in self.dRules:
    #         self.dRules[(fam_rule, lp)] = self.Rule(fam_rule, lp)
    #         # print("RULE NOT EXIST")
    #         # print(self.dRules[(fam_rule, lp)].lhs)
    #     # else:
    #     #     print("RULE ALREADY EXIST")
    #     #     print(self.dRules[(fam_rule, lp)].lhs)
    #     return self.dRules[(fam_rule, lp)]

    # dInc = {}
    # def inclusion(self, fam_inc, g_a, g_b, lhs):
    #     if (fam_inc, g_a, g_b, lhs) not in self.dInc:
    #         # print("INC NOT EXIST")
    #         self.dInc[(fam_inc, g_a, g_b, lhs)] = self.Inclusion(fam_inc, g_a, g_b, lhs)
    #         # print(self.dInc[(fam_inc, g_a, g_b, lhs)].lhs)
    #     # else:
    #     #     print("INC ALREADY EXIST")
    #     #     print(self.dInc[(fam_inc, g_a, g_b, lhs)])
    #     return self.dInc[(fam_inc, g_a, g_b, lhs)]

    class Rule:
        def __init__(self, fam_rule, lp):
            # print(fam_rule.lhs, "|||", lp.naked())
            assert fam_rule.lhs == lp.naked()
            self.fam = fam_rule
            self.lhs = lp
            self.rhs = fam_rule.rhs(lp)

        def __eq__(self, other):
            if not isinstance(other, FamPFunctor.Rule):
                return False
            return self.fam == other.fam and self.lhs == other.lhs

        def __hash__(self):
            return hash(self.fam) ^ 31 * hash(self.lhs)

        def __repr__(self):
            return "r(fam : " + str(self.fam) + ", lhs " + str(self.lhs) + ", rhs " + str(self.rhs) + ")"

    class Inclusion:
        def __init__(self, fam_inc, g_a, g_b, lhs):
            # print(fam_inc.lhs, lhs.naked())
            assert fam_inc.lhs == lhs.naked()
            self.fam = fam_inc
            self.g_a = g_a
            self.g_b = g_b
            self.lhs = lhs
            self.rhs = fam_inc.rhs(g_a.lhs, g_b.lhs, g_a.rhs, g_b.rhs)

        def __eq__(self, other):
            if not isinstance(other, FamPFunctor.Inclusion):
                return False
            return self.fam == other.fam and self.g_a == other.g_a and self.g_b == other.g_b and self.lhs == other.lhs

        def __hash__(self):
            return hash(self.fam) ^ 31 * hash(self.lhs) ^ 31 * hash(self.g_a) ^ 31 * hash(self.g_b)

        def __repr__(self):
            return "i(fam: " + str(self.fam) + ", g_a " + str(self.g_a) + " g_b " + str(self.g_b) + ", lhs " + str(self.lhs) + ", rhs " + str(self.rhs) + ")"

    def iter_self_inclusions(self, rule):
        for inc_fam in rule.fam.iter_self_inclusions():
            inc_lhs = rule.lhs.restrict(inc_fam.lhs)
            self_rule = self.Rule(rule.fam, inc_lhs.dom)
            self_inc = self.Inclusion(inc_fam, self_rule, rule, inc_lhs)
            # print()
            # print()
            # print("rule.lhs", rule.lhs)
            # print()
            # print("rule.rhs", rule.rhs)
            # print()
            # print("inc_fam.lhs", inc_fam.lhs)
            # print()
            # print("inc_lhs", inc_lhs)
            # print()
            # print("self_inc.g_a.lhs ", self_inc.g_a.lhs)
            # print()
            # print("self_inc.lhs.dom ", self_inc.lhs.dom)
            # print()
            # print("self_inc.g_b.lhs ", self_inc.g_b.lhs)
            # print()
            # print("self_inc.lhs.cod ", self_inc.lhs.cod)
            # assert self_inc.g_a.lhs == self_inc.lhs.dom
            yield self_inc

    def nb_small(self, rule):
        return len(self.small_pred.in_edges(rule.fam))

    def iter_small(self, rule):
        for small_rule_fam, _, inc_fam in self.small_pred.in_edges(rule.fam, keys = True):
            inc_lhs = rule.lhs.restrict(inc_fam.lhs)
            small_rule = self.Rule(small_rule_fam, inc_lhs.dom)
            pinclusion = self.Inclusion(inc_fam, small_rule, rule, inc_lhs)
            yield small_rule, pinclusion.lhs

    def iter_under(self, match):
        for u_rule_fam, _, u_inc_fam in self.G.in_edges(match.rule.fam, keys=True):
            u_inc_lhs = match.rule.lhs.restrict(u_inc_fam.lhs)
            u_rule = lambda: self.Rule(u_rule_fam, u_inc_lhs.dom)
            u_inc = lambda u_rule: self.Inclusion(u_inc_fam, u_rule, match.rule, u_inc_lhs)
            yield u_rule, u_inc, u_inc_lhs.compose(match.ins)

    def pmatch_up(self, match):
        for _, over_rule_fam, inc_fam in self.G.out_edges(match.rule.fam, keys = True):
            for over_match in self.CS.pattern_match(inc_fam.lhs, match.ins):
                over_rule = self.Rule(over_rule_fam, over_match.dom)
                yield over_rule, over_match

    def next_small(self, X):
        for small_rule_fam in self.smalls:
            for small_match in self.CS.pattern_match(small_rule_fam.lhs, X):
                small_match.clean()
                small_rule = self.Rule(small_rule_fam, small_match.dom)
                yield small_rule, small_match


class ExpPFunctor(PFunctor):
    class ExpRule:
        def __init__(self, lhs, rhs_exp):
            self.lhs = lhs
            self.rhs_exp = rhs_exp
            self.self_exp_inclusions = {  }

        def __eq__(self, other):
            if not isinstance(other,ExpPFunctor.ExpRule):
                return False
            return self.lhs == other.lhs

        def __hash__(self):
            return hash(self.lhs)

        def __repr__(self):
            return str(self.lhs) + " => " + str(self.rhs_exp)

        def iter_self_inclusions(self):
            # TODO
            for i in self.self_inclusions:
                yield i

    class ExpInclusion():
        def __init__(self, g_a, g_b, lhs, rhs_i):
            # rhs_i: indice de retour de g_b.rhs_exp
            self.g_a = g_a
            self.g_b = g_b
            self.lhs = lhs
            self.rhs_i = rhs_i

        def __eq__(self, other):
            if not isinstance(other, ExpPFunctor.ExpInclusion):
                return False
            return self.lhs == other.lhs

        def __hash__(self):
            return hash(self.lhs)

        def __repr__(self):
            return str(self.lhs) + ' => ...' #+ str(self.rhs)

        def compose(self, other):
            # TODO
            return ExpPFunctor.ExpInclusion(self.g_a, other.g_b, self.lhs.compose(other.lhs), None)


    class Maker():
        def __init__(self, CS, LCD):
            self.CS = CS
            self.CD = LCD
            self.G = nx.MultiDiGraph()

        def add_exp_rule(self, l, re):
            rule = ExpPFunctor.ExpRule(l, re)
            self.G.add_node(rule)
            return rule

        def add_exp_inclusion(self, g_a, g_b,l, ri):
            inc = ExpPFunctor.ExpInclusion(g_a, g_b, l, ri)
            if g_a == g_b:
                g_a.self_exp_inclusions[ri] = inc
            else:
                self.G.add_edge(g_a, g_b, key = inc)
            return (g_a, g_b, inc)

        def get(self):
            return ExpPFunctor(self.CS, self.CD, self.G)

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

    class Rule:
        def __init__(self, exp_rule, rhs):
            self.exp = exp_rule
            self.lhs = exp_rule.lhs
            self.rhs = rhs # rhs.force() if rhs.forceable() else rhs

        def __eq__(self, other):
            if not isinstance(other,ExpPFunctor.Rule):
                return False
            return self.lhs == other.lhs

        def __hash__(self):
            return hash(self.lhs)

        def __repr__(self):
            return str(self.lhs) + " => " + str(self.rhs)

    class Inclusion():
        def __init__(self, exp_inc, g_a, g_b):
            self.exp = exp_inc
            self.g_a = g_a
            self.g_b = g_b
            self.lhs = exp_inc.lhs
            self.rhs = g_b.rhs.setSubobject(exp_inc.rhs_i, g_a.rhs)
            if g_b.rhs.forceable():
                # print("force forceable")
                g_b.rhs = g_b.rhs.force()
                self.rhs = self.rhs.force()

        def __eq__(self, other):
            if not isinstance(other, ExpPFunctor.Inclusion):
                return False
            return self.lhs == other.lhs

        def __hash__(self):
            return hash(self.lhs)

        def __repr__(self):
            return str(self.lhs) + ' => ...' #+ str(self.rhs)

        def compose(self, other):
            raise Exception('Oh Fuck!')
            return NDPFunctor.Inclusion(self.g_a, other.g_b, self.lhs.compose(other.lhs), self.rhs.compose(other.rhs))


    def nb_small(self, rule):
        return len(self.small_pred.in_edges(rule.exp))

    def iter_small(self, rule):
        for small_exp_rule, _, inc_exp in self.small_pred.in_edges(rule.exp, keys = True):
            # print("force iter_small")
            small_rule = self.Rule(small_exp_rule, self.CD.TO()(small_exp_rule.rhs_exp).force())
            yield small_rule, inc_exp.lhs

    def iter_under(self, match):
        for u_exp_rule, _, u_exp_inc in self.G.in_edges(match.rule.exp, keys=True):
            # print("new rule iter_under")
            u_rule = lambda: self.Rule(u_exp_rule, self.CD.TO()(u_exp_rule.rhs_exp))
            # print(type(match.rule.rhs))
            # print("new inclusion iter_under")
            u_inc = lambda u_rule: self.Inclusion(u_exp_inc, u_rule, match.rule)
            yield u_rule, u_inc, u_exp_inc.lhs.compose(match.ins)

    def pmatch_up(self, match):
        for _, over_exp_rule, inc_exp in self.G.out_edges(match.rule.exp, keys = True):
            for over_match in self.CS.pattern_match(inc_exp.lhs, match.ins):
                # print("new rule pmatch_up")
                over_rule = self.Rule(over_exp_rule, self.CD.TO()(over_exp_rule.rhs_exp))
                yield over_rule, over_match

    def iter_self_inclusions(self, rule):
        # TODO
        return
        yield

    def next_small(self, X):
        for small_exp_rule in self.smalls:
            for small_match in self.CS.pattern_match(small_exp_rule.lhs, X):
                small_match.clean()
                # print("force next_small")
                small_rule = self.Rule(small_exp_rule, self.CD.TO()(small_exp_rule.rhs_exp).force())
                yield small_rule, small_match

class FamExpPFunctor(PFunctor):
    class FamExpRule:
        def __init__(self, lhs, rhs_fam_exp, rhs_auto):
            self.lhs = lhs
            self.rhs_fam_exp = rhs_fam_exp
            self.rhs_auto = rhs_auto
            self.self_fam_exp_inclusions = {  }

        def __eq__(self, other):
            if not isinstance(other,FamExpPFunctor.FamExpRule):
                return False
            return self.lhs == other.lhs

        def __hash__(self):
            return hash(self.lhs)

        def __repr__(self):
            return str(self.lhs) + " => " + str(self.rhs_fam_exp)

        def iter_self_inclusions(self):
            # TODO
            print(self.self_fam_exp_inclusions)
            for i in self.self_fam_exp_inclusions:
                yield self.self_fam_exp_inclusions[i]

    class FamExpInclusion():
        def __init__(self, g_a, g_b, lhs, rhs_i):
            # rhs_i: indice de retour de g_b.rhs_exp
            self.g_a = g_a
            self.g_b = g_b
            self.lhs = lhs
            self.rhs_i = rhs_i

        def __eq__(self, other):
            if not isinstance(other, FamExpPFunctor.FamExpInclusion):
                return False
            return self.lhs == other.lhs

        def __hash__(self):
            return hash(self.lhs)

        def __repr__(self):
            return str(self.lhs) + ' => ...' #+ str(self.rhs)

        # def compose(self, other):
        #     def rhs(lps, lpo, rs, ro):
        #         lpm = lpo.restrict(other.lhs).dom
        #         rm = self.g_b.rhs(lpm)            raise Exception('Oh Fuck!')
        #         # print("COMPOSE", self.rhs(lps, lpm, rs, rm).compose(other.rhs(lpm, lpo, rm, ro)))
        #         return self.rhs(lps, lpm, rs, rm).compose(other.rhs(lpm, lpo, rm, ro))
        #     return FamPFunctor.FamInclusion(self.g_a, other.g_b, self.lhs.compose(other.lhs), rhs)

        def compose(self, other):
            # TODO
            raise Exception('Oh Fuck!')
            return FamExpPFunctor.FamExpInclusion(self.g_a, other.g_b, self.lhs.compose(other.lhs), None)

    class Maker():
        def __init__(self, CS, CD):
            self.CS = CS
            self.CD = CD
            self.G = nx.MultiDiGraph()

        def add_fam_exp_rule(self, l, re, ra):
            rule = FamExpPFunctor.FamExpRule(l, re, ra)
            self.G.add_node(rule)
            return rule

        def add_fam_exp_inclusion(self, g_a, g_b, l, ri):
            inc = FamExpPFunctor.FamExpInclusion(g_a, g_b, l, ri)
            if g_a == g_b:
                g_a.self_fam_exp_inclusions[ri] = inc
            else:
                self.G.add_edge(g_a, g_b, key = inc)
            return (g_a, g_b, inc)

        def get(self):
            return FamExpPFunctor(self.CS, self.CD, self.G)

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

    class Rule:
        def __init__(self, fam_exp_rule, lp, rhs):
            # print(fam_rule.lhs, "|||", lp.naked())
            # assert fam_rule.lhs == lp.naked()
            self.fam_exp = fam_exp_rule
            self.lhs = lp
            self.rhs = rhs

        def __eq__(self, other):
            if not isinstance(other, FamExpPFunctor.Rule):
                return False
            return self.fam_exp == other.fam_exp and self.lhs == other.lhs

        def __hash__(self):
            return hash(self.fam_exp) ^ 31 * hash(self.lhs)

        def __repr__(self):
            return str(self.lhs) + " => " + str(self.rhs)
            # return "r(fam_exp : " + str(self.fam_exp) + ", lhs " + str(self.lhs) + ", rhs " + str(self.rhs) + ")"

    class Inclusion():
        def __init__(self, fam_exp_inc, g_a, g_b, lhs, auto=False):
            self.fam_exp = fam_exp_inc
            self.g_a = g_a
            self.g_b = g_b
            self.lhs = lhs
            # print("PASS", type(g_b.rhs))
            if not auto:
                print(g_b.rhs.subobjects)
                if g_b.rhs.subobjects[fam_exp_inc.rhs_i] != None:
                    # print(g_b.rhs.subobjects[fam_exp_inc.rhs_i].dom.created_from, g_a.rhs.expr)
                    # if g_b.rhs.subobjects[fam_exp_inc.rhs_i].dom.created_from == g_a.rhs.expr:
                    #     print("LOL")
                    self.rhs = g_b.rhs.subobjects[fam_exp_inc.rhs_i]
                else:
                    self.rhs = g_b.rhs.setSubobject(fam_exp_inc.rhs_i, g_a.rhs)
                # print("type self rhs", type(self.rhs))
                # if g_b.rhs.forceable():
                #     # print("force forceable")
                #     # print(g_b.lhs)
                #     g_b.rhs = g_b.rhs.force()
                #     self.rhs = self.rhs.force()
            else:
                # print(type(g_a.rhs.subobjects))
                # print(self.rhs.force())
                print("NEW AUTO INCLUSION")
                assert g_a == g_b
                self.rhs = g_b.rhs.autos[fam_exp_inc.rhs_i]
                # if g_b.rhs.forceable():
                #     print("FOOOOOOOOOOOOOOOOOOOOOOOOOOORCE")
                #     g_b.rhs = g_b.rhs.force()
                #     self.rhs = self.rhs.force()

        def __eq__(self, other):
            if not isinstance(other, FamExpPFunctor.Inclusion):
                return False
            return self.fam_exp == other.fam_exp and self.g_a == other.g_a and self.g_b == other.g_b and self.lhs == other.lhs

        # def __eq__(self, other):
        #     if not isinstance(other, FamExpPFunctor.Inclusion):
        #         return False
        #     return self.lhs == other.lhs

        def __hash__(self):
            return hash(self.fam_exp) ^ 31 * hash(self.lhs) ^ 31 * hash(self.g_a) ^ 31 * hash(self.g_b)

        # def __hash__(self):
        #     return hash(self.lhs)

        def __repr__(self):
            return "i(fam_exp: " + str(self.fam_exp) + ", g_a " + str(self.g_a) + " g_b " + str(self.g_b) + ", lhs " + str(self.lhs) + ", rhs " + str(self.rhs) + ")"

        # def compose(self, other):
        #     raise Exception('Oh Fuck!')
        #     return NDPFunctor.Inclusion(self.g_a, other.g_b, self.lhs.compose(other.lhs), self.rhs.compose(other.rhs))

    def nb_small(self, rule):
        return len(self.small_pred.in_edges(rule.fam_exp))

    def iter_small(self, rule):
        for small_rule_fam_exp, _, inc_fam_exp in self.small_pred.in_edges(rule.fam_exp, keys = True):
            inc_lhs = rule.lhs.restrict(inc_fam_exp.lhs)
            # print("force iter_small")
            small_rule = self.Rule(small_rule_fam_exp, inc_lhs.dom, self.CD.TO()(small_rule_fam_exp.rhs_fam_exp(inc_lhs.dom), small_rule_fam_exp.rhs_auto).force())
            # print("new inclusion iter_small")
            # pinclusion = self.Inclusion(inc_fam_exp, small_rule, rule, inc_lhs) FORCE TOO EARLY -> fix not so general ?
            yield small_rule, inc_lhs #pinclusion.lhs

    def iter_under(self, match):
        for u_rule_fam_exp, _, u_inc_fam_exp in self.G.in_edges(match.rule.fam_exp, keys=True):
            u_inc_lhs = match.rule.lhs.restrict(u_inc_fam_exp.lhs)
            # print("new rule iter_under")
            u_rule = lambda: self.Rule(u_rule_fam_exp, u_inc_lhs.dom, self.CD.TO()(u_rule_fam_exp.rhs_fam_exp(u_inc_lhs.dom), u_rule_fam_exp.rhs_auto))
            # print(type(match.rule.rhs))
            # print("new inclusion iter_under")
            def u_inc(u_rule):
                print("UINC ITER UNDER")
                print("u_rule")
                print(id(u_rule))
                print(u_rule)
                print("match_rule")
                print(id(match.rule))
                print(match.rule)
                return self.Inclusion(u_inc_fam_exp, u_rule, match.rule, u_inc_lhs)
            # u_inc = lambda u_rule: self.Inclusion(u_inc_fam_exp, u_rule, match.rule, u_inc_lhs)
            yield u_rule, u_inc, u_inc_lhs.compose(match.ins)

    def pmatch_up(self, match):
        for _, over_rule_fam_exp, inc_fam_exp in self.G.out_edges(match.rule.fam_exp, keys = True):
            for over_match in self.CS.pattern_match(inc_fam_exp.lhs, match.ins):
                # print("lel", over_rule_fam_exp.rhs_fam_exp(over_match.dom))
                # print("new rule pmatch_up")
                over_rule = self.Rule(over_rule_fam_exp, over_match.dom, self.CD.TO()(over_rule_fam_exp.rhs_fam_exp(over_match.dom), over_rule_fam_exp.rhs_auto))
                yield over_rule, over_match

    def next_small(self, X):
        for small_rule_fam_exp in self.smalls:
            for small_match in self.CS.pattern_match(small_rule_fam_exp.lhs, X):
                small_match.clean()
                # print("force next_small")
                small_rule = self.Rule(small_rule_fam_exp, small_match.dom, self.CD.TO()(small_rule_fam_exp.rhs_fam_exp(small_match.dom), small_rule_fam_exp.rhs_auto).force())
                yield small_rule, small_match

    def iter_self_inclusions(self, rule): # TODO check ?
        for inc_fam_exp in rule.fam_exp.iter_self_inclusions():
            print("ITER SELF INCLUSIONS", inc_fam_exp)
            inc_lhs = rule.lhs.restrict(inc_fam_exp.lhs)
            # print("new rule iter_self_inclusions")
            self_rule = self.Rule(rule.fam_exp, inc_lhs.dom, rule.rhs)
            # print("new inclusion iter_self_inclusions")
            self_inc = self.Inclusion(inc_fam_exp, self_rule, rule, inc_lhs, True)
            print("id self_rule ", id(self_rule))
            print("self_rule", self_rule)
            print("id rule ", id(rule))
            print("rule", rule)
            # print("id inc ", id(self_inc))
            yield self_inc