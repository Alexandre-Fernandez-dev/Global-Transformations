import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

def triangle_mesh_refinement():
    from src.engine.downward_resolv.GT import GT
    import src.engine.downward_resolv.PFunctor as PFunctor
    from src.data.Graph import Graph
    from src.data.Sheaf import Parametrisation

    def restriction(f, q):
        ret = {}
        # TODO :genericity with element operator ?
        for e in f.dom.nodes:
            ret[e] = q[f.apply(e)]
        for e in f.dom.edges:
            ret[e] = q[f.apply(e)]
        return ret

    def amalgamation(f, p, g, q):
        assert f.cod == g.cod
        ret = {}
        for e in f.dom.nodes():
            ret[f.apply(e)] = p[e]

        for e in g.dom.nodes():
            if ret.get(g.apply(e)) == None:
                ret[g.apply(e)] = q[e]
            elif ret[g.apply(e)] != q[e]:
                raise Exception("fail amalgamation")

        for e in f.dom.edges:
            ret[f.apply(e)] = p[e]

        for e in g.dom.edges:
            if ret.get(g.apply(e)) == None:
                ret[g.apply(e)] = q[e]
            elif ret[g.apply(e)] != q[e]:
                raise Exception("fail amalgamation")

        return ret

    def amalgamation_2_in_1(ret, g, q):
        for e in g.dom.nodes():
            if ret.get(g.apply(e)) == None:
                ret[g.apply(e)] = q[e]
            elif ret[g.apply(e)] != q[e]:
                raise Exception("fail amalgamation 2 in 1")

        for e in g.dom.edges:
            if ret.get(g.apply(e)) == None:
                ret[g.apply(e)] = q[e]
            elif ret[g.apply(e)] != q[e]:
                raise Exception("fail amalgamation 2 in 1")

    def amalgamation_quotient(f, p):
        ret = {}
        for e in f.dom.nodes():
            ret[f.apply(e)] = p[e]
        for e in f.dom.edges:
            ret[f.apply(e)] = p[e]

        return ret

    def phash(p): # TODO WHY NOT NEEDED, REMOVE ?
        r = 1
        # r = 31 * len(p.items())
        # for k, v in p.items():
        #     r ^= 31 * hash(k)
        #     r ^= 31 * hash(v)
        return r

    ParameterGraph = {
        'name'                  : "ParGraph",
        'parhash'               : phash,
        'restriction'           : restriction,
        'amalgamation'          : amalgamation,
        'amalgamation_2_in_1'   : amalgamation_2_in_1,
        'amalgamation_quotient' : amalgamation_quotient
    }
    CO, CM, C = Parametrisation.get(Graph, ParameterGraph)

    pfm = PFunctor.FamPFunctor.Maker(C, C)

    l0 = Graph.TO()()
    l0n0 = l0.add_node()
    r0 = lambda x : x

    # print("L0", l0)
    # print("R0", r0)

    g0 = pfm.add_fam_rule(l0, r0)

    l1 = Graph.TO()()
    l1n0 = l1.add_node()
    l1n1 = l1.add_node()
    l1e0 = l1.add_edge(l1n0, l1n1)
    r1 = Graph.TO()()
    r1n0 = r1.add_node()
    r1n1 = r1.add_node()
    r1n2 = r1.add_node()
    r1e01 = r1.add_edge(r1n0, r1n1)
    r1e12 = r1.add_edge(r1n1, r1n2)
    def r1_(x):
        assert x.OC == l1
        p = {r1n0: x.ET[l1n0],
            r1n1: ((x.ET[l1n0][0]+x.ET[l1n1][0])/2, (x.ET[l1n0][1]+x.ET[l1n1][1])/2, (x.ET[l1n0][2]+x.ET[l1n1][2])/2),
            r1n2: x.ET[l1n1],
            r1e01: x.ET[l1e0],
            r1e12: x.ET[l1e0]}
        r1p = CO(r1, p)
        return r1p

    # print("L1", l1)
    # print("R1", r1)

    g1 = pfm.add_fam_rule(l1, r1_)

    l2 = Graph.TO()()
    l2n0 = l2.add_node()
    l2n1 = l2.add_node()
    l2n2 = l2.add_node()
    l2e01 = l2.add_edge(l2n0, l2n1)
    l2e12 = l2.add_edge(l2n1, l2n2)
    l2e20 = l2.add_edge(l2n2, l2n0)
    r2 = Graph.TO()()
    r2n0  = r2.add_node()
    r2n01 = r2.add_node()
    r2n1  = r2.add_node()
    r2n12 = r2.add_node()
    r2n2  = r2.add_node()
    r2n20 = r2.add_node()
    r2e001 = r2.add_edge(r2n0, r2n01)
    r2e011 = r2.add_edge(r2n01, r2n1)
    r2e112 = r2.add_edge(r2n1, r2n12)
    r2e122 = r2.add_edge(r2n12, r2n2)
    r2e220 = r2.add_edge(r2n2, r2n20)
    r2e200 = r2.add_edge(r2n20, r2n0)
    r2e2012 = r2.add_edge(r2n20, r2n12)
    r2e1201 = r2.add_edge(r2n12, r2n01)
    r2e0120 = r2.add_edge(r2n01, r2n20)
    def r2_(x):
        assert x.OC == l2
        p = {r2n0: x.ET[l2n0],
            r2n01: ((x.ET[l2n0][0]+x.ET[l2n1][0])/2, (x.ET[l2n0][1]+x.ET[l2n1][1])/2, (x.ET[l2n0][2]+x.ET[l2n1][2])/2),
            r2n1: x.ET[l2n1],
            r2n12: ((x.ET[l2n1][0]+x.ET[l2n2][0])/2, (x.ET[l2n1][1]+x.ET[l2n2][1])/2, (x.ET[l2n1][2]+x.ET[l2n2][2])/2),
            r2n2: x.ET[l2n2],
            r2n20: ((x.ET[l2n2][0]+x.ET[l2n0][0])/2, (x.ET[l2n2][1]+x.ET[l2n0][1])/2, (x.ET[l2n2][2]+x.ET[l2n0][2])/2),
            r2e001: x.ET[l2e01],
            r2e011: x.ET[l2e01],
            r2e112: x.ET[l2e12],
            r2e122: x.ET[l2e12],
            r2e220: x.ET[l2e20],
            r2e200: x.ET[l2e20],
            r2e2012: (x.ET[l2e20]+x.ET[l2e12])/2,
            r2e1201: (x.ET[l2e12]+x.ET[l2e01])/2,
            r2e0120: (x.ET[l2e01]+x.ET[l2e20])/2}
        return CO(r2, p)

    # print("L2", l2)
    # print("R2", r2)

    g2 = pfm.add_fam_rule(l2, r2_)

    lhs010 = Graph.TM()(l0, l1, {l0n0: l1n0})

    lhs011 = Graph.TM()(l0, l1, {l0n0: l1n1})

    # print("LHS010", lhs010)
    # print("LHS011", lhs011)

    def rhs010(lps, lpo, rs, ro):
        # l2 => \ pl2. ... return (r2, pr2)
        #  /\
        #  |  => \ pl1, pl2, (r2,pr2), (r2, pr1) ... return f: (r1, pr1) -> (r2, pr2) 
        #  |i
        # l1 => \pl1. ... return (r1, pr1)
        gm = Graph.TM()(rs.OC, ro.OC, {l0n0: r1n0})
        return CM(rs, ro, gm)

    def rhs011(lps, lpo, rs, ro):
        gm = Graph.TM()(rs.OC, ro.OC, {l0n0: r1n2})
        return CM(rs, ro, gm)

    pfm.add_fam_inclusion(g0, g1, lhs010, rhs010)

    pfm.add_fam_inclusion(g0, g1, lhs011, rhs011)

    lhs120 = Graph.TM()(l1, l2, {l1n0: l2n0, l1n1: l2n1, l1e0: l2e01})

    lhs121 = Graph.TM()(l1, l2, {l1n0: l2n1, l1n1: l2n2, l1e0: l2e12})

    lhs122 = Graph.TM()(l1, l2, {l1n0: l2n2, l1n1: l2n0, l1e0: l2e20})

    # print("LHS120", lhs120)

    # print("LHS121", lhs121)

    # print("LHS122", lhs122)

    def rhs120(lps, lpo, rs, ro):
        gm = Graph.TM()(rs.OC, ro.OC, {0: 0, 1: 1, 2: 2, (0, 1, 0): (0, 1, 0), (1, 2, 0): (1, 2, 0)})
        gm = Graph.TM()(rs.OC, ro.OC, {r1n0: r2n0, r1n1: r2n01, r1n2: r2n1, r1e01: r2e001, r1e12: r2e011})
        return CM(rs, ro, gm)

    def rhs121(lps, lpo, rs, ro):
        gm = Graph.TM()(rs.OC, ro.OC, {0: 2, 1: 3, 2: 4, (0, 1, 0): (2, 3, 0), (1, 2, 0): (3, 4, 0)})
        gm = Graph.TM()(rs.OC, ro.OC, {r1n0: r2n1, r1n1: r2n12, r1n2: r2n2, r1e01: r2e112, r1e12: r2e122})
        return CM(rs, ro, gm)

    def rhs122(lps, lpo, rs, ro):
        gm = Graph.TM()(rs.OC, ro.OC, {0: 4, 1: 5, 2: 0, (0, 1, 0): (4, 5, 0), (1, 2, 0): (5, 0, 0)})
        gm = Graph.TM()(rs.OC, ro.OC, {r1n0: r2n2, r1n1: r2n20, r1n2: r2n0, r1e01: r2e220, r1e12: r2e200})
        return CM(rs, ro, gm)

    pfm.add_fam_inclusion(g1, g2, lhs120, rhs120)

    pfm.add_fam_inclusion(g1, g2, lhs121, rhs121)

    pfm.add_fam_inclusion(g1, g2, lhs122, rhs122)

    # AUTO
    lhs220 = Graph.TM()(l2, l2, {0: 1, 1: 2, 2: 0, (0, 1, 0): (1, 2, 0), (1, 2, 0): (2, 0, 0), (2, 0, 0): (0, 1, 0)})
    lhs220 = Graph.TM()(l2, l2, {l2n0: l2n1, l2n1: l2n2, l2n2: l2n0, l2e01: l2e12, l2e12: l2e20, l2e20: l2e01})

    lhs221 = Graph.TM()(l2, l2, {0: 2, 1: 0, 2: 1, (0, 1, 0): (2, 0, 0), (1, 2, 0): (0, 1, 0), (2, 0, 0): (1, 2, 0)})
    lhs221 = Graph.TM()(l2, l2, {l2n0: l2n2, l2n1: l2n0, l2n2: l2n1, l2e01: l2e20, l2e12: l2e01, l2e20: l2e12})

    def rhs220(lps, lpo, rs, ro):
        gm = Graph.TM()(rs.OC, ro.OC, {
            0: 2,
            1: 3,
            2: 4,
            3: 5,
            4: 0,
            5: 1,
            (0, 1, 0): (2, 3, 0),
            (1, 2, 0): (3, 4, 0),
            (2, 3, 0): (4, 5, 0),
            (3, 4, 0): (5, 0, 0),
            (4, 5, 0): (0, 1, 0),
            (5, 0, 0): (1, 2, 0),
            (5, 3, 0): (1, 5, 0),
            (3, 1, 0): (5, 3, 0),
            (1, 5, 0): (3, 1, 0)
        })
        gm = Graph.TM()(rs.OC, ro.OC, {
            r2n0: r2n1,
            r2n01: r2n12,
            r2n1: r2n2,
            r2n12: r2n20,
            r2n2: r2n0,
            r2n20: r2n01,
            r2e001: r2e112,
            r2e011: r2e122,
            r2e112: r2e220,
            r2e122: r2e200,
            r2e220: r2e001,
            r2e200: r2e011,
            r2e2012: r2e0120,
            r2e1201: r2e2012,
            r2e0120: r2e1201
        })
        return CM(rs, ro, gm)

    def rhs221(lps, lpo, rs, ro):
        gm = Graph.TM()(rs.OC, ro.OC, {
            0: 4,
            1: 5,
            2: 0,
            3: 1,
            4: 2,
            5: 3,
            (0, 1, 0): (4, 5, 0),
            (1, 2, 0): (5, 0, 0),
            (2, 3, 0): (0, 1, 0),
            (3, 4, 0): (1, 2, 0),
            (4, 5, 0): (2, 3, 0),
            (5, 0, 0): (3, 4, 0),
            (5, 3, 0): (3, 1, 0),
            (3, 1, 0): (1, 3, 0),
            (1, 5, 0): (5, 3, 0)
        })
        gm = Graph.TM()(rs.OC, ro.OC, {
            r2n0: r2n2,
            r2n01: r2n20,
            r2n1: r2n0,
            r2n12: r2n01,
            r2n2: r2n1,
            r2n20: r2n12,
            r2e001: r2e220,
            r2e011: r2e200,
            r2e112: r2e001,
            r2e122: r2e011,
            r2e220: r2e112,
            r2e200: r2e122,
            r2e2012: r2e1201,
            r2e1201: r2e0120,
            r2e0120: r2e2012
        })
        return CM(rs, ro, gm)

    pfm.add_fam_inclusion(g2, g2, lhs220, rhs220)

    pfm.add_fam_inclusion(g2, g2, lhs221, rhs221)

    pf = pfm.get()

    T = GT(pf)

    g = Graph.TO()()
    n1 = g.add_node()
    n2 = g.add_node()
    n3 = g.add_node()
    n4 = g.add_node()
    e12 = g.add_edge(n1,n2)
    e23 = g.add_edge(n2,n3)
    e31 = g.add_edge(n3,n1)
    e41 = g.add_edge(n4,n1)
    e14 = g.add_edge(n1,n4)
    e42 = g.add_edge(n4,n2)
    e24 = g.add_edge(n2,n4)
    e43 = g.add_edge(n4,n3)
    e34 = g.add_edge(n3,n4)
    p = {n1: (0.0, 0.0, 0.0), n2: (-0.5, 0.5, 0.0), n3 : (0.5, 0.5, 0.0), n4 : (0.0, 0.0, 0.5), e12 : 0.0, e23 : 0.0, e31 : 0.0, e41 : 0.0, e14 : 0.0, e42 : 0.0, e24 : 0.0, e43 : 0.0, e34 : 0.0}
    gp = CO(g, p)

    return T, gp 