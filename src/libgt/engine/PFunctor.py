import networkx as nx
from .Memory import Instance, InstanceInc

class FlatPFunctor:
    """
    A class to represent the partial functor of the local rules (lhs: C => rhs: D) 

    Classes
    ----------
    Rule : Type
        Type of the rules
    Inclusion : Type
        Type of inclusions between rules
    Maker : Type
        Class to construct a FlatPFunctor

    Attributes
    ----------
    CS : Datastructure
        Source datastructure
    CD : Datastructure
        Destination datastructure
    smalls : Set[Rule]
        Set of minimal rules
    G : networkx.MultiDiGraph[Rule, Inclusion]
        Graph of rules with rule inclusions

    Methods
    ----------
    is_small(ins) : bool
        Check if an instance corresponds to a minimal rule
    next_small(X) : Iterator[Callable[[],[Instance]]
        Iterate over matches of a small rules in X
    iter_under(ins) : Iterator[CS.TM(), Callable[[],[Instance], Callable[[Instance],[InstanceInc]]
        Iterate over sub-instances under an instance
    pmatch_up(ins) : Iterator[CS.TM(), Callable[[],[Instance], Callable[[Instance],[InstanceInc]]
        Iterate over super-instances over an instance
    iter_self_inclusions(ins) : Iterator[CS.TM(), Callable[[],[Instance], Callable[[Instance],[InstanceInc]]
        Iterate over symetric instances of an instance
    """

    class Rule:
        """
        Represents a rule
        
        lhs => rhs

        Attributes
        ----------
        lhs : CS.TO()
            Left hand side object
        rhs : CD.TO()
            Right hand side object
        cunder : int
            Count the rules directly under this rule in the graph of rules
        self_inclusions : List[Inclusion]
            List of automorphisms of the rule

        Methods
        ----------
        get_rhs() : CD.TO()
            Get the right hand side of the rule
        
        iter_self_inclusions() : Generator[Inclusion]
            Iterate over automorphisms of the rule
        """
        
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

        #iterate
        def iter_self_inclusions(self):
            for i in self.self_inclusions:
                yield i

    class Inclusion:
        """
        Represents an inclusion of rules
        
        g_a => g_b

        Attributes
        ----------
        g_a : Rule
            Source rule
        g_b : Rule
            Destination rule
        lhs : CS.TM()
            Inclusion of g_a.lhs in g_b.lhs
        rhs : CD.TM()
            Inclusion of g_a.rhs in g_b.rhs

        Methods
        ----------
        get_rhs() : CD.TM()
            Get the right hand side of the inclusion
        """

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
        """
        Maker class for a FlatPFunctor

        Attributes
        ----------
        CS : Datastructure
            Source datastructure
        CD : Datastructure
            Destination datastructure
        smalls : Set[Rule]
            Set of minimal rules
        G : networkx.MultiDiGraph[Rule, Inclusion]
            Graph of rules with rule inclusions

        Methods
        ----------
        add_rule(l, r) : Rule
            Insert new rule
        add_inclusion(g_a, g_b, l, r) : (Rule, Rule, Inclusion)
            Insert new rule inclusion
        get() : FlatPFunctor
            Get the generated FlatPFunctor
        """

        def __init__(self, CS, CD):
            self.CS = CS
            self.CD = CD
            self.smalls = set()
            self.G = nx.MultiDiGraph()

        def add_rule(self, l, r):
            rule = FlatPFunctor.Rule(l, r)
            self.G.add_node(rule)
            self.smalls.add(rule)
            return rule

        def add_inclusion(self, g_a, g_b, l, r):
            inc = FlatPFunctor.Inclusion(g_a, g_b, l, r)
            if g_a == g_b:
                assert l.dom == g_a.lhs
                g_a.self_inclusions.add(inc)
            else:
                g_b.cunder += 1
                self.G.add_edge(g_a, g_b, key = inc)
                if g_b in self.smalls:
                    self.smalls.remove(g_b)
            return (g_a, g_b, inc)

        def get(self):
            return FlatPFunctor(self.CS, self.CD, self.smalls, self.G)
        
    def __init__(self, CS, CD, smalls, G):
        self.CS = CS
        self.CD = CD
        self.G = G
        self.smalls = smalls
    
    def is_small(self, ins): # could be a bool in ins
        return ins.rule in self.smalls

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
            get_ins_inc = lambda u_ins : InstanceInc(u_inc, u_ins, ins)
            yield u_occ, get_u_ins, get_ins_inc
    
    def pmatch_up(self, ins):
        for _, o_rule, o_inc in self.G.out_edges(ins.rule, keys = True):
            for o_occ in self.CS.pattern_match(o_inc.lhs, ins.occ):
                get_o_ins = lambda : Instance(o_rule, o_occ)
                get_ins_inc = lambda o_ins : InstanceInc(o_inc, ins, o_ins)
                yield o_occ, get_o_ins, get_ins_inc
    
    def iter_self_inclusions(self, ins):
        rule = ins.rule
        for inc in rule.iter_self_inclusions():
            s_occ = inc.lhs.compose(ins.occ)
            get_s_ins = lambda : Instance(rule, s_occ)
            get_ins_inc = lambda u_ins : InstanceInc(inc, u_ins, ins)
            yield s_occ, get_s_ins, get_ins_inc

# rules : lhs: C => rhs: Par<C,T> -> D
# here the lhs l is used to match a pattern of shape C in some decorated object X in Par<C,T>
# then the rhs takes the decoration of the pattern l in X to compute the rhs in D
class FamPFunctor:
    """
    A class to represent the partial functor of the local rules or rule families (lhs : CS.TO().naked => rhs : Callable[CS.TO(), CD.TO()])

    A rule family represents a set of rules such that lhs are all the decorations of the same structure

    Classes
    ----------
    FamRule : Type
        Type of the rules families
    FamInclusion : Type
        Type of inclusions between rules rule families
    Rule : Type
        Type of a rule in a rule family
    Inclusion : Type
        Type of an inclusion between rules
    Maker : Type
        Class to construct a FamPFunctor

    Attributes
    ----------
    CS : Datastructure
        Source parametrisation datastructure
    CD : Datastructure
        Destination datastructure
    smalls : Set[Rule]
        Set of minimal rules families
    G : networkx.MultiDiGraph[Rule, Inclusion]
        Graph of rules families with rule families inclusions

    Methods
    ----------
    is_small(ins) : bool
        Check if an instance corresponds to a minimal rule family
    next_small(X) : Iterator[Callable[[],[Instance]]
        Iterate over matches of a small rule family in X
    iter_under(ins) : Iterator[CS.TM(), Callable[[],[Instance], Callable[[Instance],[InstanceInc]]
        Iterate over sub-instances under an instance
    pmatch_up(ins) : Iterator[CS.TM(), Callable[[],[Instance], Callable[[Instance],[InstanceInc]]
        Iterate over super-instances over an instance
    iter_self_inclusions(ins) : Iterator[CS.TM(), Callable[[],[Instance], Callable[[Instance],[InstanceInc]]
        Iterate over symetric instances of an instance
    """

    class FamRule:
        """
        Represents a rule family
        
        lhs : CS.TO().naked => rhs : Callable[CS.TO(), CD.TO()]

        Attributes
        ----------
        lhs : CS.TO().naked
            Left hand side object
        rhs : Callable[CD.TO(), CD.TO()]
            Right hand side object
        cunder : int
            Count the rule families directly under this rule family in the graph of rules
        self_inclusions : List[FamInclusion]
            List of automorphisms of the rule family

        Methods
        ----------
        iter_self_inclusions() : Generator[FamInclusion]
            Iterate over automorphisms of the rule family
        """
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
        """
        Represents an inclusion of rule families
        
        g_a => g_b

        Attributes
        ----------
        g_a : FamRule
            Source rule family
        g_b : FamRule
            Destination rule family
        lhs : CS.TM().naked
            Inclusion of g_a.lhs in g_b.lhs
        rhs : CD.TM()
            Inclusion of g_a.rhs in g_b.rhs
        """

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

    class Maker():
        """
        Maker class for a FamPFunctor

        Attributes
        ----------
        CS : Datastructure
            Source datastructure
        CD : Datastructure
            Destination datastructure
        smalls : Set[FamRule]
            Set of minimal rule families
        G : networkx.MultiDiGraph[FamRule, FamInclusion]
            Graph of rule families with rule familie inclusions

        Methods
        ----------
        add_rule(l, r) : FamRule
            Insert new rule family
        add_inclusion(g_a, g_b, l, r) : (FamRule, FamRule, FamInclusion)
            Insert new rule family inclusion
        get() : FamPFunctor
            Get the generated FamPFunctor
        """
        def __init__(self, CS, CD):
            self.CS = CS
            self.CD = CD
            self.smalls = set()
            self.G = nx.MultiDiGraph()

        def add_fam_rule(self, l, r):
            rule = FamPFunctor.FamRule(l, r)
            self.G.add_node(rule)
            self.smalls.add(rule)
            return rule

        def add_fam_inclusion(self, g_a, g_b, l, r):
            inc = FamPFunctor.FamInclusion(g_a, g_b, l, r)
            if g_a == g_b:
                g_a.self_fam_inclusions.add(inc)
            else:
                g_b.cunder += 1
                self.G.add_edge(g_a, g_b, key = inc)
                if g_b in self.smalls:
                    self.smalls.remove(g_b)
            return (g_a, g_b, inc)

        def get(self):
            return FamPFunctor(self.CS, self.CD, self.smalls, self.G)

    def __init__(self, CS, CD, smalls, G):
        self.CS = CS
        self.CD = CD
        self.G = G
        self.smalls = smalls

    class Rule:
        """
        Represents a rule
        
        lhs : CS.TO() => rhs : CD.TO()

        Attributes
        ----------
        fam : List[FamRule]
            The rule family of this rule
        lhs : CS.TO()
            Left hand side (parametrisation) object
        rhs : CD.TO()
            Right hand side object
        cunder : int
            Count the rules directly under this rule in the graph of rule families

        Methods
        ----------
        get_rhs() : CD.TO()
            Get the right hand side of the rule
        """
        def __init__(self, fam_rule, lp):
            assert fam_rule.lhs == lp.naked()
            self.fam = fam_rule
            self.cunder = fam_rule.cunder
            self.lhs = lp
            self.rhs = fam_rule.rhs(lp)
        
        def get_rhs(self, underincs):
            return self.rhs

        def __eq__(self, other):
            if not isinstance(other, FamPFunctor.Rule):
                return False
            return self.fam == other.fam and self.lhs == other.lhs

        def __hash__(self):
            return hash(self.fam) ^ 31 * hash(self.lhs)

        def __repr__(self):
            return "r(fam : " + str(self.fam) + ", lhs " + str(self.lhs) + ", rhs " + str(self.rhs) + ")"

    class Inclusion:
        """
        Represents an inclusion of rules
        
        g_a => g_b

        Attributes
        ----------
        g_a : Rule
            Source rule
        g_b : Rule
            Destination rule
        lhs : CS.TM()
            Inclusion of g_a.lhs in g_b.lhs
        rhs : CD.TM()
            Inclusion of g_a.rhs in g_b.rhs

        Methods
        ----------
        get_rhs() : CD.TM()
            Get the right hand side of the inclusion
        """

        def __init__(self, fam_inc, g_a, g_b, lhs):
            assert fam_inc.lhs == lhs.naked()
            self.fam = fam_inc
            self.g_a = g_a
            self.g_b = g_b
            self.lhs = lhs
            self.rhs = fam_inc.rhs(g_a.lhs, g_b.lhs, g_a.rhs, g_b.rhs)

        def get_rhs(self, over_rhs):
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
                return InstanceInc(u_inc, u_ins, ins)
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
                    return InstanceInc(o_inc, ins, o_ins)
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
                return InstanceInc(s_inc, s_ins, ins)
            yield s_occ, get_s_ins, get_ins_inc
