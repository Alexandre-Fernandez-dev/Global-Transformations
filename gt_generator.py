import networkx as nx
from Graph import Graph, GraphO, GraphM

class RuleSet:
    class Rule:
        def __init__(self, lhs, rhs):
            self.lhs = lhs
            self.rhs = rhs

        def __hash__(self):
            return hash(self.lhs)
        
        def __eq__(self, other):
            return self.lhs == other.lhs and self.rhs == other.rhs
        
        def __repr__(self):
            return str(self.lhs) + " -> " + str(self.rhs)

    class Generator:
        class Hs_inc:
            def __init__(self, g_a, g_b, hs):
                self.g_a = g_a
                self.g_b = g_b
                self.hs = hs
            
            def name(self):
                return self.hs.name
            
            def set_name(self, name):
                self.hs.name = name
            
            def compose(self, other):
                return RuleSet.Generator.Hs_inc(self.g_a, other.g_b, self.hs.compose(other.hs))

            def __repr__(self):
                return str(self.g_a) + " => " + str(self.g_b) + " : " + str(self.hs)
            
            def __hash__(self):
                return hash(self.hs)
            
            def __eq__(self, other):
                return self.g_a == other.g_a and self.g_b == other.g_b and self.hs == other.hs

        def __init__(self, CS, CD):
            self.gl_gen = GraphO()
            self.gl_free = None
            self.m_l_gen_free = None
            self.gr = GraphO()
            self.level_r = { }
            self.max_level = 0
            self.r_nl = { } # rule -> node in gl
            self.r_nr =  { } # rule -> node in gr
            self.i_el = { } # lhs_inc -> edge in gl
            self.i_er = { } # rhs_inc -> edge in gr
            # should be stocked in the graph structure \/
            self.nl_r = { } # node in gl -> rule
            self.nr_r = { } # node in gr -> rule
            self.el_i = { } # edge in gl -> lhs_inc
            self.er_i = { } # edge in gr -> rhs_inc
            #
            self.CS = CS
            self.CD = CD
        
        def add_generator_rule(self, lhs, rhs, level):
            r = RuleSet.Rule(lhs, rhs)
            nl = self.gl_gen.add_node()
            nr = self.gr.add_node()
            self.r_nl[r] = nl
            self.r_nr[r] = nr
            self.nl_r[nl] = r
            self.nr_r[nr] = r
            l_list = self.level_r.setdefault(level, [])
            if level > self.max_level:
                self.max_level = level
            l_list.append(r)
            return r
        
        def add_lhs_inc(self, g_a, g_b, lhs):
            i = self.Hs_inc(g_a, g_b, lhs)
            el = self.gl_gen.add_edge(self.r_nl[g_a], self.r_nl[g_b])
            self.i_el[i] = el
            self.el_i[el] = i
        
        def add_rhs_inc(self, g_a, g_b, rhs):
            i = self.Hs_inc(g_a, g_b, rhs)
            er = self.gr.add_edge(self.r_nr[g_a], self.r_nr[g_b])
            self.i_er[i] = er
            self.er_i[er] = i
        
        @staticmethod
        def free_gen(g, level_r, max_level, r_n, n_r, i_e, e_i):
            # generate automorphims for each level
            def genAuto(edges_auto, constraints):
                cont = False
                new = []
                for i in edges_auto:
                    i_i = e_i[i]
                    for j in edges_auto:
                        i_j = e_i[j]
                        i_ij = i_i.compose(i_j)
                        if i_ij in i_e.keys():
                            i_ij = e_i[i_e[i_ij]] # weird way to get reprensentant from dict
                        if i_ij.name() == None:
                            i_ij.set_name("(" + i_i.name() + " . " + i_j.name() + ")")
                        if i_ij not in i_e.keys() and i_ij not in new:
                            cont = True
                            new.append(i_ij)
                        i_ij_c = constraints.setdefault(i_ij, [])
                        if (i_i, i_j) not in i_ij_c:
                            cont = True
                            i_ij_c.append((i_i, i_j))
                for i_n in new:
                    e_n = g.add_edge(r_n[i_n.g_a], r_n[i_n.g_b])
                    i_e[i_n] = e_n
                    e_i[e_n] = i_n
                    edges_auto.append(e_n)
                if cont:
                    return genAuto(edges_auto, constraints)
                else:
                    return edges_auto, constraints

            def genMorph(edge1, edge2, constraints, addinfirst):
                cont = False
                new = []
                add = edge1 if addinfirst else edge2
                for i in edge1:
                    i_i = e_i[i]
                    for j in edge2:
                        i_j = e_i[j]
                        i_ij = i_i.compose(i_j)
                        if i_ij in i_e.keys():
                            i_ij = e_i[i_e[i_ij]] # weird way to get reprensentant from dict
                        if i_ij.name() == None:
                            i_ij.set_name("(" + i_i.name() + " . " + i_j.name() + ")")
                        if i_ij not in i_e.keys() and i_ij not in new:
                            cont = True
                            new.append(i_ij)
                        i_ij_c = constraints.setdefault(i_ij, [])
                        if (i_i, i_j) not in i_ij_c:
                            cont = True
                            i_ij_c.append((i_i, i_j))
                for i_n in new:
                    e_n = g.add_edge(r_n[i_n.g_a], r_n[i_n.g_b])
                    i_e[i_n] = e_n
                    e_i[e_n] = i_n
                    add.append(e_n)
                if cont:
                    return genMorph(edge1, edge2, constraints, addinfirst)
                else:
                    return edge1, edge2, constraints

            constraints = dict()
            for i in range(0, max_level+1):
                # print(level_r[i])
                # for r in level_r[i]:
                #     for aut in r.aut:
                #         print(" ", aut)
                # rule_auto_edges = [ [ i_e[aut] for aut in r.aut ] for r in level_r[i] ]
                rule_auto_edges = [ list(set(g.out_edges(r_n[r])).intersection(g.in_edges(r_n[r]))) for r in level_r[i] ]
                for auto_edges in rule_auto_edges:
                    genAuto(auto_edges, constraints)

                #     for e in auto_edges:
                #         print(e_i[e].name(), e_i[e].lhs)
                #     for k, v in constraints.items():
                #         print(k.name(), " : ", [ vi[0].name() + " . " + vi[1].name() for vi in v ])
                #     print()
                # print()
            
            for i in range(0, max_level):
                # print("LEVEL ", i)
                for r0 in level_r[i]:
                    n0 = r_n[r0]
                    # auto_edges_0 = [ i_e[aut] for aut in r0.aut ]
                    auto_edges_0 = list(set(g.out_edges(n0)).intersection(g.in_edges(n0)))
                    # print(auto_edges_0)
                    for r1 in level_r[i+1]:
                        n1 = r_n[r1]
                        # auto_edges_1 = [ i_e[aut] for aut in r1.aut ]
                        auto_edges_1 = list(set(g.out_edges(n1)).intersection(g.in_edges(n1)))
                        edgesbetween = list(set(g.out_edges(n0)).intersection(g.in_edges(n1)))

                        genMorph(auto_edges_0, edgesbetween, constraints, False)

                        # for e in edgesbetween:
                        #     print(e_i[e].name(), e_i[e].lhs)
                        # for k, v in constraints.items():
                        #     print(k.name(), " : ", [ vi[0].name() + " . " + vi[1].name() for vi in v ])
                        # print()

                        genMorph(edgesbetween, auto_edges_1, constraints, True)

                        # for e in edgesbetween:
                        #     print(e_i[e].name(), e_i[e].lhs)
                        # for k, v in constraints.items():
                        #     print(k.name(), " : ", [ vi[0].name() + " . " + vi[1].name() for vi in v ])
                        # print()
                        
            # print(len(g.edges()))
            # for k, v in constraints.items():
            #     print(k.name(), len(v))
            for e in g.edges(keys = True):
                print(e_i[e].name())#, e_i[e].lhs)
            for k, v in constraints.items():
                print("-", k.name(), " : ")
                for vi in v:
                    print("  *", vi[0].name() + " . " + vi[1].name())
            return constraints

        def generate(self):
            # note : in some cases the rhs category can also be generated with only the objects
            # and some banned constraints for the morphisms -> no generator is really needed
            # maybe it can be the same for the lhs category but it will affect the search tree because
            # the generator lhs category will be trivally it's own freely generated category
            # -> the search tree is a rooted multi-span

            # first take the freely generated rhs category
            # then generate the lhs category (add composites of autos then composite of a o i and i o a)
                # when a new composite is found it adds composition constraints on the lhs graph
            # iterate the pattern matchings of the lhs graph generator graph in the rhs freely generated graph
                # from theses pattern matching recursively extend to all lhs category
                    # if a lhs constraint is broken 
            
            #test
            self.gl_free = self.gl_gen.copy()
            self.r_nl_f = self.r_nl.copy()
            self.nl_r_f = self.nl_r.copy()
            self.i_el_f = self.i_el.copy()
            self.el_i_f = self.el_i.copy()

            constraintsl = self.free_gen(self.gl_free, self.level_r, self.max_level, self.r_nl_f, self.nl_r_f, self.i_el_f, self.el_i_f)
            self.free_gen(self.gr, self.level_r, self.max_level, self.r_nr, self.nr_r, self.i_er, self.er_i)
            print(len(self.gl_gen.edges()))
            print(len(self.gl_free.edges()))
            print(len(self.gr.edges()))

            rules = []
            i = 0
            for m in Graph.pattern_match(self.gl_free, self.gr):
                keep = True
                for nl in self.gl_free.nodes(): # check if nodes are correctly mapped
                    nr = m.apply(nl)
                    r = self.nl_r[nl]
                    rp = self.nr_r[nr]
                    if r != rp:
                        keep = False
                        break
                    
                if not keep:
                    continue
                # break
                for leq_l in constraintsl: # check if edges are correctly mapped (respects compositions)
                    for leq_r in constraintsl[leq_l]:
                        req_l = self.er_i[m.apply(self.i_el_f[leq_l])]
                        l_com = self.el_i_f[self.i_el_f[leq_r[0].compose(leq_r[1])]]
                        r_com = self.er_i[m.apply(self.i_el_f[l_com])]
                        if req_l != r_com:
                            keep = False
                            break
                    if not keep:
                        break
                if keep:
                    rules.append(m)
                break
                i += 1

            return rules

    def __init__(self, g):
        self.g = g

def test_free_gen():
    rsgen = RuleSet.Generator(Graph, Graph)

    l0 = GraphO()
    l0n0 = l0.add_node()
    l0.name = "N"

    g_0 = rsgen.add_generator_rule(l0, l0, 0)

    l1 = GraphO()
    l1n0 = l1.add_node()
    l1n1 = l1.add_node()
    l1e0 = l1.add_edge(l1n0, l1n1)
    l1e1 = l1.add_edge(l1n1, l1n0)
    l1.name = "E"

    r1 = GraphO()
    r1n0 = r1.add_node()
    r1n1 = r1.add_node()
    r1n2 = r1.add_node()
    r1e0 = r1.add_edge(r1n0, r1n1)
    r1e1 = r1.add_edge(r1n1, r1n0)
    r1e2 = r1.add_edge(r1n1, r1n2)
    r1e3 = r1.add_edge(r1n2, r1n1)
    r1.name = "Es"

    g_1 = rsgen.add_generator_rule(l1, r1, 1)

    l2 = GraphO()
    l2n0 = l2.add_node()
    l2n1 = l2.add_node()
    l2n2 = l2.add_node()
    l2e0 = l2.add_edge(l2n0, l2n1)
    l2e1 = l2.add_edge(l2n1, l2n0)
    l2e2 = l2.add_edge(l2n1, l2n2)
    l2e3 = l2.add_edge(l2n2, l2n1)
    l2e4 = l2.add_edge(l2n2, l2n0)
    l2e5 = l2.add_edge(l2n0, l2n2)
    l2.name = "T"

    r2 = GraphO()
    r2n0  = r2.add_node()
    r2n1  = r2.add_node()
    r2n2  = r2.add_node()
    r2n3  = r2.add_node()
    r2n4  = r2.add_node()
    r2n5  = r2.add_node()
    r2e0  = r2.add_edge(r2n0, r2n1)
    r2e1  = r2.add_edge(r2n1, r2n0)
    r2e2  = r2.add_edge(r2n1, r2n2)
    r2e3  = r2.add_edge(r2n2, r2n1)
    r2e4  = r2.add_edge(r2n2, r2n3)
    r2e5  = r2.add_edge(r2n3, r2n2)
    r2e6  = r2.add_edge(r2n3, r2n4)
    r2e7  = r2.add_edge(r2n4, r2n3)
    r2e8  = r2.add_edge(r2n4, r2n5)
    r2e9  = r2.add_edge(r2n5, r2n4)
    r2e10 = r2.add_edge(r2n5, r2n0)
    r2e11 = r2.add_edge(r2n0, r2n5)
    r2e12 = r2.add_edge(r2n3, r2n1)
    r2e13 = r2.add_edge(r2n1, r2n3)
    r2e14 = r2.add_edge(r2n5, r2n3)
    r2e15 = r2.add_edge(r2n3, r2n5)
    r2e16 = r2.add_edge(r2n1, r2n5)
    r2e17 = r2.add_edge(r2n5, r2n1)
    r2.name = "Ts"

    g_2 = rsgen.add_generator_rule(l2, r2, 2)

    idl0 = GraphM(l0, l0, {
        l0n0 : l0n0
    })
    idl0.name = "id" + l0.name

    rsgen.add_lhs_inc(g_0, g_0, idl0)
    rsgen.add_rhs_inc(g_0, g_0, idl0)

    idl1 = GraphM(l1, l1, {
        l1n0 : l1n0,
        l1n1 : l1n1,
        l1e0 : l1e0,
        l1e1 : l1e1
    })
    idl1.name = "id" + l1.name

    rsgen.add_lhs_inc(g_1, g_1, idl1)

    idr1 = GraphM(r1, r1, {
        r1n0 : r1n0 ,
        r1n1 : r1n1 ,
        r1n2 : r1n2 ,
        r1e0 : r1e0 ,
        r1e1 : r1e1 ,
        r1e2 : r1e2 ,
        r1e3 : r1e3 
    })
    idr1.name = "id" + r1.name

    rsgen.add_rhs_inc(g_1, g_1, idr1)

    l1l1 = GraphM(l1, l1, {
        l1n0 : l1n1,
        l1n1 : l1n0,
        l1e0 : l1e1,
        l1e1 : l1e0
    })
    l1l1.name = "f"  + l1.name

    rsgen.add_lhs_inc(g_1, g_1, l1l1)

    r1r1 = GraphM(r1, r1, {
        r1n0 : r1n2 ,
        r1n1 : r1n1 ,
        r1n2 : r1n0 ,
        r1e0 : r1e3 ,
        r1e1 : r1e2 ,
        r1e2 : r1e1 ,
        r1e3 : r1e0 
    })
    r1r1.name = "f" + r1.name

    rsgen.add_rhs_inc(g_1, g_1, r1r1)

    idl2 = GraphM(l2, l2, {
        l2n0 : l2n0,
        l2n1 : l2n1,
        l2n2 : l2n2,
        l2e0 : l2e0,
        l2e1 : l2e1,
        l2e2 : l2e2,
        l2e3 : l2e3,
        l2e4 : l2e4,
        l2e5 : l2e5
    })
    idl2.name = "id" + l2.name

    rsgen.add_lhs_inc(g_2, g_2, idl2)

    idr2 = GraphM(r2, r2, {
        r2n0 : r2n0,
        r2n1 : r2n1,
        r2n2 : r2n2,
        r2n3 : r2n3,
        r2n4 : r2n4,
        r2n5 : r2n5,
        r2e0 : r2e0,
        r2e1 : r2e1,
        r2e2 : r2e2,
        r2e3 : r2e3,
        r2e4 : r2e4,
        r2e5 : r2e5,
        r2e6 : r2e6,
        r2e7 : r2e7,
        r2e8 : r2e8,
        r2e9 : r2e9,
        r2e10: r2e10,
        r2e11: r2e11,
        r2e12: r2e12,
        r2e13: r2e13,
        r2e14: r2e14,
        r2e15: r2e15,
        r2e16: r2e16,
        r2e17: r2e17
    })
    idr2.name = "id" + r2.name

    rsgen.add_rhs_inc(g_2, g_2, idr2)

    l2l2r = GraphM(l2, l2, {
        l2n0 : l2n1,
        l2n1 : l2n2,
        l2n2 : l2n0,
        l2e0 : l2e2,
        l2e1 : l2e3,
        l2e2 : l2e4,
        l2e3 : l2e5,
        l2e4 : l2e0,
        l2e5 : l2e1
    })
    l2l2r.name = "r" + l2.name

    rsgen.add_lhs_inc(g_2, g_2, l2l2r)

    r2r2r = GraphM(r2, r2, {
        r2n0 : r2n2,
        r2n1 : r2n3,
        r2n2 : r2n4,
        r2n3 : r2n5,
        r2n4 : r2n0,
        r2n5 : r2n1,
        r2e0 : r2e4,
        r2e1 : r2e5,
        r2e2 : r2e6,
        r2e3 : r2e7,
        r2e4 : r2e8,
        r2e5 : r2e9,
        r2e6 : r2e10,
        r2e7 : r2e11,
        r2e8 : r2e0,
        r2e9 : r2e1,
        r2e10: r2e2,
        r2e11: r2e3,
        r2e12: r2e14,
        r2e13: r2e15,
        r2e14: r2e16,
        r2e15: r2e17,
        r2e16: r2e12,
        r2e17: r2e13
    })
    r2r2r.name = "r" + r2.name

    rsgen.add_rhs_inc(g_2, g_2, r2r2r)

    l2l2f = GraphM(l2, l2, {
        l2n0 : l2n0,
        l2n1 : l2n2,
        l2n2 : l2n1,
        l2e0 : l2e5,
        l2e1 : l2e4,
        l2e2 : l2e3,
        l2e3 : l2e2,
        l2e4 : l2e1,
        l2e5 : l2e0
    })
    l2l2f.name = "f" + l2.name

    rsgen.add_lhs_inc(g_2, g_2, l2l2f)

    r2r2f = GraphM(r2, r2, {
        r2n0 : r2n0,
        r2n1 : r2n5,
        r2n2 : r2n4,
        r2n3 : r2n3,
        r2n4 : r2n2,
        r2n5 : r2n1,
        r2e0 : r2e11,
        r2e1 : r2e10,
        r2e2 : r2e9,
        r2e3 : r2e8,
        r2e4 : r2e7,
        r2e5 : r2e6,
        r2e6 : r2e5,
        r2e7 : r2e4,
        r2e8 : r2e3,
        r2e9 : r2e2,
        r2e10: r2e1,
        r2e11: r2e0,
        r2e12: r2e15,
        r2e13: r2e14,
        r2e14: r2e13,
        r2e15: r2e12,
        r2e16: r2e17,
        r2e17: r2e16
    })
    r2r2f.name = "f" + r2.name

    rsgen.add_rhs_inc(g_2, g_2, r2r2f)

    l0l1 = GraphM(l0, l1, {
        l0n0 : l1n0
    })
    l0l1.name = "DiE"

    rsgen.add_lhs_inc(g_0, g_1, l0l1)

    r0r1 = GraphM(l0, r1, {
        l0n0 : r1n0
    })
    r0r1.name = "DiEs"

    rsgen.add_rhs_inc(g_0, g_1, r0r1)
    
    l1l2 = GraphM(l1, l2, {
        l1n0 : l2n0,
        l1n1 : l2n1,
        l1e0 : l2e0,
        l1e1 : l2e1
    })
    l1l2.name = "EiT"

    rsgen.add_lhs_inc(g_1, g_2, l1l2)

    r1r2 = GraphM(r1, r2, {
        r1n0 : r2n0,
        r1n1 : r2n1,
        r1n2 : r2n2,
        r1e0 : r2e0,
        r1e1 : r2e1,
        r1e2 : r2e2,
        r1e3 : r2e3
    })
    r1r2.name = "EiTs"

    rsgen.add_rhs_inc(g_1, g_2, r1r2)

    print(len(rsgen.generate()))


def simpleTriMeshRefinement():
    l0 = GraphO()
    l0n0 = l0.add_node()
    l0.name = "N"

    l1 = GraphO()
    l1n0 = l1.add_node()
    l1n1 = l1.add_node()
    l1e0 = l1.add_edge(l1n0, l1n1)
    l1e1 = l1.add_edge(l1n0, l1n1)
    l1.name = "E"

    l2 = GraphO()
    l2n0 = l2.add_node()
    l2n1 = l2.add_node()
    l2n2 = l2.add_node()
    l2e0 = l2.add_edge(l2n0, l2n1)
    l2e1 = l2.add_edge(l2n1, l2n0)
    l2e2 = l2.add_edge(l2n1, l2n2)
    l2e3 = l2.add_edge(l2n2, l2n1)
    l2e4 = l2.add_edge(l2n2, l2n0)
    l2e5 = l2.add_edge(l2n0, l2n2)
    l2.name = "T"

    idl1 = GraphM(l1, l1, {
        l1n0 : l1n0,
        l1n1 : l1n1,
        l1e0 : l1e0,
        l1e1 : l1e1
    })
    idl1.name = "id" + l1.name

    l1l1 = GraphM(l1, l1, {
        l1n0 : l1n1,
        l1n1 : l1n0,
        l1e0 : l1e1,
        l1e1 : l1e0
    })
    l1l1.name = l1.name + "f"

    idl2 = GraphM(l2, l2, {
        l2n0 : l2n0,
        l2n1 : l2n1,
        l2n2 : l2n2,
        l2e0 : l2e0,
        l2e1 : l2e1,
        l2e2 : l2e2,
        l2e3 : l2e3,
        l2e4 : l2e4,
        l2e5 : l2e5
    })
    idl2.name = "id" + l2.name

    l2l2r = GraphM(l2, l2, {
        l2n0 : l2n1,
        l2n1 : l2n2,
        l2n2 : l2n0,
        l2e0 : l2e2,
        l2e1 : l2e3,
        l2e2 : l2e4,
        l2e3 : l2e5,
        l2e4 : l2e0,
        l2e5 : l2e1
    })
    l2l2r.name = l2.name + "r"

    l2l2f = GraphM(l2, l2, {
        l2n0 : l2n0,
        l2n1 : l2n2,
        l2n2 : l2n1,
        l2e0 : l2e5,
        l2e1 : l2e4,
        l2e2 : l2e3,
        l2e3 : l2e2,
        l2e4 : l2e1,
        l2e5 : l2e0
    })
    l2l2f.name = l2.name + "f"

    def genAuto(boxGenAuto, constraints):
        cont = False
        new = []
        for i in boxGenAuto:
            for j in boxGenAuto:
                i_j = i.compose(j)
                if i_j in boxGenAuto:
                    i_j = boxGenAuto[i_j]
                if i_j.name == None:
                    i_j.name = "(" + i.name + " . " + j.name + ")"
                if i_j not in boxGenAuto and i_j not in new:
                    cont = True
                    new.append(i_j)
                i_jc = constraints.setdefault(i_j, [])
                if (i, j) not in i_jc:
                    cont = True
                    i_jc.append((i, j))
        for n in new:
            boxGenAuto[n] = n
        if cont:
            return genAuto(boxGenAuto, constraints)
        else:
            return boxGenAuto, constraints

    boxAuto0 = dict()

    boxAuto1 = { idl1 : idl1, l1l1 : l1l1 }
    boxAuto1, constraints1 = genAuto(boxAuto1, dict())

    print()
    for m in boxAuto1:
        print(m.name, m)
    for k, v in constraints1.items():
        print(k.name, " : ", [ vi[0].name + " . " + vi[1].name for vi in v ])
    
    boxAuto2 = { idl2 : idl2, l2l2f : l2l2f, l2l2r : l2l2r }
    boxAuto2, constraints2 = genAuto(boxAuto2, dict())

    print()
    for m in boxAuto2:
        print(m.name, m)
    for k, v in constraints2.items():
        print(k.name, " : ", [ vi[0].name + " . " + vi[1].name for vi in v ])
    
    l0l1 = GraphM(l0, l1, {
        l0n0 : l1n0
    })
    l0l1.name = "DiE"
    
    l1l2 = GraphM(l1, l2, {
        l1n0 : l2n0,
        l1n1 : l2n1,
        l1e0 : l2e0,
        l1e1 : l2e1
    })
    l1l2.name = "EiT"

    def genM(boxGenM, constraints, addinfirst):
        cont = False
        new = []
        add = boxGenM[0] if addinfirst else boxGenM[1]
        for i in boxGenM[0]:
            for j in boxGenM[1]:
                i_j = i.compose(j)
                if i_j in add:
                    i_j = add[i_j]
                if i_j.name == None:
                    i_j.name = "(" + i.name + " . " + j.name + ")"
                if i_j not in add and i_j not in new:
                    cont = True
                    new.append(i_j)
                i_jc = constraints.setdefault(i_j, [])
                if (i, j) not in i_jc:
                    cont = True
                    i_jc.append((i, j))
        for n in new:
            add[n] = n
        if cont:
            return genM(boxGenM, constraints, addinfirst)
        else:
            return boxGenM, constraints
    
    boxM001 = ({ l0l1 : l0l1 }, boxAuto0)

    boxM011 = ({ l0l1 : l0l1 }, boxAuto1)

    boxM01 = boxM001[0].update(boxM011[0])

    boxM011, constraints3 = genM(boxM011, dict(), True)

    print()
    for m in boxM011[0]:
        print(m.name, m)
    for k, v in constraints3.items():
        print(k.name, " : ", [ vi[0].name + " . " + vi[1].name for vi in v ])
    
    boxM112 = (boxAuto1, { l1l2 : l1l2})

    boxM112, constraints4 = genM(boxM112, dict(), False)

    print()
    for m in boxM112[1]:
        print(m.name, m)
    for k, v in constraints4.items():
        print(k.name, " : ", [ vi[0].name + " . " + vi[1].name for vi in v ])

    boxM122 = ( boxM112[1], boxAuto2 )

    boxM122, constraints5 = genM(boxM122, dict(), True)

    print()
    for m in boxM122[0]:
        print(m.name, m)
    for k, v in constraints5.items():
        print(">> ", k.name, " : ")
        print(" ", k, " : ")
        for vi in v:
            print(" -", vi[0].name + " . " + vi[1].name, " : ")
            print(" a", vi[0])
            print(" b", vi[1])
            print(" c", vi[0].compose(vi[1]))
            assert(vi[0].compose(vi[1]) == k)
            print()
        print()

test_free_gen()
# simpleTriMeshRefinement()