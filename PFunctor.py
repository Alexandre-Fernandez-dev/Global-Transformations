import networkx as nx

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

        if not isinstance(other,Rule):
            return False
        return self.lhs == other.lhs

    def __hash__(self):
        return hash(self.lhs)

    def __repr__(self):
        return str(self.lhs) + " => " + str(self.rhs)


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
        if not isinstance(other,Inclusion):
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
        return Inclusion(self.g_a, other.g_b, self.lhs.compose(other.lhs), self.rhs.compose(other.rhs))

class PartialFunctor:
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
            rule = Rule(l, r)
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
            inc = Inclusion(g_a, g_b, l, r)
            if g_a == g_b:
                g_a.self_inclusions.add(inc)
            else:
                self.G.add_edge(g_a, g_b, key = inc)
            return (g_a, g_b, inc)
        
        def get(self):
            return PartialFunctor(self.CS, self.CD, self.G)

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
            yield small_rule, inc
    
    def iter_under(self, rule):
        for u_rule, _, u_inc in self.G.in_edges(rule, keys=True):
            yield u_rule, u_inc
    
    def pmatch_up(self, rule, match):
        for _, over_rule, inc in self.G.out_edges(rule, keys = True):
            for over_match in self.CS.pattern_match(inc.lhs, match):
                yield over_rule, over_match
    
    def next_small(self, X):
        for small_rule in self.smalls:
            for small_match in self.CS.pattern_match(small_rule.lhs, X):
                small_match.clean()
                yield small_rule, small_match