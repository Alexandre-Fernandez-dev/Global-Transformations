import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from data.Open import Open
import data.Graph as GraphModule
from data.Graph import *
import matplotlib.pyplot as plt
from engine.PFunctor import FlatPFunctor
from engine.GT import GT

def divide_edges():
    OGraphO, OGraphM, OGraph = Open.get(Graph)
    epf = FlatPFunctor.Maker(Graph, OGraph)
    
    l0 = GraphO()
    nl0 = l0.add_node()
    r0 = l0
    nr0 = nl0

    R0 = OGraphO([ l0 ])
    g0 = epf.add_rule(l0, R0)

    l1 = GraphO()
    nl1_0 = l1.add_node()
    nl1_1 = l1.add_node()
    el1_0 = l1.add_edge(nl1_0, nl1_1)
    el1_1 = l1.add_edge(nl1_1, nl1_0)

    r1a = l1
    r1b = GraphO()
    nr1b_0 = r1b.add_node()
    nr1b_1 = r1b.add_node()
    nr1b_2 = r1b.add_node()
    er1b_0 = r1b.add_edge(nr1b_0, nr1b_1)
    er1b_1 = r1b.add_edge(nr1b_1, nr1b_0)
    er1b_2 = r1b.add_edge(nr1b_1, nr1b_2)
    er1b_3 = r1b.add_edge(nr1b_2, nr1b_1)

    R1 = OGraphO([r1a, r1b])
    g1 = epf.add_rule(l1, R1)

    l01_0 = GraphM(l0, l1, {
        nl0 : nl1_0
    })

    r01_0a = l01_0
    r01_0b = GraphM(r0, r1b, {
        nl0 : nr1b_0
    })
    r01_0 = OGraphM(R0, R1, [0, 0], [r01_0a, r01_0b])

    i01_0 = epf.add_inclusion(g0, g1, l01_0, r01_0)


    # l01_1 = GraphM(l0, l1, {
    #     nl0 : nl1_1
    # })

    # r01_1a = l01_1
    # r01_1b = GraphM(r0, r1b, {
    #     nl0 : nr1b_2
    # })

    # r01_1 = OGraphM(R0, R1, [0, 0], [r01_1a, r01_1b])
    # i01_1 = epf.add_inclusion(g0, g1, l01_1, r01_1)
    
    l11 = GraphM(l1, l1, {
        nl1_0 : nl1_1,
        nl1_1 : nl1_0,
        el1_0 : el1_1,
        el1_1 : el1_0
    })

    r11a = l11

    r11b = GraphM(r1b, r1b, {
        nr1b_0 : nr1b_2,
        nr1b_1 : nr1b_1,
        nr1b_2 : nr1b_0,
        er1b_0 : er1b_3,
        er1b_1 : er1b_2,
        er1b_2 : er1b_1,
        er1b_3 : er1b_0,
    })

    r11 = OGraphM(R1, R1, [0, 1], [r11a, r11b])
    i11 = epf.add_inclusion(g1, g1, l11, r11)

    l01_1 = l01_0.compose(l11)
    r01_1 = r01_0.compose(r11)
    i01_1 = epf.add_inclusion(g0, g1, l01_1, r01_1)

    pfT = epf.get()
    T = GT(pfT)

    g = GraphO()
    n1 = g.add_node()
    n2 = g.add_node()
    n3 = g.add_node()
    e12 = g.add_edge(n1,n2)
    e21 = g.add_edge(n2,n1)
    e23 = g.add_edge(n2,n3)
    e32 = g.add_edge(n3,n2)
    e31 = g.add_edge(n3,n1)
    e13 = g.add_edge(n1,n3)
    print(len(g.g.nodes))

    #plt.subplot(121)
    options = {
        'node_color': 'black',
        'node_size': 20,
        'width': 1,
    }

    GraphModule.show = False
    nx.draw_kamada_kawai(g.g, **options)
    # plt.show()
    for i in range(0, 3):
        #if i == 3:
        GraphModule.show = True
        g_ = T.extend(g)
        g = g_.object
        nx.draw_kamada_kawai(g.g, **options)
        plt.show()

def divide_edges_add_node():
    OGraphO, OGraphM, OGraph = Open.get(Graph)
    epf = FlatPFunctor.Maker(Graph, OGraph)
    
    #rules
    l0 = GraphO()
    nl0 = l0.add_node()
    r0 = l0
    nr0 = nl0

    R0 = OGraphO([ l0 ])
    g0 = epf.add_rule(l0, R0)

    l1 = GraphO()
    nl1_0 = l1.add_node()
    nl1_1 = l1.add_node()
    el1_0 = l1.add_edge(nl1_0, nl1_1)
    el1_1 = l1.add_edge(nl1_1, nl1_0)

    r1a = l1
    r1b = GraphO()
    nr1b_0 = r1b.add_node()
    nr1b_1 = r1b.add_node()
    nr1b_2 = r1b.add_node()
    er1b_0 = r1b.add_edge(nr1b_0, nr1b_1)
    er1b_1 = r1b.add_edge(nr1b_1, nr1b_0)
    er1b_2 = r1b.add_edge(nr1b_1, nr1b_2)
    er1b_3 = r1b.add_edge(nr1b_2, nr1b_1)

    R1 = OGraphO([r1a, r1b])
    g1 = epf.add_rule(l1, R1)

    l2 = r1b
    r2a = l2
    r2b = GraphO()
    nr2b_0 = r2b.add_node()
    nr2b_1 = r2b.add_node()
    nr2b_2 = r2b.add_node()
    nr2b_3 = r2b.add_node()
    er2b_0 = r2b.add_edge(nr2b_0, nr2b_1)
    er2b_1 = r2b.add_edge(nr2b_1, nr2b_0)
    er2b_2 = r2b.add_edge(nr2b_1, nr2b_2)
    er2b_3 = r2b.add_edge(nr2b_2, nr2b_1)
    er2b_4 = r2b.add_edge(nr2b_2, nr2b_3)
    er2b_5 = r2b.add_edge(nr2b_3, nr2b_2)

    r2c = r2b
    r2d = GraphO()
    nr2d_0 = r2d.add_node()
    nr2d_1 = r2d.add_node()
    nr2d_2 = r2d.add_node()
    nr2d_3 = r2d.add_node()
    nr2d_4 = r2d.add_node()
    nr2d_5 = r2d.add_node()
    er2d_0 = r2d.add_edge(nr2d_0, nr2d_1)
    er2d_1 = r2d.add_edge(nr2d_1, nr2d_0)
    er2d_2 = r2d.add_edge(nr2d_1, nr2d_2)
    er2d_3 = r2d.add_edge(nr2d_2, nr2d_1)
    er2d_4 = r2d.add_edge(nr2d_2, nr2d_3)
    er2d_5 = r2d.add_edge(nr2d_3, nr2d_2)
    er2d_6 = r2d.add_edge(nr2d_3, nr2d_4)
    er2d_7 = r2d.add_edge(nr2d_4, nr2d_3)
    er2d_8 = r2d.add_edge(nr2d_2, nr2d_5)

    R2 = OGraphO([r2a, r2b, r2c, r2d])
    g2 = epf.add_rule(l2, R2)

    #inclusions
    l01_0 = GraphM(l0, l1, {
        nl0 : nl1_0
    })
    l01_0.name

    r01_0a = l01_0
    r01_0a.name = "r01_0a"
    r01_0b = GraphM(r0, r1b, {
        nl0 : nr1b_0
    })
    r01_0b.name = "r01_0b"
    r01_0 = OGraphM(R0, R1, [0, 0], [r01_0a, r01_0b])

    i01_0 = epf.add_inclusion(g0, g1, l01_0, r01_0)

    l01_1 = GraphM(l0, l1, {
        nl0 : nl1_1
    })

    r01_1a = l01_1
    r01_1a.name = "r01_1a"
    r01_1b = GraphM(r0, r1b, {
        nl0 : nr1b_2
    })
    r01_1b.name = "r01_1b"

    r01_1 = OGraphM(R0, R1, [0, 0], [r01_1a, r01_1b])
    i01_1 = epf.add_inclusion(g0, g1, l01_1, r01_1)

    l11 = GraphM(l1, l1, {
        nl1_0 : nl1_1,
        nl1_1 : nl1_0,
        el1_0 : el1_1,
        el1_1 : el1_0
    })

    r11a = l11
    r11a.name = "r11a"

    r11b = GraphM(r1b, r1b, {
        nr1b_0 : nr1b_2,
        nr1b_1 : nr1b_1,
        nr1b_2 : nr1b_0,
        er1b_0 : er1b_3,
        er1b_1 : er1b_2,
        er1b_2 : er1b_1,
        er1b_3 : er1b_0,
    })
    r11b.name = "r11b"

    r11 = OGraphM(R1, R1, [0, 1], [r11a, r11b])
    i11 = epf.add_inclusion(g1, g1, l11, r11)
    
    l12_1 = GraphM(l1, l2, {
        nl1_0 : nr1b_0,
        nl1_1 : nr1b_1,
        el1_0 : er1b_0,
        el1_1 : er1b_1
    })

    r12_1a = l12_1
    r12_1a.name = "r12_1a"

    r12_1b = GraphM(r1a, r2b, {
        nl1_0 : nr2b_0,
        nl1_1 : nr2b_1,
        el1_0 : er2b_0,
        el1_1 : er2b_1
    })
    r12_1b.name = "r12_1b"

    r12_1c = GraphM(r1b, r2c, {
        nr1b_0 : nr2b_0,
        nr1b_1 : nr2b_1,
        nr1b_2 : nr2b_2,
        er1b_0 : er2b_0,
        er1b_1 : er2b_1,
        er1b_2 : er2b_2,
        er1b_3 : er2b_3
    })
    r12_1c.name = "r12_1c"

    r12_1d = GraphM(r1b, r2d, {
        nr1b_0 : nr2d_0,
        nr1b_1 : nr2d_1,
        nr1b_2 : nr2d_2,
        er1b_0 : er2d_0,
        er1b_1 : er2d_1,
        er1b_2 : er2d_2,
        er1b_3 : er2d_3
    })
    r12_1d.name = "r12_1d"

    r12_1 = OGraphM(R1, R2, [0, 0, 1, 1], [r12_1a, r12_1b, r12_1c, r12_1d])
    i12_1 = epf.add_inclusion(g1, g2, l12_1, r12_1)

    l12_1p = l11.compose(l12_1)
    r12_1p = r11.compose(r12_1)
    i12_1p = epf.add_inclusion(g1, g2, l12_1p, r12_1p)

    l22 = r11b
    r22a = l22
    r22a.name = "r22a"

    r22b = GraphM(r2c, r2b, {
        nr2b_0 : nr2b_3,
        nr2b_1 : nr2b_2,
        nr2b_2 : nr2b_1,
        nr2b_3 : nr2b_0,
        er2b_0 : er2b_5,
        er2b_1 : er2b_4,
        er2b_2 : er2b_3,
        er2b_3 : er2b_2,
        er2b_4 : er2b_1,
        er2b_5 : er2b_0
    })
    r22b.name = "r22b"

    r22c = GraphM(r2b, r2c, {
        nr2b_0 : nr2b_3,
        nr2b_1 : nr2b_2,
        nr2b_2 : nr2b_1,
        nr2b_3 : nr2b_0,
        er2b_0 : er2b_5,
        er2b_1 : er2b_4,
        er2b_2 : er2b_3,
        er2b_3 : er2b_2,
        er2b_4 : er2b_1,
        er2b_5 : er2b_0
    })
    r22c.name = "r22c"

    r22d = GraphM(r2d, r2d, {
        nr2d_0 : nr2d_4,
        nr2d_1 : nr2d_3,
        nr2d_2 : nr2d_2,
        nr2d_3 : nr2d_1,
        nr2d_4 : nr2d_0,
        er2d_0 : er2d_7,
        er2d_1 : er2d_6,
        er2d_2 : er2d_5,
        er2d_3 : er2d_4,
        er2d_4 : er2d_3,
        er2d_5 : er2d_2,
        er2d_6 : er2d_1,
        er2d_7 : er2d_0
    })
    r22d.name = "r22d"

    r22 = OGraphM(R2, R2, [0, 2, 1, 3], [r22a, r22b, r22c, r22d])
    i22 = epf.add_inclusion(g2, g2, l22, r22)

    l12_2 = l12_1.compose(l22)
    r12_2 = r12_1.compose(r22)
    # l = ["a", "b", "c", "d"]
    # for i in range(0, 4):
    #     r12_2.ev[i].name = "r12_2" + l[i]
    i12_2 = epf.add_inclusion(g1, g2, l12_2, r12_2)

    l12_2p = l12_1p.compose(l22)
    r12_2p = r12_1p.compose(r22)
    i12_2p = epf.add_inclusion(g1, g2, l12_2p, r12_2p)
    print(r12_2p.projL)

    pfT = epf.get()
    T = GT(pfT)

    g = GraphO()
    n1 = g.add_node()
    n2 = g.add_node()
    n3 = g.add_node()
    n4 = g.add_node()
    e12 = g.add_edge(n1,n2)
    e21 = g.add_edge(n2,n1)
    e23 = g.add_edge(n2,n3)
    e32 = g.add_edge(n3,n2)
    e23 = g.add_edge(n3,n4)
    e32 = g.add_edge(n4,n3)
    e23 = g.add_edge(n4,n1)
    e32 = g.add_edge(n1,n4)
    print(len(g.g.nodes))

    options = {
        'node_color': 'black',
        'node_size': 20,
        'width': 1,
    }

    GraphModule.show = False
    nx.draw_kamada_kawai(g.g, **options)
    plt.show()
    for i in range(0, 3):
        #if i == 3:
        GraphModule.show = True
        g_ = T.extend(g)
        g = g_.object
        nx.draw_kamada_kawai(g.g, **options)
        plt.show()

def divide_tri():
    OGraphO, OGraphM, OGraph = Open.get(Graph)
    epf = FlatPFunctor.Maker(Graph, OGraph)
    
    class G:
        def __init__(self, g, n, e):
            self.g = g
            self.n = n
            self.e = e
    class M:
        def __init(self, g1, g2, d):
            pass

    def graph_sym(i, l):
        g = GraphO()
        n = [ g.add_node() for _ in range(0, i) ]
        e = [ g.add_edge(es[u], es[v])
            for es in l
            for i in range(len(es) - 1)
            for u, v in [ (i, (i+1) % len(es)), ((i+1) % len(es), i) ]
            ]
        return G(g, n, e)
    
    def graph_m_sym(g1, g2, d):
        assert isinstance(g1, G) and isinstance(g2, G)
        dk = list(d.keys())
        for n1 in dk:
            for n2 in dk:
                if (n1, n2, 0) in g1.e:
                    d[(n1, n2, 0)] = (d[n1], d[n2], 0)
        return GraphM(g1.g, g2.g, d)
    
    node = graph_sym(1, [])
    edge = graph_sym(2, [ [0, 1] ])
    tri  = graph_sym(3, [ [0, 1, 2, 0] ])

    edge2 = graph_sym(3, [ [0, 2], [2, 1] ])

    tri2  = graph_sym(4, [ [0, 3, 1, 2, 0], [3, 2] ])

    tri3  = graph_sym(5, [ [0, 3, 1, 4, 2, 0], [3, 2], [3, 4] ])

    tri4  = graph_sym(6, [ [0, 3, 1, 4, 2, 5, 0], [3, 4], [4, 5], [5, 3] ])

    node_edge = graph_m_sym(node, edge, { 0: 0 })

    edge_edge = graph_m_sym(edge, edge, { 0: 1, 1: 0})

    edge_tri = { (i, j) : graph_m_sym(edge, tri, { 0: i, 1: j })
                    for (i, j) in [(0, 1), (1, 0), (1, 2), (2, 1), (2, 0), (0, 2)] }

    tri_tri_r = graph_m_sym(tri,  tri,  { 0: 1, 1: 2, 2: 0})
    tri_tri_f2 = graph_m_sym(tri,  tri,  { 0: 1, 1: 0, 2: 2})

    mids = { (0, 1) : 3, (1, 2) : 4, (2, 0) : 5}
    mids.update({ (j, i) : v for ((i, j), v) in mids.items()})

    node_edge2 = graph_m_sym(node, edge2, { 0: 0 })
    
    edge2_edge2 = graph_m_sym(edge2, edge2, { 0: 1, 2: 2, 1: 0})

    edge_tri2 = { (i, j) : graph_m_sym(edge, tri2, { 0: i, 1: j })
                    for (i, j) in [(1, 2), (2, 1), (2, 0), (0, 2)] }

    edge2_tri2 = { (i, j) : graph_m_sym(edge2, tri2, { 0: i, 2: mids[i, j], 1: j })
                    for (i, j) in [(0, 1), (1, 0)]}

    edge_tri3 = { (i, j) : graph_m_sym(edge, tri3, { 0: i, 1: j })
                    for (i, j) in [(2, 0), (0, 2)]}
    edge2_tri3 = { (i, j) : graph_m_sym(edge2, tri3, { 0: i, 2: mids[i, j], 1: j })
                    for (i, j) in [(0, 1), (1, 0), (1, 2), (2, 1)]}

    edge2_tri4 = { (i, j) : graph_m_sym(edge2, tri4, { 0: i, 2: mids[i, j], 1: j })
                    for (i, j) in [(0, 1), (1, 0), (1, 2), (2, 1), (2, 0), (0, 2)]}

    # mm = [ node_edge, edge_tri, node_edge2, edge2_tri2_01, edge_tri2_12, edge_tri2_20, edge2_tri3_01, edge2_tri3_12, edge_tri3_20, edge2_tri4_01, edge2_tri4_12, edge2_tri4_20 ]
    # import data.Graph as GraphModule
    # for m in mm:
    #     GraphModule.draw([m], [m], "COUCOU")
    
    tri2_tri2_id  = graph_m_sym(tri2, tri2, { i: i for i in tri2.n })
    tri2_tri2_f2  = graph_m_sym(tri2, tri2, { 0: 1, 3: 3, 1: 0, 2 : 2})
    
    tri3_tri3_id  = graph_m_sym(tri3, tri3, { i: i for i in tri3.n })

    tri4_tri4_r   = graph_m_sym(tri4, tri4, { 0: 1, 3: 4, 1: 2, 4: 5, 2: 0, 5: 3 })
    tri4_tri4_f2  = graph_m_sym(tri4, tri4, { 0: 1, 3: 3, 1: 0, 4: 5, 2: 2, 5: 4 })

    r0 = OGraphO([ node.g ])
    g0 = epf.add_rule(node.g, r0)

    r1 = OGraphO([ edge.g, edge2.g ])
    g1 = epf.add_rule(edge.g, r1)

    r2 = OGraphO([ tri.g, tri2.g, tri2.g, tri2.g, tri3.g, tri3.g, tri3.g, tri3.g, tri3.g, tri3.g, tri4.g ])
    g2 = epf.add_rule(tri.g, r2)


    r01_0 = OGraphM(r0, r1, [0, 0], [node_edge, node_edge2])
    _, _, g01_0 = epf.add_inclusion(g0, g1, node_edge, r01_0)

    r11 = OGraphM(r1, r1, [0, 1], [edge_edge, edge2_edge2])
    _, _, g11 = epf.add_inclusion(g1, g1, edge_edge, r11)

    ass = [(0, edge_tri[0, 1]),
           (1, edge2_tri2[0, 1]),
           (0, edge_tri2[2, 0]),
           (0, edge_tri2[1, 2]),
           (1, edge2_tri3[0, 1]),
           (1, edge2_tri3[2, 1]),
           (1, edge2_tri3[1, 2]),
           (1, edge2_tri3[1, 0]),
           (0, edge_tri3[2, 0]),
           (0, edge_tri3[0, 2]),
           (1, edge2_tri4[0, 1])]
    proj = [ i for i, j in ass ]
    ev   = [ j for i, j in ass ]
    r12_01 = OGraphM(r1, r2, proj, ev)

    _, _, g12_01 = epf.add_inclusion(g1, g2, edge_tri[0, 1], r12_01)

    ass = [(0, edge_tri[1, 2]),
           (0, edge_tri2[1, 2]),
           (1, edge2_tri2[0, 1]),
           (0, edge_tri2[2, 0]),
           (1, edge2_tri3[1, 2]),
           (1, edge2_tri3[1, 0]),
           (0, edge_tri3[2, 0]),
           (0, edge_tri3[0, 2]),
           (1, edge2_tri3[0, 1]),
           (1, edge2_tri3[2, 1]),
           (1, edge2_tri4[1, 2])]
    proj = [ i for i, j in ass ]
    ev   = [ j for i, j in ass ]
    r12_12 = OGraphM(r1, r2, proj, ev)

    _, _, g12_12 = epf.add_inclusion(g1, g2, edge_tri[1, 2], r12_12)

    ass = [(0, edge_tri[2, 0]),
           (0, edge_tri2[2, 0]),
           (0, edge_tri2[1, 2]),
           (1, edge2_tri2[0, 1]),
           (0, edge_tri3[2, 0]),
           (0, edge_tri3[0, 2]),
           (1, edge2_tri3[0, 1]),
           (1, edge2_tri3[2, 1]),
           (1, edge2_tri3[1, 2]),
           (1, edge2_tri3[1, 0]),
           (1, edge2_tri4[2, 0])]
    proj = [ i for i, j in ass ]
    ev   = [ j for i, j in ass ]
    r12_20 = OGraphM(r1, r2, proj, ev)

    _, _, g12_20 = epf.add_inclusion(g1, g2, edge_tri[2, 0], r12_20)

    ######
    ass = [(0, tri_tri_r),
           (3, tri2_tri2_id),
           (1, tri2_tri2_id),
           (2, tri2_tri2_id),
           (6, tri3_tri3_id),
           (7, tri3_tri3_id),
           (8, tri3_tri3_id),
           (9, tri3_tri3_id),
           (4, tri3_tri3_id),
           (5, tri3_tri3_id),
           (10, tri4_tri4_r)]
    proj = [ i for i, j in ass ]
    ev   = [ j for i, j in ass ]
    r22_r = OGraphM(r2, r2, proj, ev)

    _, _, g22_r = epf.add_inclusion(g2, g2, tri_tri_r, r22_r)

    ass = [(0, tri_tri_f2),
           (1, tri2_tri2_f2),
           (3, tri2_tri2_f2),
           (2, tri2_tri2_f2),
           (7, tri3_tri3_id),
           (6, tri3_tri3_id),
           (5, tri3_tri3_id),
           (4, tri3_tri3_id),
           (9, tri3_tri3_id),
           (8, tri3_tri3_id),
           (10, tri4_tri4_f2)]

    proj = [ i for i, j in ass ]
    ev   = [ j for i, j in ass ]
    r22_f2 = OGraphM(r2, r2, proj, ev)

    _, _, g22_f2 = epf.add_inclusion(g2, g2, tri_tri_f2, r22_f2)

    #### compose
    l = [ (g01_0, g11),
      (g11, g12_01),
      (g11, g12_12),
      (g11, g12_20),
      (g22_r, g22_f2),
      (g22_f2, g22_r),
      (g22_r, g22_r) ]
    for f, g in l:
        epf.add_inclusion(f.g_a, g.g_b, f.lhs.compose(g.lhs), f.rhs.compose(g.rhs))

    ####

    # node = GraphO()
    # node_n = [ node.add_node() ]

    # edge = GraphO()
    # edge_n = [ edge.add_node() for _ in range(0, 2) ]
    # edge_e = [ edge.add_edge(edge_n[0], edge_n[1]), edge.add_edge(edge_n[1], edge_n[0]) ]

    # tri = GraphO()
    # tri_n = [ tri.add_node() for _ in range(0, 3) ]
    # tri_e = [ tri.add_edge(tri_n[i], tri_n[(i + 1) % 3]) for i in range(0, 3) ]

    # edged = GraphO()
    # edged_n = [ edged.add_node() for _ in range(0, 3) ]
    # edged_e = [ edged.add_edge(edged_n[i], edged_n[(i + 1) % 3]) for i in range(0, 3) ]

    # print("g0")
    # for i in g0.self_inclusions:
    #     print(i.lhs)
    # print("g1")
    # for i in g1.self_inclusions:
    #     print(i.lhs)
    # print("g2")
    # for i in g2.self_inclusions:
    #     print(i.lhs)

    pfT = epf.get()
    T = GT(pfT)

    #carré
    # g = GraphO()
    g = tri4.g
    
    # print(len(g.g.nodes))

    options = {
        'node_color': 'black',
        'node_size': 20,
        'width': 1,
    }

    print("i =", 0)
    print("nodes :", len(g.nodes))
    print("edges :", len(g.edges))
    GraphModule.show = False
    # mng = plt.get_current_fig_manager()
    # mng.full_screen_toggle()
    nx.draw_kamada_kawai(g.g, **options)
    plt.show()
    for i in range(0, 6):
        #if i == 3:
        # GraphModule.show = True
        g_ = T.extend(g)
        g = g_.object.LO[g_.object.i]
        print("i =", i+1)
        print("nodes :", len(g.nodes))
        print("edges :", len(g.edges))
        print("waiting for draw...")
        # mng = plt.get_current_fig_manager()
        # mng.full_screen_toggle()
        nx.draw_kamada_kawai(g.g, **options)
        plt.show()

if __name__ == "__main__":
    # divide_edges()
    # divide_edges_add_node()
    divide_tri()