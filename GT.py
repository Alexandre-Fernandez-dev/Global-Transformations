import networkx as nx


class Rule:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __eq__(self, other):
        if not isinstance(other,Rule):
            return False
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
        if not isinstance(other,Inclusion):
            return False
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

        for u in self.small_pred.edges(keys = True):
            print(u)

        print()

        print(self.smalls)

        instances = {}
        potatoes = []

        def merge_potatoe(potatoe_a, potatoe_b, h_a, h_b):
            (lresult,on_a,on_b) = self.C.merge(h_a,h_b)
            potatoe = { 'obs_by': potatoe_a['obs_by'] + potatoe_b['obs_by'], 'partial_result': lresult }
            potatoes.append(potatoe)
            for ins in potatoe_a['obs_by']:
                i = instances[ins]
                i['potatoe'] = potatoe
                i['potatoe_inc'] = on_a if i['potatoe_inc'] == None else i['potatoe_inc'].compose(on_a)
            for ins in potatoe_b['obs_by']:
                i = instances[ins]
                i['potatoe'] = potatoe
                i['potatoe_inc'] = on_b if i['potatoe_inc'] == None else i['potatoe_inc'].compose(on_b)
            return potatoe, h_a.compose(on_a)

        def process(ins, rule):
            print()
            print("IN process: " + str(ins))
            is_top_ins = True
            potatoe = None
            potatoe_inc = None
            for _, over_rule, inc in self.G.out_edges(rule, keys = True):
                #print("    " + str(inc))
                for over_ins in self.C.pattern_match(inc.lhs, ins):
                    is_top_ins = False
                    if over_ins not in instances:
                        over_ins.clean()
                        instances[over_ins] = { 'nb_dep': len(self.small_pred.in_edges(over_rule)) }
                        process(over_ins, over_rule)
                    over_potatoe = instances[over_ins]['potatoe']
                    over_potatoe_inc = instances[over_ins]['potatoe_inc']
                    potatoe_inc_ = inc.rhs if over_potatoe_inc == None else inc.rhs.compose(over_potatoe_inc)
                    if potatoe == None:
                        potatoe = over_potatoe
                        potatoe_inc = potatoe_inc_
                        potatoe['obs_by'].append(ins)
                        instances[ins]['potatoe'] = potatoe
                        instances[ins]['potatoe_inc'] = potatoe_inc
                    else:
                        potatoe, potatoe_inc = merge_potatoe(over_potatoe, potatoe, potatoe_inc_, potatoe_inc)

            print("OUT process. Top instance? " + str(is_top_ins))
            if is_top_ins:
                potatoe = { 'obs_by': [ ins ], 'partial_result': rule.rhs }
                instances[ins]['potatoe'] = potatoe
                instances[ins]['potatoe_inc'] = None # None for identity
                potatoes.append(potatoe)

            print()
            print("Instances:")
            for ins in instances.items():
                print(ins)
            print()
            print("Potatoes:")
            for pot in potatoes:
                print(pot)

        print()
        for small_rule in self.smalls:
            # print("small rule: " + str(small_rule))
            for small_ins in self.C.pattern_match(small_rule.lhs, X):
                # print()
                if small_ins not in instances:
                    small_ins.clean()
                    instances[small_ins] = { 'nb_dep': 1 }
                    process(small_ins, small_rule)
                break

        print()
        print(instances)

        print()
        print(len(potatoes))
        print(potatoes)



def test():
        pass


if __name__ == "__main__":
    test()













#
