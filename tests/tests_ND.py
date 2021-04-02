import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from src.data.Open import Open
import src.data.Graph as GraphModule
from src.data.Graph import *
import matplotlib.pyplot as plt
from src.engine.PFunctor import FlatPFunctor
from src.engine.GT import GT

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


    l01_1 = GraphM(l0, l1, {
        nl0 : nl1_1
    })

    r01_1a = l01_1
    r01_1b = GraphM(r0, r1b, {
        nl0 : nr1b_2
    })

    r01_1 = OGraphM(R0, R1, [0, 0], [r01_1a, r01_1b])
    i01_1 = epf.add_inclusion(g0, g1, l01_1, r01_1)
    
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
    plt.show()
    print("drawed")
    for i in range(0, 2):
        #if i == 3:
        GraphModule.show = True
        g_ = T.extend(g)
        g = g_.object
        # plt.subplot(121)
        nx.draw_kamada_kawai(g.g, **options)
        plt.show()

if __name__ == "__main__":
    divide_edges()