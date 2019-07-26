import networkx as nx


class Rule:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __eq__(self, other):
        return self.lhs == other.lhs

    def __hash__(self):
        return hash(self.lhs)

    def __repr__(self):
        return str(self.lhs) + ' => ...' # + str(self.rhs)

class Inclusion:
    def __init__(self, g_a, g_b, lhs, rhs):
        self.g_a = g_a
        self.g_b = g_b
        self.lhs = lhs
        self.rhs = rhs

    def __eq__(self, other):
        return self.lhs == other.lhs

    def __hash__(self):
        return hash(self.lhs)

    def __repr__(self):
        return str(self.lhs) + ' => ...' #+ str(self.rhs)

    def compose(self, other):
        return Inclusion(self.g_a, other.g_b, self.lhs.compose(other.lhs), self.rhs.compose(other.rhs))


class GT:

    def __init__(self,C):
        self.C = C
        self.G = nx.MultiDiGraph()
        self.smalls = set()
        pass

    def add_rule(self,l,r):
        rule = Rule(l,r)
        self.G.add_node(rule)
        return rule

    def add_inclusion(self,g_a,g_b,l,r):
        if g_a == g_b: return None
        assert g_a.lhs == l.dom
        assert g_b.lhs == l.cod
        assert g_a.rhs == r.dom
        assert g_b.rhs == r.cod
        inc = Inclusion(g_a,g_b,l,r)
        e = self.G.add_edge(g_a, g_b, key = inc)
        return (g_a,g_b,e)

    def apply(self,X):
        self.small_pred = nx.MultiDiGraph()

        def toto(g):
            if g in self.small_pred.nodes():
                return [ r for _, _, r in self.small_pred.in_edges(g, keys = True) ]
            self.small_pred.add_node(g)
            l = []
            for s, _, inc in self.G.in_edges(g, keys = True):
                r = toto(s)
                if r == []:
                    l.append(inc)
                else:
                    l = l + [ incp.compose(inc) for incp in r ]
            if l == []: self.smalls.add(g)
            for inc in l:
                self.small_pred.add_edge(inc.g_a, g, inc)
            return l


        for g in self.G.nodes:
            toto(g)

        for u in self.small_pred.edges():
            print(u)


        instances = {}
        print(self.smalls)


        def process(ins, rule):
            print("IN process: " + str(ins))
            is_top_ins = True
            for _, over_rule, inc in self.G.out_edges(rule, keys = True):
                print("    " + str(inc))
                for over_ins in self.C.pattern_match(inc.lhs, ins):
                    is_top_ins = False
                    if over_ins not in instances:
                        over_ins.clean()
                        instances[over_ins] = None
                        process(over_ins, over_rule)
                    # if already in instances skip
                    # else add it with all it small inclusions
            print("OUT process. Top instance? " + str(is_top_ins))

        print()
        for small_rule in self.smalls:
            print("small rule: " + str(small_rule))
            for small_ins in self.C.pattern_match(small_rule.lhs, X):
                print()
                if small_ins not in instances:
                    small_ins.clean()
                    instances[small_ins] = None
                    process(small_ins, small_rule)

        print()
        print(instances)



def test():
        pass


if __name__ == "__main__":
    test()













#
