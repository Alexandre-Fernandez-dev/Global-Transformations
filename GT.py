import networkx as nx


class GT:

    def __init__(self,C):
        self.C = C
        self.G = nx.MultiDiGraph()
        pass

    def add_rule(self,l,r):
        rid = self.G.number_of_nodes()
        self.G.add_node(rid, lhs = l, rhs = r)
        return rid

    def get_lhs(self,id):
        return self.G.nodes[id]['lhs']

    def get_rhs(self,id):
        return self.G.nodes[id]['rhs']

    def add_inclusion(self,id_a,id_b,l,r):
        assert self.get_lhs(id_a) == l.s
        assert self.get_lhs(id_b) == l.t
        assert self.get_rhs(id_a) == r.s
        assert self.get_rhs(id_b) == r.t

        e = self.G.add_edge(id_a,id_b, lhs = l, rhs = r)
        return (id_a,id_b,e)

    def apply(self,X):
        batch = nx.DiGraph()
        for g in reversed(list(nx.algorithms.dag.topological_sort(self.G))): #self.G.nodes(data = 'lhs'):
            l = self.G.nodes[g]['lhs']
            for ll in self.C.pattern_match(l,X):
                 =
                flag = False
                for lll in batch.nodes(data = 'green'):
                    if lll == l:
                        flag = True
                if not flat: batch.add_node(batch.number_of_nodes(), green = ll)
        print(batch.nodes(data = True))


















#
