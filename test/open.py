import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

import networkx as nx
import matplotlib.pyplot as plt
from src.libgt.data.Open import Open
from src.libgt.data.Graph import Graph, GraphO, GraphM
import src.libgt.data.Graph as GraphModule
from src.libgt.engine.PFunctor import FlatPFunctor, FamPFunctor
from src.libgt.engine.GT import GT
from src.libgt.data.Sheaf import Parametrisation
from src.libgt.data.Gmap import Premap, PremapO, PremapM

def divide_edges(show = 0):
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
    # print(len(g.g.nodes))

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

def divide_edges_add_node(show = False):
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
    # print(r12_2p.projL)

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
    # print(len(g.g.nodes))

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

def divide_tri(show = False):
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

    # print("i =", 0)
    # print("nodes :", len(g.nodes))
    # print("edges :", len(g.edges))
    if show > 0:
        options = {
            'node_color': 'black',
            'node_size': 20,
            'width': 1,
        }
        # mng = plt.get_current_fig_manager()
        # mng.full_screen_toggle()
        nx.draw_kamada_kawai(g.g, **options)
        plt.show()

    for i in range(0, 6):
        if show == 2:
            GraphModule.show = True
        g_ = T.extend(g)
        g = g_.LO[0]
        print("i =", i+1)
        print("nodes :", len(g.nodes))
        print("edges :", len(g.edges))
        if show > 0:
            print("waiting for draw...")
            # mng = plt.get_current_fig_manager()
            # mng.full_screen_toggle()
            nx.draw_kamada_kawai(g.g, **options)
            plt.show()
    
class Test:
    @staticmethod
    def sierpinsky():
        def restriction(f, q):
            ret = {}
            for e in f.dom.nodes:
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

            return ret

        def amalgamation_2_in_1(ret, g, q):
            for e in g.dom.nodes():
                if ret.get(g.apply(e)) == None:
                    ret[g.apply(e)] = q[e]
                elif ret[g.apply(e)] != q[e]:
                    raise Exception("fail amalgamation 2 in 1")

        def phash(p): # TODO WHY NOT NEEDED, REMOVE ?
            r = 1
            return r

        ParameterGraph = {
            'name'                  : "ParGraph",
            'parhash'               : phash,
            'restriction'           : restriction,
            'amalgamation'          : amalgamation,
            'amalgamation_2_in_1'   : amalgamation_2_in_1,
        }
        CO, CM, C = Parametrisation.get(Graph, ParameterGraph)
        COO, CMO, C_O = Open.get(C)

        pfm = FamPFunctor.Maker(C, C_O)

        l0 = Graph.TO()()
        l0n0 = l0.add_node()
        r0 = lambda x : COO([ x ])

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
        r1e12 = r1.add_edge(r1n2, r1n1)
        def r1_(x):
            assert x.OC == l1
            p = {r1n0: x.ET[l1n0],
                r1n1: ((x.ET[l1n0][0]+x.ET[l1n1][0])/2, (x.ET[l1n0][1]+x.ET[l1n1][1])/2, (x.ET[l1n0][2]+x.ET[l1n1][2])/2),
                r1n2: x.ET[l1n1],
            }
            r1p = CO(r1, p)
            return COO([ x, r1p ])

        g1 = pfm.add_fam_rule(l1, r1_)

        l2 = Graph.TO()()
        l2n0 = l2.add_node()
        l2n1 = l2.add_node()
        l2n2 = l2.add_node()
        l2e01 = l2.add_edge(l2n0, l2n1)
        l2e12 = l2.add_edge(l2n2, l2n1)
        l2e20 = l2.add_edge(l2n2, l2n0)
        r2 = Graph.TO()()
        r2n0  = r2.add_node()
        r2n01 = r2.add_node()
        r2n1  = r2.add_node()
        r2n12 = r2.add_node()
        r2n2  = r2.add_node()
        r2n20 = r2.add_node()
        r2e001 = r2.add_edge(r2n0, r2n01)
        r2e011 = r2.add_edge(r2n1, r2n01)
        r2e112 = r2.add_edge(r2n1, r2n12)
        r2e122 = r2.add_edge(r2n2, r2n12)
        r2e220 = r2.add_edge(r2n2, r2n20)
        r2e200 = r2.add_edge(r2n0, r2n20)
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
            }
            r2p = CO(r2, p)
            return COO([ x, r2p ])

        g2 = pfm.add_fam_rule(l2, r2_)

        lhs010 = Graph.TM()(l0, l1, {l0n0: l1n0})

        lhs011 = Graph.TM()(l0, l1, {l0n0: l1n1})

        def rhs010(lps, lpo, rs, ro):
            r010 = CM(rs.LO[0], ro.LO[0], lhs010)
            gmp = Graph.TM()(rs.LO[0].OC, ro.LO[1].OC, {l0n0: r1n0})
            r010p = CM(rs.LO[0], ro.LO[1], gmp)
            return CMO(rs, ro, [0, 0], [r010, r010p])

        def rhs011(lps, lpo, rs, ro):
            r011 = CM(rs.LO[0], ro.LO[0], lhs011)
            gmp = Graph.TM()(rs.LO[0].OC, ro.LO[1].OC, {l0n0: r1n2})
            r011p = CM(rs.LO[0], ro.LO[1], gmp)
            return CMO(rs, ro, [0, 0], [r011, r011p])

        pfm.add_fam_inclusion(g0, g1, lhs010, rhs010)

        pfm.add_fam_inclusion(g0, g1, lhs011, rhs011)

        lhs120 = Graph.TM()(l1, l2, {l1n0: l2n0, l1n1: l2n1, l1e0: l2e01})

        lhs121 = Graph.TM()(l1, l2, {l1n0: l2n2, l1n1: l2n1, l1e0: l2e12})

        lhs122 = Graph.TM()(l1, l2, {l1n0: l2n2, l1n1: l2n0, l1e0: l2e20})

        def rhs120(lps, lpo, rs, ro):
            r120 = CM(rs.LO[0], ro.LO[0], lhs120)
            gmp = Graph.TM()(rs.LO[1].OC, ro.LO[1].OC, {r1n0: r2n0, r1n1: r2n01, r1n2: r2n1, r1e01: r2e001, r1e12: r2e011})
            r120p = CM(rs.LO[1], ro.LO[1], gmp)
            return CMO(rs, ro, [0, 1], [r120, r120p])

        def rhs121(lps, lpo, rs, ro):
            r121 = CM(rs.LO[0], ro.LO[0], lhs121)
            gmp = Graph.TM()(rs.LO[1].OC, ro.LO[1].OC, {r1n0: r2n2, r1n1: r2n12, r1n2: r2n1, r1e01: r2e112, r1e12: r2e122})
            r121p = CM(rs.LO[1], ro.LO[1], gmp)
            return CMO(rs, ro, [0, 1], [r121, r121p])

        def rhs122(lps, lpo, rs, ro):
            r122 = CM(rs.LO[0], ro.LO[0], lhs122)
            gmp = Graph.TM()(rs.LO[1].OC, ro.LO[1].OC, {r1n0: r2n2, r1n1: r2n20, r1n2: r2n0, r1e01: r2e220, r1e12: r2e200})
            r122p = CM(rs.LO[1], ro.LO[1], gmp)
            return CMO(rs, ro, [0, 1], [r122, r122p])

        pfm.add_fam_inclusion(g1, g2, lhs120, rhs120)

        pfm.add_fam_inclusion(g1, g2, lhs121, rhs121)

        pfm.add_fam_inclusion(g1, g2, lhs122, rhs122)

        pf = pfm.get()

        T = GT(pf)

        g = Graph.TO()()
        n1 = g.add_node()
        n2 = g.add_node()
        n3 = g.add_node()
        e12 = g.add_edge(n1,n2)
        e23 = g.add_edge(n3,n2)
        e31 = g.add_edge(n3,n1)
        p = {n1: (0.0, 0.0, 1.41*1.73/2), n2: (-0.5, 0.5, 0.0), n3 : (0.5, -0.5, 0.0)}
        gp = CO(g, p)

        return T, gp 
        
    @staticmethod
    def rivers():

        def restriction(f, q):
            ret = {}
            # print(f)
            # print("f.dom", f.dom)
            # print("f.cod", f.cod)
            # print()
            # print(q)
            for n in f.dom.iter_icells(0):
                ret[n] = q[f.cod.get_icell(0, f.apply(n))]
            for e in f.dom.iter_icells(1):
                # print(e)
                te  = f.dom.get_icell(2, e)
                tep  = f.dom.get_icell(2, f.dom.alpha(2, e))
                # print(e, te)
                # print(e, tep)
                ret[e, te]   = q[ f.cod.get_icell(1, f.apply(e)),
                                  f.cod.get_icell(2, f.apply(te)) ]
                ret[e, tep]  = q[ f.cod.get_icell(1, f.apply(e)),
                                  f.cod.get_icell(2, f.apply(tep)) ]
            return ret

        def amalgamation(f, p, g, q):
            assert f.cod == g.cod
            ret = {}
            for n in f.dom.iter_icells(0):
                # print(p)
                # print(n)
                ret[f.cod.get_icell(0, f.apply(n))] = p[n]

            for n in g.dom.iter_icells(0):
                gn = g.cod.get_icell(0, g.apply(n))
                if gn not in ret:
                    ret[gn] = q[n]
                elif ret[gn] != q[n]:
                    raise Exception("fail amalgamation")
            
            for e in f.dom.iter_icells(1):
                te  = f.dom.get_icell(2, e)
                tep  = f.dom.get_icell(2, f.dom.alpha(2, e))
                ret[ f.cod.get_icell(1, f.apply(e)),
                     f.cod.get_icell(2, f.apply(te)) ] = p[e, te]
                ret[ f.cod.get_icell(1, f.apply(e)),
                     f.cod.get_icell(2, f.apply(tep)) ] = p[e, tep]
            
            for e in g.dom.iter_icells(1):
                te  = g.dom.get_icell(2, e)
                ke = (g.cod.get_icell(1, g.apply(e)), g.cod.get_icell(2, g.apply(te)))
                if ke not in ret:
                    ret[ke] = q[e, te]
                elif ret[ke] != q[e, te]:
                    raise Exception("fail amalgamation")
                tep = g.dom.get_icell(2, g.dom.alpha(2, e))
                kep = (g.cod.get_icell(1, g.apply(e)), g.cod.get_icell(2, g.apply(tep)))
                if kep not in ret:
                    ret[kep] = q[e, tep]
                elif ret[kep] != q[e, tep]:
                    raise Exception("fail amalgamation")
            

            return ret

        def amalgamation_2_in_1(ret, g, q):
            for n in g.dom.iter_icells(0):
                gn = g.cod.get_icell(0, g.apply(n))
                if gn not in ret:
                    ret[gn] = q[n]
                elif ret[gn] != q[n]:
                    raise Exception("fail amalgamation 2 in 1")

            for e in g.dom.iter_icells(1):
                te  = g.dom.get_icell(2, e)
                ke = (g.cod.get_icell(1, g.apply(e)), g.cod.get_icell(2, g.apply(te)))
                if ke not in ret:
                    ret[ke] = q[e, te]
                elif ret[ke] != q[e, te]:
                    raise Exception("fail amalgamation")
                tep = g.dom.get_icell(2, g.dom.alpha(2, e))
                kep = (g.cod.get_icell(1, g.apply(e)), g.cod.get_icell(2, g.apply(tep)))
                if kep not in ret:
                    ret[kep] = q[e, tep]
                elif ret[kep] != q[e, tep]:
                    raise Exception("fail amalgamation")

        def phash(p): # TODO WHY NOT NEEDED, REMOVE ?
            r = 1
            return r

        ParNodesGmap = {
            'name'                  : "ParNodeGmap",
            'parhash'               : phash,
            'restriction'           : restriction,
            'amalgamation'          : amalgamation,
            'amalgamation_2_in_1'   : amalgamation_2_in_1
        }

        CO, CM, C = Parametrisation.get(Premap, ParNodesGmap)
        COO, CMO, C_O = Open.get(C)

        fpf = FamPFunctor.Maker(C, C_O)

        l0 = PremapO(2)
        l0d0 = l0.add_dart()
        l0d1 = l0.add_dart()
        l0.sew(0, l0d0, l0d1)
        l0d2 = l0.add_dart()
        l0d3 = l0.add_dart()
        l0.sew(0, l0d2, l0d3)
        l0.sew(2, l0d0, l0d2)
        l0.sew(2, l0d1, l0d3)

        r0 = PremapO(2)
        r0d0 = r0.add_dart()
        r0d1 = r0.add_dart()
        r0d2 = r0.add_dart()
        r0d3 = r0.add_dart()
        r0.sew(0, r0d0, r0d1)
        r0.sew(0, r0d2, r0d3)
        r0d4 = r0.add_dart()
        r0d5 = r0.add_dart()
        r0d6 = r0.add_dart()
        r0d7 = r0.add_dart()
        r0.sew(0, r0d4, r0d5)
        r0.sew(0, r0d6, r0d7)
        r0.sew(2, r0d0, r0d4)
        r0.sew(2, r0d1, r0d5)
        r0.sew(2, r0d2, r0d6)
        r0.sew(2, r0d3, r0d7)

        def R0(x):
            # print(x.ET)
            p1 = {r0d0: x.ET[l0d0],
                 r0d1: ((x.ET[l1d0][0] + x.ET[l1d1][0])/2, (x.ET[l1d0][1] + x.ET[l1d1][1])/2, (x.ET[l1d0][2] + x.ET[l1d1][2])/2),
                 r0d2: ((x.ET[l1d0][0] + x.ET[l1d1][0])/2, (x.ET[l1d0][1] + x.ET[l1d1][1])/2, (x.ET[l1d0][2] + x.ET[l1d1][2])/2),
                 r0d3: x.ET[l0d1],
                 (r0d0, r0d0) : x.ET[l0d0, l0d0],
                 (r0d0, r0d4) : x.ET[l0d0, l0d2],
                 (r0d2, r0d2) : 0,
                 (r0d2, r0d6) : 0
                }
            p2 = {r0d0: x.ET[l0d0],
                 r0d1: ((x.ET[l1d0][0] + x.ET[l1d1][0])/2, (x.ET[l1d0][1] + x.ET[l1d1][1])/2, (x.ET[l1d0][2] + x.ET[l1d1][2])/2),
                 r0d2: ((x.ET[l1d0][0] + x.ET[l1d1][0])/2, (x.ET[l1d0][1] + x.ET[l1d1][1])/2, (x.ET[l1d0][2] + x.ET[l1d1][2])/2),
                 r0d3: x.ET[l0d1],
                 (r0d0, r0d0) : 0,
                 (r0d0, r0d4) : 0,
                 (r0d2, r0d2) : x.ET[l0d0, l0d0],
                 (r0d2, r0d6) : x.ET[l0d0, l0d2]
                }
            r0p1 = CO(r0, p1)
            r0p2 = CO(r0, p2)
            return COO([r0p1, r0p2])

        g0 = fpf.add_fam_rule(l0, R0)
        
        l00_0 = PremapM(l0, l0, [l0d1, l0d0, l0d3, l0d2])
        r00_0 = PremapM(r0, r0, [r0d3, r0d2, r0d1, r0d0, r0d7, r0d6, r0d5, r0d4])

        def R00_0(lps, lpo, rs, ro):
            gm0 = CM(rs.LO[1], ro.LO[0], r00_0)
            gm1 = CM(rs.LO[0], ro.LO[1], r00_0)
            return CMO(rs, ro, [1, 0], [gm0, gm1])
        
        fpf.add_fam_inclusion(g0, g0, l00_0, R00_0)
        
        l00_1 = PremapM(l0, l0, [l0d2, l0d3, l0d0, l0d1])
        r00_1 = PremapM(r0, r0, [r0d4, r0d5, r0d6, r0d7, r0d0, r0d1, r0d2, r0d3])

        def R00_1(lps, lpo, rs, ro): # should not be applied on edges decorated with different colors
            gm0 = CM(rs.LO[0], ro.LO[0], r00_1)
            gm1 = CM(rs.LO[1], ro.LO[1], r00_1)
            return CMO(rs, ro, [0, 1], [gm0, gm1])

        fpf.add_fam_inclusion(g0, g0, l00_1, R00_1)
        
        l00_2 = l00_0.compose(l00_1)
        r00_2 = r00_0.compose(r00_1)

        def R00_2(lps, lpo, rs, ro): #same
            gm0 = CM(rs.LO[1], ro.LO[0], r00_2)
            gm1 = CM(rs.LO[0], ro.LO[1], r00_2)
            return CMO(rs, ro, [1, 0], [gm0, gm1])

        fpf.add_fam_inclusion(g0, g0, l00_2, R00_2)

        l1 = PremapO(2)
        l1d0 = l1.add_dart()
        l1d1 = l1.add_dart()
        l1.sew(0, l1d0, l1d1)
        l1d2 = l1.add_dart()
        l1d3 = l1.add_dart()
        l1.sew(0, l1d2, l1d3)
        l1.sew(1, l1d1, l1d2)
        l1d4 = l1.add_dart()
        l1d5 = l1.add_dart()
        l1.sew(0, l1d4, l1d5)
        l1.sew(1, l1d3, l1d4)
        l1.sew(1, l1d0, l1d5)
        l1d6 = l1.add_dart()
        l1d7 = l1.add_dart()
        l1.sew(0, l1d6, l1d7)
        l1d8 = l1.add_dart()
        l1d9 = l1.add_dart()
        l1.sew(0, l1d8, l1d9)
        l1d10 = l1.add_dart()
        l1d11 = l1.add_dart()
        l1.sew(0, l1d10, l1d11)
        l1.sew(2, l1d0, l1d6)
        l1.sew(2, l1d1, l1d7)
        l1.sew(2, l1d2, l1d8)
        l1.sew(2, l1d3, l1d9)
        l1.sew(2, l1d4, l1d10)
        l1.sew(2, l1d5, l1d11)

        r1 = PremapO(2)
        r1d0 = r1.add_dart()
        r1d1 = r1.add_dart()
        r1.sew(0, r1d0, r1d1)
        r1d2 = r1.add_dart()
        r1d3 = r1.add_dart()
        r1.sew(0, r1d2, r1d3)
        r1.sew(1, r1d1, r1d2)
        r1d4 = r1.add_dart()
        r1d5 = r1.add_dart()
        r1.sew(0, r1d4, r1d5)
        r1.sew(1, r1d3, r1d4)
        r1.sew(1, r1d0, r1d5)
        r1d6 = r1.add_dart()
        r1d7 = r1.add_dart()
        r1.sew(0, r1d6, r1d7)
        r1d8 = r1.add_dart()
        r1d9 = r1.add_dart()
        r1.sew(0, r1d8, r1d9)
        r1d10 = r1.add_dart()
        r1d11 = r1.add_dart()
        r1.sew(0, r1d10, r1d11)
        r1.sew(2, r1d0, r1d6)
        r1.sew(2, r1d1, r1d7)
        r1.sew(2, r1d2, r1d8)
        r1.sew(2, r1d3, r1d9)
        r1.sew(2, r1d4, r1d10)
        r1.sew(2, r1d5, r1d11)

        r1d12 = r1.add_dart()
        r1d13 = r1.add_dart()
        r1.sew(0, r1d12, r1d13)
        r1d14 = r1.add_dart()
        r1d15 = r1.add_dart()
        r1.sew(0, r1d14, r1d15)
        r1.sew(1, r1d13, r1d14)
        r1d16 = r1.add_dart()
        r1d17 = r1.add_dart()
        r1.sew(0, r1d16, r1d17)
        r1.sew(1, r1d15, r1d16)
        r1.sew(1, r1d12, r1d17)
        r1d18 = r1.add_dart()
        r1d19 = r1.add_dart()
        r1.sew(0, r1d18, r1d19)
        r1d20 = r1.add_dart()
        r1d21 = r1.add_dart()
        r1.sew(0, r1d20, r1d21)
        r1d22 = r1.add_dart()
        r1d23 = r1.add_dart()
        r1.sew(0, r1d22, r1d23)
        r1.sew(2, r1d12, r1d18)
        r1.sew(2, r1d13, r1d19)
        r1.sew(2, r1d14, r1d20)
        r1.sew(2, r1d15, r1d21)
        r1.sew(2, r1d16, r1d22)
        r1.sew(2, r1d17, r1d23)

        r1d24 = r1.add_dart()
        r1d25 = r1.add_dart()
        r1.sew(0, r1d24, r1d25)
        r1d26 = r1.add_dart()
        r1d27 = r1.add_dart()
        r1.sew(0, r1d26, r1d27)
        r1.sew(1, r1d25, r1d26)
        r1d28 = r1.add_dart()
        r1d29 = r1.add_dart()
        r1.sew(0, r1d28, r1d29)
        r1.sew(1, r1d27, r1d28)
        r1.sew(1, r1d24, r1d29)
        r1d30 = r1.add_dart()
        r1d31 = r1.add_dart()
        r1.sew(0, r1d30, r1d31)
        r1d32 = r1.add_dart()
        r1d33 = r1.add_dart()
        r1.sew(0, r1d32, r1d33)
        r1d34 = r1.add_dart()
        r1d35 = r1.add_dart()
        r1.sew(0, r1d34, r1d35)
        r1.sew(2, r1d24, r1d30)
        r1.sew(2, r1d25, r1d31)
        r1.sew(2, r1d26, r1d32)
        r1.sew(2, r1d27, r1d33)
        r1.sew(2, r1d28, r1d34)
        r1.sew(2, r1d29, r1d35)

        r1.sew(1, r1d8, r1d23)
        r1.sew(1, r1d9, r1d30)
        r1.sew(1, r1d22, r1d31)

        r1.sew(2, r1d2, r1d8)
        r1.sew(2, r1d3, r1d9)
        r1.sew(2, r1d16, r1d22)
        r1.sew(2, r1d17, r1d23)
        r1.sew(2, r1d24, r1d30)
        r1.sew(2, r1d25, r1d31)

        def R1(x):
            pn = { r1d0 : x.ET[l1d0],
                   r1d1 : ((x.ET[l1d0][0] + x.ET[l1d1][0])/2, (x.ET[l1d0][1] + x.ET[l1d1][1])/2, (x.ET[l1d0][2] + x.ET[l1d1][2])/2),
                   r1d13: x.ET[l1d1],
                   r1d15: ((x.ET[l1d1][0] + x.ET[l1d3][0])/2, (x.ET[l1d1][1] + x.ET[l1d3][1])/2, (x.ET[l1d1][2] + x.ET[l1d3][2])/2),
                   r1d27: x.ET[l1d3],
                   r1d3 : ((x.ET[l1d3][0] + x.ET[l1d0][0])/2, (x.ET[l1d3][1] + x.ET[l1d0][1])/2, (x.ET[l1d3][2] + x.ET[l1d0][2])/2)
                  }
            d = lambda a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r : {
                (r1d0, r1d0)   : a,
                (r1d0, r1d6)   : b,
                (r1d12, r1d12) : c,
                (r1d12, r1d18) : d,
                (r1d14, r1d12) : e,
                (r1d14, r1d20) : f,
                (r1d26, r1d24) : g,
                (r1d26, r1d32) : h,
                (r1d28, r1d24) : i,
                (r1d28, r1d34) : j,
                (r1d4, r1d0)   : k,
                (r1d4, r1d10)  : l,
                (r1d2, r1d0)   : m,
                (r1d2, r1d8)   : n,
                (r1d16, r1d12) : o,
                (r1d16, r1d8)  : p,
                (r1d24, r1d24) : q,
                (r1d24, r1d8)  : r
                }
            pc = lambda cb, cd, cf, ch, cj, cl : d(-cb, cb, -cd, cd, -cf, cf, -ch, ch, -cj, cj, -cl, cl, cb + cl, -(cb + cl), cd + cf, -(cd + cf), ch + cj, -(ch + cj))
            # print(">>>> Results par")
            R000 = CO(r1, pc(x.ET[l1d0, l1d6], 0, x.ET[l1d2, l1d8], 0, x.ET[l1d4, l1d10], 0))
            R000.ET.update(pn)
            # print(R000.ET)
            R100 = CO(r1, pc(0, x.ET[l1d0, l1d6], x.ET[l1d2, l1d8], 0, x.ET[l1d4, l1d10], 0))
            R100.ET.update(pn)
            # print(R100.ET)
            R010 = CO(r1, pc(x.ET[l1d0, l1d6], 0, 0, x.ET[l1d2, l1d8], x.ET[l1d4, l1d10], 0))
            R010.ET.update(pn)
            # print(R010.ET)
            R110 = CO(r1, pc(0, x.ET[l1d0, l1d6], 0, x.ET[l1d2, l1d8], x.ET[l1d4, l1d10], 0))
            R110.ET.update(pn)
            # print(R110.ET)
            R001 = CO(r1, pc(x.ET[l1d0, l1d6], 0, x.ET[l1d2, l1d8], 0, 0, x.ET[l1d4, l1d10]))
            R001.ET.update(pn)
            # print(R001.ET)
            R101 = CO(r1, pc(0, x.ET[l1d0, l1d6], x.ET[l1d2, l1d8], 0, 0, x.ET[l1d4, l1d10]))
            R101.ET.update(pn)
            # print(R101.ET)
            R011 = CO(r1, pc(x.ET[l1d0, l1d6], 0, 0, x.ET[l1d2, l1d8], 0, x.ET[l1d4, l1d10]))
            R011.ET.update(pn)
            # print(R011.ET)
            R111 = CO(r1, pc(0, x.ET[l1d0, l1d6], 0, x.ET[l1d2, l1d8], 0, x.ET[l1d4, l1d10]))
            R111.ET.update(pn)
            # print(R111.ET)
            # import sys
            # sys.exit()
            return COO([R000, R100, R010, R110, R001, R101, R011, R111])

        g1 = fpf.add_fam_rule(l1, R1)

        l11_r0 = PremapM(l1, l1, [ l1d2, l1d3, l1d4, l1d5, l1d0, l1d1, l1d8, l1d9, l1d10, l1d11, l1d6, l1d7 ])
        r11_r0 = PremapM(r1, r1, [ r1d14, r1d15, r1d16, r1d17, r1d12, r1d13, r1d20, r1d21, r1d22, r1d23, r1d18, r1d19, r1d26, r1d27, r1d28, r1d29, r1d24, r1d25, r1d32, r1d33, r1d34, r1d35, r1d30, r1d31, r1d2, r1d3, r1d4, r1d5, r1d0, r1d1, r1d8, r1d9, r1d10, r1d11, r1d6, r1d7 ])

        def R11_r0(lps, lpo, rs, ro): #sould not be called on a lot of colored triangles
            gm0 = CM(rs.LO[0], ro.LO[0], r11_r0)
            gm1 = CM(rs.LO[4], ro.LO[1], r11_r0)
            gm2 = CM(rs.LO[1], ro.LO[2], r11_r0)
            gm3 = CM(rs.LO[5], ro.LO[3], r11_r0)
            gm4 = CM(rs.LO[2], ro.LO[4], r11_r0)
            gm5 = CM(rs.LO[6], ro.LO[5], r11_r0)
            gm6 = CM(rs.LO[3], ro.LO[6], r11_r0)
            gm7 = CM(rs.LO[7], ro.LO[7], r11_r0)
            return CMO(rs, ro, [0, 4, 1, 5, 2, 6, 3, 7], [gm0, gm1, gm2, gm3, gm4, gm5, gm6, gm7])

        fpf.add_fam_inclusion(g1, g1, l11_r0, R11_r0)
        
        l11_r1 = l11_r0.compose(l11_r0)
        r11_r1 = r11_r0.compose(r11_r0)

        def R11_r1(lps, lpo, rs, ro): #same
            gm0 = CM(rs.LO[0], ro.LO[0], r11_r0)
            gm1 = CM(rs.LO[2], ro.LO[1], r11_r0)
            gm2 = CM(rs.LO[4], ro.LO[2], r11_r0)
            gm3 = CM(rs.LO[6], ro.LO[3], r11_r0)
            gm4 = CM(rs.LO[1], ro.LO[4], r11_r0)
            gm5 = CM(rs.LO[3], ro.LO[5], r11_r0)
            gm6 = CM(rs.LO[5], ro.LO[6], r11_r0)
            gm7 = CM(rs.LO[7], ro.LO[7], r11_r0)
            return CMO(rs, ro, [0, 2, 4, 6, 1, 3, 5, 7], [gm0, gm1, gm2, gm3, gm4, gm5, gm6, gm7])

        fpf.add_fam_inclusion(g1, g1, l11_r1, R11_r1)


        l01_0 = PremapM(l0, l1, [l1d0, l1d1, l1d6, l1d7])
        r01_0 = PremapM(r0, r1, [r1d0, r1d1, r1d12, r1d13, r1d6, r1d7, r1d18, r1d19])

        def R01_0(lps, lpo, rs, ro):
            gm0 = CM(rs.LO[0], ro.LO[0], r01_0)
            gm1 = CM(rs.LO[1], ro.LO[1], r01_0)
            gm2 = CM(rs.LO[0], ro.LO[2], r01_0)
            gm3 = CM(rs.LO[1], ro.LO[3], r01_0)
            gm4 = CM(rs.LO[0], ro.LO[4], r01_0)
            gm5 = CM(rs.LO[1], ro.LO[5], r01_0)
            gm6 = CM(rs.LO[0], ro.LO[6], r01_0)
            gm7 = CM(rs.LO[1], ro.LO[7], r01_0)
            return CMO(rs, ro, [0, 1, 0, 1, 0, 1, 0, 1], [gm0, gm1, gm2, gm3, gm4, gm5, gm6, gm7])

        fpf.add_fam_inclusion(g0, g1, l01_0, R01_0)
        
        l01_0f0 = l00_0.compose(l01_0)
        r01_0f0 = r00_0.compose(r01_0)

        def R01_0f0(lps, lpo, rs, ro):
            gm0 = CM(rs.LO[1], ro.LO[0], r01_0f0)
            gm1 = CM(rs.LO[0], ro.LO[1], r01_0f0)
            gm2 = CM(rs.LO[1], ro.LO[2], r01_0f0)
            gm3 = CM(rs.LO[0], ro.LO[3], r01_0f0)
            gm4 = CM(rs.LO[1], ro.LO[4], r01_0f0)
            gm5 = CM(rs.LO[0], ro.LO[5], r01_0f0)
            gm6 = CM(rs.LO[1], ro.LO[6], r01_0f0)
            gm7 = CM(rs.LO[0], ro.LO[7], r01_0f0)
            return CMO(rs, ro, [1, 0, 1, 0, 1, 0, 1, 0], [gm0, gm1, gm2, gm3, gm4, gm5, gm6, gm7])

        fpf.add_fam_inclusion(g0, g1, l01_0f0, R01_0f0)

        l01_0f1 = l00_1.compose(l01_0)
        r01_0f1 = r00_1.compose(r01_0)

        def R01_0f1(lps, lpo, rs, ro):
            gm0 = CM(rs.LO[0], ro.LO[0], r01_0f1)
            gm1 = CM(rs.LO[1], ro.LO[1], r01_0f1)
            gm2 = CM(rs.LO[0], ro.LO[2], r01_0f1)
            gm3 = CM(rs.LO[1], ro.LO[3], r01_0f1)
            gm4 = CM(rs.LO[0], ro.LO[4], r01_0f1)
            gm5 = CM(rs.LO[1], ro.LO[5], r01_0f1)
            gm6 = CM(rs.LO[0], ro.LO[6], r01_0f1)
            gm7 = CM(rs.LO[1], ro.LO[7], r01_0f1)
            return CMO(rs, ro, [0, 1, 0, 1, 0, 1, 0, 1], [gm0, gm1, gm2, gm3, gm4, gm5, gm6, gm7])

        fpf.add_fam_inclusion(g0, g1, l01_0f1, R01_0f1)
        
        l01_0f2 = l00_2.compose(l01_0)
        r01_0f2 = r00_2.compose(r01_0)

        def R01_0f2(lps, lpo, rs, ro):
            gm0 = CM(rs.LO[1], ro.LO[0], r01_0f2)
            gm1 = CM(rs.LO[0], ro.LO[1], r01_0f2)
            gm2 = CM(rs.LO[1], ro.LO[2], r01_0f2)
            gm3 = CM(rs.LO[0], ro.LO[3], r01_0f2)
            gm4 = CM(rs.LO[1], ro.LO[4], r01_0f2)
            gm5 = CM(rs.LO[0], ro.LO[5], r01_0f2)
            gm6 = CM(rs.LO[1], ro.LO[6], r01_0f2)
            gm7 = CM(rs.LO[0], ro.LO[7], r01_0f2)
            return CMO(rs, ro, [1, 0, 1, 0, 1, 0, 1, 0], [gm0, gm1, gm2, gm3, gm4, gm5, gm6, gm7])

        fpf.add_fam_inclusion(g0, g1, l01_0f2, R01_0f2)

        l01_1 = PremapM(l0, l1, [l1d2, l1d3, l1d8, l1d9])
        r01_1 = PremapM(r0, r1, [r1d14, r1d15, r1d26, r1d27, r1d20, r1d21, r1d32, r1d33])


        def R01_1(lps, lpo, rs, ro):
            gm0 = CM(rs.LO[0], ro.LO[0], r01_1)
            gm1 = CM(rs.LO[0], ro.LO[1], r01_1)
            gm2 = CM(rs.LO[1], ro.LO[2], r01_1)
            gm3 = CM(rs.LO[1], ro.LO[3], r01_1)
            gm4 = CM(rs.LO[0], ro.LO[4], r01_1)
            gm5 = CM(rs.LO[0], ro.LO[5], r01_1)
            gm6 = CM(rs.LO[1], ro.LO[6], r01_1)
            gm7 = CM(rs.LO[1], ro.LO[7], r01_1)
            return CMO(rs, ro, [0, 0, 1, 1, 0, 0, 1, 1], [gm0, gm1, gm2, gm3, gm4, gm5, gm6, gm7])

        fpf.add_fam_inclusion(g0, g1, l01_1, R01_1)

        l01_1f0 = l00_0.compose(l01_1)
        r01_1f0 = r00_0.compose(r01_1)

        def R01_1f0(lps, lpo, rs, ro):
            gm0 = CM(rs.LO[1], ro.LO[0], r01_1f0)
            gm1 = CM(rs.LO[1], ro.LO[1], r01_1f0)
            gm2 = CM(rs.LO[0], ro.LO[2], r01_1f0)
            gm3 = CM(rs.LO[0], ro.LO[3], r01_1f0)
            gm4 = CM(rs.LO[1], ro.LO[4], r01_1f0)
            gm5 = CM(rs.LO[1], ro.LO[5], r01_1f0)
            gm6 = CM(rs.LO[0], ro.LO[6], r01_1f0)
            gm7 = CM(rs.LO[0], ro.LO[7], r01_1f0)
            return CMO(rs, ro, [1, 1, 0, 0, 1, 1, 0, 0], [gm0, gm1, gm2, gm3, gm4, gm5, gm6, gm7])

        fpf.add_fam_inclusion(g0, g1, l01_1f0, R01_1f0)

        l01_1f1 = l00_1.compose(l01_1)
        r01_1f1 = r00_1.compose(r01_1)

        def R01_1f1(lps, lpo, rs, ro):
            gm0 = CM(rs.LO[0], ro.LO[0], r01_1f1)
            gm1 = CM(rs.LO[0], ro.LO[1], r01_1f1)
            gm2 = CM(rs.LO[1], ro.LO[2], r01_1f1)
            gm3 = CM(rs.LO[1], ro.LO[3], r01_1f1)
            gm4 = CM(rs.LO[0], ro.LO[4], r01_1f1)
            gm5 = CM(rs.LO[0], ro.LO[5], r01_1f1)
            gm6 = CM(rs.LO[1], ro.LO[6], r01_1f1)
            gm7 = CM(rs.LO[1], ro.LO[7], r01_1f1)
            return CMO(rs, ro, [0, 0, 1, 1, 0, 0, 1, 1], [gm0, gm1, gm2, gm3, gm4, gm5, gm6, gm7])

        fpf.add_fam_inclusion(g0, g1, l01_1f1, R01_1f1)

        l01_1f2 = l00_2.compose(l01_1)
        r01_1f2 = r00_2.compose(r01_1)

        def R01_1f2(lps, lpo, rs, ro):
            gm0 = CM(rs.LO[1], ro.LO[0], r01_1f2)
            gm1 = CM(rs.LO[1], ro.LO[1], r01_1f2)
            gm2 = CM(rs.LO[0], ro.LO[2], r01_1f2)
            gm3 = CM(rs.LO[0], ro.LO[3], r01_1f2)
            gm4 = CM(rs.LO[1], ro.LO[4], r01_1f2)
            gm5 = CM(rs.LO[1], ro.LO[5], r01_1f2)
            gm6 = CM(rs.LO[0], ro.LO[6], r01_1f2)
            gm7 = CM(rs.LO[0], ro.LO[7], r01_1f2)
            return CMO(rs, ro, [1, 1, 0, 0, 1, 1, 0, 0], [gm0, gm1, gm2, gm3, gm4, gm5, gm6, gm7])

        fpf.add_fam_inclusion(g0, g1, l01_1f2, R01_1f2)


        l01_2 = PremapM(l0, l1, [l1d4, l1d5, l1d10, l1d11])
        r01_2 = PremapM(r0, r1, [r1d28, r1d29, r1d4, r1d5, r1d34, r1d35, r1d10, r1d11])

        def R01_2(lps, lpo, rs, ro):
            gm0 = CM(rs.LO[0], ro.LO[0], r01_2)
            gm1 = CM(rs.LO[0], ro.LO[1], r01_2)
            gm2 = CM(rs.LO[0], ro.LO[2], r01_2)
            gm3 = CM(rs.LO[0], ro.LO[3], r01_2)
            gm4 = CM(rs.LO[1], ro.LO[4], r01_2)
            gm5 = CM(rs.LO[1], ro.LO[5], r01_2)
            gm6 = CM(rs.LO[1], ro.LO[6], r01_2)
            gm7 = CM(rs.LO[1], ro.LO[7], r01_2)
            return CMO(rs, ro, [0, 0, 0, 0, 1, 1, 1, 1], [gm0, gm1, gm2, gm3, gm4, gm5, gm6, gm7])

        fpf.add_fam_inclusion(g0, g1, l01_2, R01_2)
        
        l01_2f0 = l00_0.compose(l01_2)
        r01_2f0 = r00_0.compose(r01_2)

        def R01_2f0(lps, lpo, rs, ro):
            gm0 = CM(rs.LO[1], ro.LO[0], r01_2f0)
            gm1 = CM(rs.LO[1], ro.LO[1], r01_2f0)
            gm2 = CM(rs.LO[1], ro.LO[2], r01_2f0)
            gm3 = CM(rs.LO[1], ro.LO[3], r01_2f0)
            gm4 = CM(rs.LO[0], ro.LO[4], r01_2f0)
            gm5 = CM(rs.LO[0], ro.LO[5], r01_2f0)
            gm6 = CM(rs.LO[0], ro.LO[6], r01_2f0)
            gm7 = CM(rs.LO[0], ro.LO[7], r01_2f0)
            return CMO(rs, ro, [1, 1, 1, 1, 0, 0, 0, 0], [gm0, gm1, gm2, gm3, gm4, gm5, gm6, gm7])

        fpf.add_fam_inclusion(g0, g1, l01_2f0, R01_2f0)

        l01_2f1 = l00_1.compose(l01_2)
        r01_2f1 = r00_1.compose(r01_2)

        def R01_2f1(lps, lpo, rs, ro):
            gm0 = CM(rs.LO[0], ro.LO[0], r01_2f1)
            gm1 = CM(rs.LO[0], ro.LO[1], r01_2f1)
            gm2 = CM(rs.LO[0], ro.LO[2], r01_2f1)
            gm3 = CM(rs.LO[0], ro.LO[3], r01_2f1)
            gm4 = CM(rs.LO[1], ro.LO[4], r01_2f1)
            gm5 = CM(rs.LO[1], ro.LO[5], r01_2f1)
            gm6 = CM(rs.LO[1], ro.LO[6], r01_2f1)
            gm7 = CM(rs.LO[1], ro.LO[7], r01_2f1)
            return CMO(rs, ro, [0, 0, 0, 0, 1, 1, 1, 1], [gm0, gm1, gm2, gm3, gm4, gm5, gm6, gm7])

        fpf.add_fam_inclusion(g0, g1, l01_2f1, R01_2f1)

        l01_2f2 = l00_2.compose(l01_2)
        r01_2f2 = r00_2.compose(r01_2)

        def R01_2f2(lps, lpo, rs, ro):
            gm0 = CM(rs.LO[1], ro.LO[0], r01_2f2)
            gm1 = CM(rs.LO[1], ro.LO[1], r01_2f2)
            gm2 = CM(rs.LO[1], ro.LO[2], r01_2f2)
            gm3 = CM(rs.LO[1], ro.LO[3], r01_2f2)
            gm4 = CM(rs.LO[0], ro.LO[4], r01_2f2)
            gm5 = CM(rs.LO[0], ro.LO[5], r01_2f2)
            gm6 = CM(rs.LO[0], ro.LO[6], r01_2f2)
            gm7 = CM(rs.LO[0], ro.LO[7], r01_2f2)
            return CMO(rs, ro, [1, 1, 1, 1, 0, 0, 0, 0], [gm0, gm1, gm2, gm3, gm4, gm5, gm6, gm7])

        fpf.add_fam_inclusion(g0, g1, l01_2f2, R01_2f2)

        p = {l1d0 : (0.5, 1.73/2, 0.0),
             l1d1: (1.0, 0.0, 0.0),
             l1d3: (0.0, 0.0, 0.0),
             (l1d0, l1d0)   : 1,
             (l1d0, l1d6)   : -1,
             (l1d2, l1d0)   : -1,
             (l1d2, l1d8)   : 1,
             (l1d4, l1d0)   : 0,
             (l1d4, l1d10)  : 0
            }
        gp = CO(l1, p)

        f = fpf.get()

        T = GT(f)

        return T, gp

if __name__ == "__main__":
    show = 0
    if len(sys.argv) > 1:
        if sys.argv[1] == "--show":
            show = 1
        elif sys.argv[1] == "--showall":
            show = 2
        else:
            print("Unknown argument :", "'"+sys.argv[1]+"'", "... Try '--show' or '--showall")
    # divide_tri(show)
    T, gp = Test.rivers()
    for _ in range(0, 6):
        gp = T.extend(gp).LO[0]