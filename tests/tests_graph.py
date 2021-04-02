import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from src.data.DataStructure import Lazy
from src.data.Sheaf import Parametrisation
import src.data.Graph as GraphModule
from src.data.Graph import *
import matplotlib.pyplot as plt
from src.data.Sequence import *
from random import *

def triangular_mesh_refinement():
    from src.engine.PFunctor import FlatPFunctor
    from src.engine.GT import GT
    pfTm = FlatPFunctor.Maker(Graph, Graph)

    l0 = GraphO()
    nl0 = l0.add_node()
    r0 = l0
    nr0 = nl0

    g0 = pfTm.add_rule(l0,r0)

    l1 = GraphO()
    nl1a = l1.add_node()
    nl1b = l1.add_node()
    el1ab = l1.add_edge(nl1a,nl1b)
    r1 = GraphO()
    nr1a = r1.add_node()
    nr1ab = r1.add_node()
    nr1b = r1.add_node()
    er1aab = r1.add_edge(nr1a,nr1ab)
    er1abb = r1.add_edge(nr1ab,nr1b)

    g1 = pfTm.add_rule(l1,r1)

    l2 = GraphO()
    nl2a = l2.add_node()
    nl2b = l2.add_node()
    nl2c = l2.add_node()
    el2ab = l2.add_edge(nl2a,nl2b)
    el2bc = l2.add_edge(nl2b,nl2c)
    el2ca = l2.add_edge(nl2c,nl2a)
    r2 = GraphO()
    nr2a = r2.add_node()
    nr2ab = r2.add_node()
    nr2b = r2.add_node()
    nr2bc = r2.add_node()
    nr2c = r2.add_node()
    nr2ca = r2.add_node()
    er2aab = r2.add_edge(nr2a,nr2ab)
    er2abb = r2.add_edge(nr2ab,nr2b)
    er2bbc = r2.add_edge(nr2b,nr2bc)
    er2bcc = r2.add_edge(nr2bc,nr2c)
    er2cca = r2.add_edge(nr2c,nr2ca)
    er2caa = r2.add_edge(nr2ca,nr2a)
    er2abca = r2.add_edge(nr2ab,nr2ca)
    er2cabc = r2.add_edge(nr2ca,nr2bc)
    er2bcab = r2.add_edge(nr2bc,nr2ab)

    g2 = pfTm.add_rule(l2,r2)


    incl01a = GraphM(l0,l1,{
        nl0: nl1a
    })
    incr01a = GraphM(r0,r1,{
        nr0: nr1a
    })

    inc01a = pfTm.add_inclusion(g0,g1,incl01a,incr01a)


    incl01b = GraphM(l0,l1,{
        nl0: nl1b
    })
    incr01b = GraphM(r0,r1,{
        nr0: nr1b
    })

    inc01b = pfTm.add_inclusion(g0,g1,incl01b,incr01b)

    incl22a = GraphM(l2,l2,{
        nl2a: nl2b,
        nl2b: nl2c,
        nl2c: nl2a,
        el2ab: el2bc,
        el2bc: el2ca,
        el2ca: el2ab
    })
    incr22a = GraphM(r2,r2,{
        nr2a:nr2b,
        nr2ab:nr2bc,
        nr2b:nr2c,
        nr2bc:nr2ca,
        nr2c:nr2a,
        nr2ca:nr2ab,
        er2aab:er2bbc,
        er2abb:er2bcc,
        er2bbc:er2cca,
        er2bcc:er2caa,
        er2cca:er2aab,
        er2caa:er2abb,
        er2abca:er2bcab,
        er2cabc:er2abca,
        er2bcab:er2cabc
    })

    inc22a = pfTm.add_inclusion(g2,g2,incl22a,incr22a)

    incl22b = incl22a.compose(incl22a)
    incr22b = incr22a.compose(incr22a)
    inc22b = pfTm.add_inclusion(g2,g2,incl22b,incr22b)

    incl12a = GraphM(l1,l2,{
        nl1a: nl2a,
        nl1b: nl2b,
        el1ab: el2ab
    })
    incr12a = GraphM(r1,r2,{
        nr1a: nr2a,
        nr1ab: nr2ab,
        nr1b: nr2b,
        er1aab: er2aab,
        er1abb: er2abb
    })

    inc12a = pfTm.add_inclusion(g1,g2,incl12a,incr12a)
    inc12b = pfTm.add_inclusion(g1,g2,incl12a.compose(incl22a),incr12a.compose(incr22a))
    inc12c = pfTm.add_inclusion(g1,g2,incl12a.compose(incl22b),incr12a.compose(incr22b))

    g = GraphO()
    n1 = g.add_node()
    n2 = g.add_node()
    n3 = g.add_node()
    e12 = g.add_edge(n1,n2)
    e23 = g.add_edge(n2,n3)
    e31 = g.add_edge(n3,n1)

    pfT = pfTm.get()
    T = GT(pfT)

    #plt.subplot(121)
    options = {
        'node_color': 'black',
        'node_size': 20,
        'width': 1,
    }

    nx.draw_kamada_kawai(g.g, **options)
    plt.show()
    GraphModule.show = False
    for i in range(3):
        GraphModule.show = True
        print("------------------------------------------COMPUTE START", i)
        g_ = T.extend(g)
        g = g_.object
        print(len(g.nodes))
        print(len(g.edges))
        nx.draw_kamada_kawai(g.g, **options)
        plt.show()

if __name__ == "__main__":
    triangular_mesh_refinement()

# Here I keep old tests that needs to be adapted
def old():
    def test_graph_ndv2_2():
        from GT_DU_2 import GT_DU, OPFunctor
        seed(10)

        fpfm = OPFunctor.Maker(Graph, Graph)
        Choices = OPFunctor.Choices

        # dot
        l0 = GraphO()
        nl0 = l0.add_node()
        r0 = l0
        nr0 = nl0

        r0C = Choices(l0, [r0])

        # edge
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

        r1C = Choices(l1, [r1a, r1b])

        #first dot in edge
        l01_0 = GraphM(l0, l1, {
            nl0 : nl1_0
        })

        r01_0a = l01_0

        r01_0b = GraphM(r0, r1b, {
            nl0 : nr1b_0
        })

        r1C.add_under_choice(l01_0, r0C, [r01_0a, r01_0b])

        # second dot in edge
        l01_1 = GraphM(l0, l1, {
            nl0 : nl1_1
        })

        r01_1a = l01_1

        r01_1b = GraphM(r0, r1b, {
            nl0 : nr1b_2
        })

        r1C.add_under_choice(l01_1, r0C, [r01_1a, r01_1b])

        # auto edge
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

        r1C.add_under_choice(l11, r1C, [r11a, r11b])

        l2 = GraphO()
        nl2_0 = l2.add_node()
        nl2_1 = l2.add_node()
        nl2_2 = l2.add_node()
        el2_0 = l2.add_edge(nl2_0, nl2_1)
        el2_1 = l2.add_edge(nl2_1, nl2_0)
        el2_2 = l2.add_edge(nl2_1, nl2_2)
        el2_3 = l2.add_edge(nl2_2, nl2_1)
        el2_4 = l2.add_edge(nl2_2, nl2_0)
        el2_5 = l2.add_edge(nl2_0, nl2_2)

        r2a = l2

        r2b = GraphO()
        nr2b = [ r2b.add_node() for _ in range(0, 4)]
        er2b = []
        for i in range(0, 4):
            er2b.append(r2b.add_edge(i, ( i+1 ) % 4))
            er2b.append(r2b.add_edge( (i+1) % 4, i))
        er2b.append(r2b.add_edge(nr2b[1], nr2b[3]))
        er2b.append(r2b.add_edge(nr2b[3], nr2b[1]))

        # r2b_rot1 = GraphO()
        # r2b_rot1.g = r2b.g.copy()

        # r2b_rot2 = GraphO()
        # r2b_rot2.g = r2b.g.copy()
        # nr2b_rot2 = [ (i + 1) % 4 for i in range(0, 4)]
        # er2b_rot2 = [ er2b[(i + 2) % 8] for i in range(0, 8)]
        # er2b_rot2 += [ er2b[8], er2b[9] ]

        r2ca = GraphO()
        r2ca = GraphO()
        nr2ca = [ r2ca.add_node() for i in range(0, 5) ]
        er2ca = []
        for i in range(0, 5):
            er2ca.append(r2ca.add_edge( i, (i+1) % 5 ))
            er2ca.append(r2ca.add_edge( (i+1) % 5, i ))
        er2ca.append(r2ca.add_edge(nr2ca[1], nr2ca[4]))
        er2ca.append(r2ca.add_edge(nr2ca[4], nr2ca[1]))
        er2ca.append(r2ca.add_edge(nr2ca[2], nr2ca[4]))
        er2ca.append(r2ca.add_edge(nr2ca[4], nr2ca[2]))
        
        # n_car1_to_ca = lambda i : (i+3) % 5
        # n_ca_to_car1 = lambda i : (i-3) % 5
        # e_car1_to_ca = lambda i : (i+6) % 10 if i < 10 else i
        # e_ca_to_car1 = lambda i : (i-6) % 10 if i < 10 else i
        # r2ca_rot1 = GraphO()
        # r2ca_rot1.g = r2ca.g.copy()
        # nr2ca_rot1 = [ n_car1_to_ca(i) for i in range(0, 5) ]
        # er2ca_rot1 = [ er2ca[e_car1_to_ca(i)] for i in range(0, 14)]

        # n_car2_to_ca = lambda i : (i+2) % 5
        # n_ca_to_car2 = lambda i : (i-2) % 5
        # e_car2_to_ca = lambda i : (i+4) % 10 if i < 10 else i
        # e_ca_to_car2 = lambda i : (i-4) % 10 if i < 10 else i
        # r2ca_rot2 = GraphO()
        # r2ca_rot2.g = r2ca.g.copy()
        # nr2ca_rot2 = [ n_car2_to_ca(i) for i in range(0, 5) ]
        # er2ca_rot2 = [ er2ca[e_car2_to_ca(i)] for i in range(0, 14)]
        # print(nr2ca_rot2)

        # sys.exit()

        n_cb_to_ca = lambda i : (5-i) % 5
        n_ca_to_cb = n_cb_to_ca
        e_cb_to_ca = lambda i : 9 - i if i < 10 else 21 - i if i < 12 else 25 - i
        e_ca_to_cb = e_cb_to_ca

        r2cb = GraphO()
        r2cb.g = r2ca.g.copy()
        nr2cb = [ n_cb_to_ca(i) for i in range(0, 5) ]
        er2cb = [ er2ca[e_cb_to_ca(i)] for i in range(0, 14)]

        r2d = GraphO()
        nr2d_0  = r2d.add_node()
        nr2d_1  = r2d.add_node()
        nr2d_2  = r2d.add_node()
        nr2d_3  = r2d.add_node()
        nr2d_4  = r2d.add_node()
        nr2d_5  = r2d.add_node()
        er2d_0 = r2d.add_edge(nr2d_0, nr2d_1)
        er2d_1 = r2d.add_edge(nr2d_1, nr2d_0)
        er2d_2 = r2d.add_edge(nr2d_1, nr2d_2)
        er2d_3 = r2d.add_edge(nr2d_2, nr2d_1)
        er2d_4 = r2d.add_edge(nr2d_2, nr2d_3)
        er2d_5 = r2d.add_edge(nr2d_3, nr2d_2)
        er2d_6 = r2d.add_edge(nr2d_3, nr2d_4)
        er2d_7 = r2d.add_edge(nr2d_4, nr2d_3)
        er2d_8 = r2d.add_edge(nr2d_4, nr2d_5)
        er2d_9 = r2d.add_edge(nr2d_5, nr2d_4)
        er2d_10 = r2d.add_edge(nr2d_5, nr2d_0)
        er2d_11 = r2d.add_edge(nr2d_0, nr2d_5)
        er2d_12 = r2d.add_edge(nr2d_3, nr2d_1)
        er2d_13 = r2d.add_edge(nr2d_1, nr2d_3)
        er2d_14 = r2d.add_edge(nr2d_5, nr2d_3)
        er2d_15 = r2d.add_edge(nr2d_3, nr2d_5)
        er2d_16 = r2d.add_edge(nr2d_1, nr2d_5)
        er2d_17 = r2d.add_edge(nr2d_5, nr2d_1)

        r2C = Choices(l2, [r2a, r2b, r2ca, r2cb, r2d])

        #auto triangle

        #rot1

        l_rot1_22 = GraphM(l2, l2, {
            nl2_0 : nl2_1,
            nl2_1 : nl2_2,
            nl2_2 : nl2_0,
            el2_0 : el2_2,
            el2_1 : el2_3,
            el2_2 : el2_4,
            el2_3 : el2_5,
            el2_4 : el2_0,
            el2_5 : el2_1
        })

        r_rot1_22a = l_rot1_22

        r_rot1_22b = None

        r_rot1_22ca = None

        r_rot1_22cb = None

        r_rot1_22d = GraphM(r2d, r2d, {
            nr2d_0 : nr2d_2,
            nr2d_1 : nr2d_3,
            nr2d_2 : nr2d_4,
            nr2d_3 : nr2d_5,
            nr2d_4 : nr2d_0,
            nr2d_5 : nr2d_1,
            er2d_0 : er2d_4,
            er2d_1 : er2d_5,
            er2d_2 : er2d_6,
            er2d_3 : er2d_7,
            er2d_4 : er2d_8,
            er2d_5 : er2d_9,
            er2d_6 : er2d_10,
            er2d_7 : er2d_11,
            er2d_8 : er2d_0,
            er2d_9 : er2d_1,
            er2d_10 : er2d_2,
            er2d_11 : er2d_3,
            er2d_12 : er2d_16,
            er2d_13 : er2d_17,
            er2d_14 : er2d_12,
            er2d_15 : er2d_13,
            er2d_16 : er2d_14,
            er2d_17 : er2d_15
        })

        r2C.add_under_choice(l_rot1_22, r2C, [r_rot1_22a, r_rot1_22b, r_rot1_22ca, r_rot1_22cb, r_rot1_22d])

        #rot2

        l_rot2_22 = l_rot1_22.compose(l_rot1_22)

        r_rot2_22a = l_rot1_22

        r_rot2_22b = None

        r_rot2_22ca = None

        r_rot2_22cb = None

        r_rot2_22d = r_rot1_22d.compose(r_rot1_22d)

        r2C.add_under_choice(l_rot2_22, r2C, [r_rot2_22a, r_rot2_22b, r_rot2_22ca, r_rot2_22cb, r_rot2_22d])

        #flip

        l_flip_22 = GraphM(l2, l2, {
            nl2_0 : nl2_0,
            nl2_1 : nl2_2,
            nl2_2 : nl2_1
        })

        r_flip_22a = l_flip_22

        r_flip_22b = None
        
        r_flip_22ca = GraphM(r2ca, r2cb, {
            nr2ca[0] : nr2cb[0],
            nr2ca[1] : nr2cb[4],
            nr2ca[2] : nr2cb[3],
            nr2ca[3] : nr2cb[2],
            nr2ca[4] : nr2cb[1],
            er2ca[0] : er2cb[9],
            er2ca[1] : er2cb[8],
            er2ca[2] : er2cb[7],
            er2ca[3] : er2cb[6],
            er2ca[4] : er2cb[5],
            er2ca[5] : er2cb[4],
            er2ca[6] : er2cb[3],
            er2ca[7] : er2cb[2],
            er2ca[8] : er2cb[1],
            er2ca[9] : er2cb[0],
            er2ca[10] : er2cb[11],
            er2ca[11] : er2cb[10],
            er2ca[12] : er2cb[13],
            er2ca[13] : er2cb[12]
        })

        r_flip_22cb = GraphM(r2cb, r2ca, { v : k for k, v in r_flip_22ca.l.items() })

        r_flip_22d = GraphM(r2d, r2d, {
            nr2d_0 : nr2d_0,
            nr2d_1 : nr2d_5,
            nr2d_2 : nr2d_4,
            nr2d_3 : nr2d_3,
            nr2d_4 : nr2d_2,
            nr2d_5 : nr2d_1,
            er2d_0 : er2d_11,
            er2d_1 : er2d_10,
            er2d_2 : er2d_9,
            er2d_3 : er2d_8,
            er2d_4 : er2d_7,
            er2d_5 : er2d_6,
            er2d_6 : er2d_5,
            er2d_7 : er2d_4,
            er2d_8 : er2d_3,
            er2d_9 : er2d_2,
            er2d_10 : er2d_1,
            er2d_11 : er2d_0,
            er2d_12 : er2d_15,
            er2d_13 : er2d_14,
            er2d_14 : er2d_13,
            er2d_15 : er2d_12,
            er2d_16 : er2d_17,
            er2d_17 : er2d_16
        })

        r2C.add_under_choice(l_flip_22, r2C, [r_flip_22a, r_flip_22b, r_flip_22ca, r_flip_22cb, r_flip_22d])

        #flip rot1

        l_flip_rot1_22 = l_flip_22.compose(l_rot1_22)

        r_flip_rot1_22a = l_flip_rot1_22

        r_flip_rot1_22b = GraphM(r2b, r2b, {
            nr2b[0] : nr2b[2],
            nr2b[1] : nr2b[1],
            nr2b[2] : nr2b[0],
            nr2b[3] : nr2b[3],
            er2b[0] : er2b[3],
            er2b[1] : er2b[2],
            er2b[2] : er2b[1],
            er2b[3] : er2b[0],
            er2b[4] : er2b[7],
            er2b[5] : er2b[6],
            er2b[6] : er2b[5],
            er2b[7] : er2b[4],
            er2b[8] : er2b[8],
            er2b[9] : er2b[9]
        })

        r_flip_rot1_22ca = None

        r_flip_rot1_22cb = None

        r_flip_rot1_22d = r_flip_22d.compose(r_rot1_22d)

        r2C.add_under_choice(l_flip_rot1_22, r2C, [r_flip_rot1_22a, r_flip_rot1_22b, r_flip_rot1_22ca, r_flip_rot1_22cb, r_flip_rot1_22d])

        #flip rot2

        l_flip_rot2_22 = l_flip_22.compose(l_rot2_22)

        r_flip_rot2_22a = l_flip_rot2_22

        r_flip_rot2_22b = None

        r_flip_rot2_22ca = None

        r_flip_rot2_22cb = None

        r_flip_rot2_22d = r_flip_22d.compose(r_rot2_22d)

        r2C.add_under_choice(l_flip_rot2_22, r2C, [r_flip_rot2_22a, r_flip_rot2_22b, r_flip_rot2_22ca, r_flip_rot2_22cb, r_flip_rot2_22d])

        #######
        
        #first edge in triangle
        l12_0 = GraphM(l1, l2, {
            nl1_0 : nl2_0,
            nl1_1 : nl2_1,
            el1_0 : el2_0,
            el1_1 : el2_1
        })

        r12_0a = l12_0

        r12_0b_1 = GraphM(r1a, r2b, {
            nl1_0 : nr2b[0],
            nl1_1 : nr2b[1],
            el1_0 : er2b[0],
            el1_1 : er2b[1]
        })

        ###
        r12_0b_2 = GraphM(r1a, r2b, {
            nl1_0 : nr2b[1],
            nl1_1 : nr2b[2],
            el1_0 : er2b[2],
            el1_1 : er2b[3]
        })

        ###
        r12_0b_3 = GraphM(r1b, r2b, {
            nr1b_0 : nr2b[2],
            nr1b_1 : nr2b[3],
            nr1b_2 : nr2b[0],
            er1b_0 : er2b[4],
            er1b_1 : er2b[5],
            er1b_2 : er2b[6],
            er1b_3 : er2b[7]
        })
        r12_0b_3.name = "LOL"

        r12_0ca_1 = GraphM(r1b, r2ca, {
            nr1b_0 : nr2ca[0],
            nr1b_1 : nr2ca[1],
            nr1b_2 : nr2ca[2],
            er1b_0 : er2ca[0],
            er1b_1 : er2ca[1],
            er1b_2 : er2ca[2],
            er1b_3 : er2ca[3]
        })

        ###
        r12_0ca_2 = GraphM(r1a, r2ca, {
            nl1_0 : nr2ca[2],
            nl1_1 : nr2ca[3],
            el1_0 : er2ca[4],
            el1_1 : er2ca[5]
        })

        ###
        r12_0ca_3 = GraphM(r1b, r2ca, {
            nr1b_0 : nr2ca[3],
            nr1b_1 : nr2ca[4],
            nr1b_2 : nr2ca[0],
            er1b_0 : er2ca[6],
            er1b_1 : er2ca[7],
            er1b_2 : er2ca[8],
            er1b_3 : er2ca[9]
        })

        r12_0cb_1 = GraphM(r1b, r2cb, {
            nr1b_0 : nr2ca[0],
            nr1b_1 : nr2ca[1],
            nr1b_2 : nr2ca[2],
            er1b_0 : er2ca[0],
            er1b_1 : er2ca[1],
            er1b_2 : er2ca[2],
            er1b_3 : er2ca[3]
        })

        ###
        r12_0cb_2 = GraphM(r1a, r2cb, {
            nl1_0 : nr2ca[2],
            nl1_1 : nr2ca[3],
            el1_0 : er2ca[4],
            el1_1 : er2ca[5]
        })

        ###
        r12_0cb_3 = GraphM(r1b, r2cb, {
            nr1b_0 : nr2ca[3],
            nr1b_1 : nr2ca[4],
            nr1b_2 : nr2ca[0],
            er1b_0 : er2ca[6],
            er1b_1 : er2ca[7],
            er1b_2 : er2ca[8],
            er1b_3 : er2ca[9]
        })

        r12_0d = GraphM(r1b, r2d, {
            nr1b_0 : nr2d_0,
            nr1b_1 : nr2d_1,
            nr1b_2 : nr2d_2,
            er1b_0 : er2d_0,
            er1b_1 : er2d_1,
            er1b_2 : er2d_2,
            er1b_3 : er2d_3
        })
        print(">>>")

        r2C.add_under_choice(l12_0, r1C, [r12_0a, r12_0b_1, r12_0ca_1, r12_0cb_1, r12_0d])
        # r2C.add_under_choice(l12_0, r1C, [r12_0a, r12_0b_1, r12_0b_2, r12_0b_3, r12_0ca_1, r12_0ca_2, r12_0ca_3, r12_0cb_1, r12_0cb_2, r12_0cb_3, r12_0d])

        #first edge in triangle rev

        l12_0r = l11.compose(l12_0)

        r12_0ra = l12_0r
        
        r12_0rb_1 = r11a.compose(r12_0b_1)

        ###
        r12_0rb_2 = r11a.compose(r12_0b_2)

        ###
        r12_0rb_3 = r11b.compose(r12_0b_3)

        r12_0rca_1 = r11b.compose(r12_0ca_1)

        ###
        r12_0rca_2 = r11a.compose(r12_0ca_2)

        ###
        r12_0rca_3 = r11b.compose(r12_0ca_3)

        r12_0rcb_1 = r11b.compose(r12_0cb_1)

        ###
        r12_0rcb_2 = r11a.compose(r12_0cb_2)

        ###
        r12_0rcb_3 = r11b.compose(r12_0cb_3)

        r12_0rd = r11b.compose(r12_0d)

        r2C.add_under_choice(l12_0r, r1C, [r12_0ra, r12_0rb_1, r12_0rca_1, r12_0rcb_1, r12_0rd])
        # r2C.add_under_choice(l12_0r, r1C, [r12_0ra, r12_0rb_1, r12_0rb_2, r12_0rb_3, r12_0rca_1, r12_0rca_2, r12_0rca_3, r12_0rcb_1, r12_0rcb_2, r12_0rcb_3, r12_0rd])

        #second edge in triangle

        l12_1 = GraphM(l1, l2, {
            nl1_0 : nl2_1,
            nl1_1 : nl2_2,
            el1_0 : el2_2,
            el1_1 : el2_3
        })

        r12_1a = l12_1

        r12_1b_1 = r12_0b_2 

        ###
        r12_1b_2 = r12_0b_3 

        ###
        r12_1b_3 = r12_0b_1

        r12_1ca_1 = r12_0ca_2 

        ###
        r12_1ca_2 = r12_0ca_3

        ###
        r12_1ca_3 = r12_0ca_1 

        r12_1cb_1 = r12_0cb_2 

        ###
        r12_1cb_2 = r12_0cb_3

        ###
        r12_1cb_3 = r12_0cb_1

        r12_1d = GraphM(r1b, r2d, {
            nr1b_0 : nr2d_2,
            nr1b_1 : nr2d_3,
            nr1b_2 : nr2d_4,
            er1b_0 : er2d_4,
            er1b_1 : er2d_5,
            er1b_2 : er2d_6,
            er1b_3 : er2d_7
        })

        r2C.add_under_choice(l12_1, r1C, [r12_1a, r12_1b_1, r12_1ca_1, r12_1cb_1, r12_1d])
        # r2C.add_under_choice(l12_1, r1C, [r12_1a, r12_1b_1, r12_1b_2, r12_1b_3, r12_1ca_1, r12_1ca_2, r12_1ca_3, r12_1cb_1, r12_1cb_2, r12_1cb_3, r12_1d])

        #second edge in triangle rev

        l12_1r = l11.compose(l12_1)

        r12_1ra = l12_1r
        
        r12_1rb_1 = r11a.compose(r12_1b_1)

        ###
        r12_1rb_2 = r11b.compose(r12_1b_2)

        ###
        r12_1rb_3 = r11a.compose(r12_1b_3)

        r12_1rca_1 = r11a.compose(r12_1ca_1)

        ###
        r12_1rca_2 = r11b.compose(r12_1ca_2)

        ###
        r12_1rca_3 = r11b.compose(r12_1ca_3)

        r12_1rcb_1 = r11a.compose(r12_1cb_1)

        ###
        r12_1rcb_2 = r11b.compose(r12_1cb_2)

        ###
        r12_1rcb_3 = r11b.compose(r12_1cb_3)

        r12_1rd = r11b.compose(r12_1d)

        r2C.add_under_choice(l12_1r, r1C, [r12_1ra, r12_1rb_1, r12_1rca_1, r12_1rcb_1, r12_1rd])

        #third edge in triangle
        l12_2 = GraphM(l1, l2, {
            nl1_0 : nl2_2,
            nl1_1 : nl2_0,
            el1_0 : el2_4,
            el1_1 : el2_5
        })

        r12_2a = l12_2

        r12_2b_1 = r12_0b_3 

        ###
        r12_2b_2 = r12_0b_1

        ###
        r12_2b_3 = r12_0b_2

        r12_2ca_1 = r12_0ca_3 

        ###
        r12_2ca_2 = r12_0ca_1

        ###
        r12_2ca_3 = r12_0ca_2

        r12_2cb_1 = r12_0cb_3 

        ###
        r12_2cb_2 = r12_0cb_1

        ###
        r12_2cb_3 = r12_0cb_2

        r12_2d = GraphM(r1b, r2d, {
            nr1b_0 : nr2d_4,
            nr1b_1 : nr2d_5,
            nr1b_2 : nr2d_0,
            er1b_0 : er2d_8,
            er1b_1 : er2d_9,
            er1b_2 : er2d_10,
            er1b_3 : er2d_11
        })

        r2C.add_under_choice(l12_2, r1C, [r12_2a, r12_2b_1, r12_2ca_1, r12_2cb_1, r12_2d])

        #third edge in triangle rev

        l12_2r = l11.compose(l12_2)

        r12_2ra = l12_2r
        
        r12_2rb_1 = r11b.compose(r12_2b_1)

        ###
        r12_2rb_2 = r11a.compose(r12_2b_2)

        ###
        r12_2rb_3 = r11a.compose(r12_2b_3)

        r12_2rca_1 = r11b.compose(r12_2ca_1)

        ###
        r12_2rca_2 = r11b.compose(r12_2ca_2)

        ###
        r12_2rca_3 = r11a.compose(r12_2ca_3)

        r12_2rcb_1 = r11b.compose(r12_2cb_1)

        ###
        r12_2rcb_2 = r11b.compose(r12_2cb_2)

        ###
        r12_2rcb_3 = r11a.compose(r12_2cb_3)

        r12_2rd = r11b.compose(r12_2d)

        r2C.add_under_choice(l12_2r, r1C, [r12_2ra, r12_2rb_1, r12_2rca_1, r12_2rcb_1, r12_2rd])

        print(r2C.f_alpha_inv)
        for k, v in r2C.f_alpha_inv.items():
            print(k)
            for i in v:
                print("    ", i)
                for j in v[i]:
                    print("        ", j)
        # sys.exit()
        
        def checkChoices(ch):
            for li, unc in ch.under.items():
                for unr in unc.results:
                    print("lol")
                    print(ch.f_alpha_inv)
                    if unr in ch.f_alpha_inv[li]:
                        for upr in ch.f_alpha_inv[li][unr]:
                            m = ch.f_beta[(li, upr)]
                            assert m.dom == unr
        # checkChoices(r0C)
        # checkChoices(r1C)
        # checkChoices(r2C)

        g0 = fpfm.add_o_rule(l0, r0C, lambda c, incs : r0)

        # def chooser(c, incs):
        #     remaining = None
        #     for inc in incs:
        #         print("inc ", inc)
        #         print("inc g_a rhs", incs[inc].g_a.rhs())
        #         print("TO INTER", c.f_alpha_inv[inc][incs[inc].g_a.rhs()])
        #         print()
        #         if remaining == None:
        #             remaining = set(c.f_alpha_inv[inc][incs[inc].g_a.rhs()])
        #         else:
        #             remaining = remaining.intersection(set(c.f_alpha_inv[inc][incs[inc].g_a.rhs()]))
        #     print("remaining ", remaining)
        #     r = randrange(0, len(remaining))
        #     return list(remaining)[r]

        def chooser(c, incs):
            remaining = set(c.results)
            for inc in incs:
                incs[inc].g_a.rhs()
                c.f_alpha_inv[inc][incs[inc].g_a.rhs()]
            print("choose", len(incs))
            print("remaining")
            for r in remaining:
                print(" -", r)
            print("incs")
            for i in incs:
                print(" -", i)
                print("  g_a.rhs:", incs[i].g_a.rhs())
            for inc in incs:
                print("inc ", inc)
                print("inc g_a rhs", incs[inc].g_a.rhs())
                print("remaining before", remaining)
                print([id(x) for x in remaining])
                print("TO INTER", c.f_alpha_inv[inc][incs[inc].g_a.rhs()])
                print([id(x) for x in c.f_alpha_inv[inc][incs[inc].g_a.rhs()]])
                print()
                # if remaining == None:
                #     remaining = set(c.f_alpha_inv[inc][incs[inc].g_a.rhs()])
                # else:
                remaining = remaining.intersection(set(c.f_alpha_inv[inc][incs[inc].g_a.rhs()]))
                print("remaining after", remaining)
            print("remaining end ", remaining)
            r = randrange(0, len(remaining))
            return list(remaining)[r]

        # g1 = fpfm.add_o_rule(l1, r1C, lambda c, incs : r1a if random() > 0.5 else r1b)
        g1 = fpfm.add_o_rule(l1, r1C, chooser)

        fpfm.add_o_inclusion(g0, g1, l01_0)
        fpfm.add_o_inclusion(g0, g1, l01_1)

        fpfm.add_o_inclusion(g1, g1, l11)


        g2 = fpfm.add_o_rule(l2, r2C, chooser)

        fpfm.add_o_inclusion(g1, g2, l12_0)
        fpfm.add_o_inclusion(g1, g2, l12_0r)

        fpfm.add_o_inclusion(g1, g2, l12_1)
        fpfm.add_o_inclusion(g1, g2, l12_1r)

        fpfm.add_o_inclusion(g1, g2, l12_2)
        fpfm.add_o_inclusion(g1, g2, l12_2r)

        fpfm.add_o_inclusion(g2, g2, l_rot1_22)
        fpfm.add_o_inclusion(g2, g2, l_rot2_22)
        fpfm.add_o_inclusion(g2, g2, l_flip_22)
        fpfm.add_o_inclusion(g2, g2, l_flip_rot1_22)
        fpfm.add_o_inclusion(g2, g2, l_flip_rot2_22)

        # for k, v in g1.rhs_choice.f_beta.items():
        #     print(type(k[0]), type(k[1]))
        #     print(k)
        #     # print(" ", v)

        # fpfm.add_o_inclusion(g0, g1, r11a)

        # end

        fpf = fpfm.get()

        T = GT_DU(fpf)
        
        s = GraphO()
        ns1 = s.add_node()
        ns2 = s.add_node()
        ns3 = s.add_node()
        es12 = s.add_edge(ns1, ns2)
        es21 = s.add_edge(ns2, ns1)
        es23 = s.add_edge(ns2, ns3)
        es32 = s.add_edge(ns3, ns2)
        es31 = s.add_edge(ns3, ns1)
        es13 = s.add_edge(ns1, ns3)
        
        options = {
            'node_color': 'black',
            'node_size': 20,
            'width': 1,
        }
        GraphModule.show = False
        nx.draw_kamada_kawai(s.g, **options)
        plt.show()

        for i in range(0, 10):
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            sp = T.extend(s).object
            # print(len(sp))
            nx.draw_kamada_kawai(s.g, **options)
            plt.show()
            # print(s)

    def test_graph_ndv2_AC():
        from src.engine.upward_resolv.GT_DU import GT_DU
        from src.engine.upward_resolv.PFunctor_DU import OPFunctor
        # seed(10)

        fpfm = OPFunctor.Maker(Graph, Graph)
        Choices = OPFunctor.Choices

        l0 = GraphO()
        nl0 = [ l0.add_node() for i in range(0, 2) ]
        el0 = []
        el0.append(l0.add_edge(0, 1))
        el0.append(l0.add_edge(1, 0))
        
        r0a = l0
        nr0a = nl0
        er0a = el0

        r0b = GraphO()
        nr0b = [ r0b.add_node() for i in range(0, 3) ]
        er0b = []
        for i in range(0, 2):
            er0b.append(r0b.add_edge(i, i+1))
            er0b.append(r0b.add_edge(i+1, i))
        
        r0C = Choices(l0, [r0a, r0b])

        ###
        l00_0 = GraphM(l0, l0, {
            nl0[0] : nl0[1],
            nl0[1] : nl0[0],
            el0[0] : el0[1],
            el0[1] : el0[0],
        })

        r00_0a = l00_0

        r00_0b = GraphM(r0b, r0b, {
            nr0b[0] : nr0b[2],
            nr0b[1] : nr0b[1],
            nr0b[2] : nr0b[0],
            er0b[0] : er0b[3],
            er0b[1] : er0b[2],
            er0b[2] : er0b[1],
            er0b[3] : er0b[0]
        })

        r0C.add_under_choice(l00_0, r0C, [r00_0a, r00_0b])

        ###

        l1 = r0b
        nl1 = nr0b
        el1 = er0b

        r1a = l1
        nr1a = nl1
        er1a = el1

        r1b = GraphO()
        nr1b = [ r1b.add_node() for i in range(0, 4) ]
        er1b = []
        for i in range(0, 3):
            er1b.append(r1b.add_edge(i, i+1))
            er1b.append(r1b.add_edge(i+1, i))

        r1c = GraphO()
        nr1c = [ r1c.add_node() for i in range(0, 4) ]
        er1c = []
        for i in range(0, 3):
            er1c.append(r1c.add_edge(i, i+1))
            er1c.append(r1c.add_edge(i+1, i))

        r1d = GraphO()
        nr1d = [ r1d.add_node() for i in range(0, 5) ]
        er1d = []
        for i in range(0, 4):
            er1d.append(r1d.add_edge(i, i+1))
            er1d.append(r1d.add_edge(i+1, i))

        r1C = Choices(l1, [r1a, r1b, r1c, r1d])

        ### auto
        l11_0 = GraphM(l1, l1, {
            nl1[0] : nl1[2],
            nl1[1] : nl1[1],
            nl1[2] : nl1[0],
            el1[0] : el1[3],
            el1[1] : el1[2],
            el1[2] : el1[1],
            el1[3] : el1[0]
        })

        r11_0a = l11_0

        r11_0b = GraphM(r1b, r1c, {
            nr1b[0] : nr1c[3],
            nr1b[1] : nr1c[2],
            nr1b[2] : nr1c[1],
            nr1b[3] : nr1c[0],
            er1b[0] : er1c[5],
            er1b[1] : er1c[4],
            er1b[2] : er1c[3],
            er1b[3] : er1c[2],
            er1b[4] : er1c[1],
            er1b[5] : er1c[0]
        })

        r11_0c = GraphM(r1c, r1b, {
            nr1c[0] : nr1b[3],
            nr1c[1] : nr1b[2],
            nr1c[2] : nr1b[1],
            nr1c[3] : nr1b[0],
            er1c[0] : er1b[5],
            er1c[1] : er1b[4],
            er1c[2] : er1b[3],
            er1c[3] : er1b[2],
            er1c[4] : er1b[1],
            er1c[5] : er1b[0]
        })

        r11_0d = GraphM(r1d, r1d, {
            nr1d[0] : nr1d[4],
            nr1d[1] : nr1d[3],
            nr1d[2] : nr1d[2],
            nr1d[3] : nr1d[1],
            nr1d[4] : nr1d[0],
            er1d[0] : er1d[7],
            er1d[1] : er1d[6],
            er1d[2] : er1d[5],
            er1d[3] : er1d[4],
            er1d[4] : er1d[3],
            er1d[5] : er1d[2],
            er1d[6] : er1d[1],
            er1d[7] : er1d[0]
        })

        r1C.add_under_choice(l11_0, r1C, [r11_0a, r11_0b, r11_0c, r11_0d])

        ###

        l01_0 = GraphM(l0, l1, {
            nl0[0] : nl1[0],
            nl0[1] : nl1[1],
            el0[0] : el1[0],
            el0[1] : el1[1]
        })

        r01_0a = l01_0

        r01_0b = GraphM(r0b, r1b, {
            nr0b[0] : nr1b[0],
            nr0b[1] : nr1b[1],
            nr0b[2] : nr1b[2],
            er0b[0] : er1b[0],
            er0b[1] : er1b[1],
            er0b[2] : er1b[2],
            er0b[3] : er1b[3],
        })

        r01_0c = GraphM(r0a, r1c, {
            nr0a[0] : nr1c[0],
            nr0a[1] : nr1c[1],
            er0a[0] : er1c[0],
            er0a[1] : er1c[1]
        })

        r01_0d = GraphM(r0b, r1d, {
            nr0b[0] : nr1d[0],
            nr0b[1] : nr1d[1],
            nr0b[2] : nr1d[2],
            er0b[0] : er1d[0],
            er0b[1] : er1d[1],
            er0b[2] : er1d[2],
            er0b[3] : er1d[3],
        })

        r1C.add_under_choice(l01_0, r0C, [r01_0a, r01_0b, r01_0c, r01_0d])
        
        ###

        l01_0r = l00_0.compose(l01_0)

        r01_0ra = l01_0r

        r01_0rb = r00_0b.compose(r01_0b)

        r01_0rc = r00_0a.compose(r01_0c)

        r01_0rd = r00_0b.compose(r01_0d)

        r1C.add_under_choice(l01_0r, r0C, [r01_0ra, r01_0rb, r01_0rc, r01_0rd])

        ###

        l01_1 = GraphM(l0, l1, {
            nl0[0] : nl1[1],
            nl0[1] : nl1[2],
            el0[0] : el1[2],
            el0[1] : el1[3]
        })

        r01_1a = l01_1

        r01_1b = GraphM(r0a, r1b, {
            nr0a[0] : nr1b[2],
            nr0a[1] : nr1b[3],
            er0a[0] : er1b[4],
            er0a[1] : er1b[5],
        })

        r01_1c = GraphM(r0b, r1c, {
            nr0b[0] : nr1c[1],
            nr0b[1] : nr1c[2],
            nr0b[2] : nr1c[3],
            er0b[0] : er1c[2],
            er0b[1] : er1c[3],
            er0b[2] : er1c[4],
            er0b[3] : er1c[5]
        })

        r01_1d = GraphM(r0b, r1d, {
            nr0b[0] : nr1d[2],
            nr0b[1] : nr1d[3],
            nr0b[2] : nr1d[4],
            er0b[0] : er1d[4],
            er0b[1] : er1d[5],
            er0b[2] : er1d[6],
            er0b[3] : er1d[7]
        })

        r1C.add_under_choice(l01_1, r0C, [r01_1a, r01_1b, r01_1c, r01_1d])

        ###

        l01_1r = l00_0.compose(l01_1)

        r01_1ra = l01_1r

        r01_1rb = r00_0a.compose(r01_1b)

        r01_1rc = r00_0b.compose(r01_1c)

        r01_1rd = r00_0b.compose(r01_1d)

        r1C.add_under_choice(l01_1r, r0C, [r01_1ra, r01_1rb, r01_1rc, r01_1rd])

        def chooser(c, incs):
            remaining = set(c.results)
            print("choose", remaining, len(incs))
            for inc in incs:
                print("inc ", inc)
                print("inc g_a rhs", incs[inc].g_a.rhs())
                print("remaining before", remaining)
                print([id(x) for x in remaining])
                print("TO INTER", c.f_alpha_inv[inc][incs[inc].g_a.rhs()])
                print([id(x) for x in c.f_alpha_inv[inc][incs[inc].g_a.rhs()]])
                print()
                # if remaining == None:
                #     remaining = set(c.f_alpha_inv[inc][incs[inc].g_a.rhs()])
                # else:
                remaining = remaining.intersection(set(c.f_alpha_inv[inc][incs[inc].g_a.rhs()]))
                print("remaining after", remaining)
            print("remaining end ", remaining)
            r = randrange(0, len(remaining))
            return list(remaining)[r]

        g0 = fpfm.add_o_rule(l0, r0C, chooser)

        g1 = fpfm.add_o_rule(l1, r1C, chooser)

        fpfm.add_o_inclusion(g0, g1, l01_0)

        fpfm.add_o_inclusion(g0, g1, l01_0r)

        fpfm.add_o_inclusion(g0, g1, l01_1)

        fpfm.add_o_inclusion(g0, g1, l01_1r)

        fpfm.add_o_inclusion(g0, g0, l00_0)

        fpfm.add_o_inclusion(g1, g1, l11_0)

        fpf = fpfm.get()

        T = GT_DU(fpf)
        
        s = GraphO()
        ns1 = s.add_node()
        ns2 = s.add_node()
        ns3 = s.add_node()
        ns4 = s.add_node()
        es12 = s.add_edge(ns1, ns2)
        es21 = s.add_edge(ns2, ns1)
        es23 = s.add_edge(ns2, ns3)
        es32 = s.add_edge(ns3, ns2)
        es34 = s.add_edge(ns3, ns4)
        es43 = s.add_edge(ns4, ns3)
        es41 = s.add_edge(ns4, ns1)
        es14 = s.add_edge(ns1, ns4)
        
        options = {
            'node_color': 'black',
            'node_size': 20,
            'width': 1,
        }
        GraphModule.show = False
        GraphModule.show = True
        nx.draw_kamada_kawai(s.g, **options)
        plt.show()

        for i in range(0, 10):
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            s = T.extend(s).object
            print(s)
            print(type(s))
            nx.draw_kamada_kawai(s.g, **options)
            plt.show()
            # print(s)

    def test_bug():
        from src.engine.upward_resolv.PFunctor_DU import FlatPFunctor
        from src.engine.upward_resolv.GT_DU import GT_DU
        pfTm = FlatPFunctor.Maker(Graph, Graph)

        l0 = GraphO()
        nl0 = l0.add_node()
        r0 = l0
        nr0 = nl0

        g0 = pfTm.add_rule(l0,r0)

        l1 = GraphO()
        nl1a = l1.add_node()
        nl1b = l1.add_node()
        el1ab = l1.add_edge(nl1a,nl1b)
        r1 = l1

        g1 = pfTm.add_rule(l1,r1)

        l2 = GraphO()
        nl2a = l2.add_node()
        nl2b = l2.add_node()
        el2ab  = l2.add_edge(nl2a,nl2b)
        el2abp = l2.add_edge(nl2a,nl2b)
        r2 = l1
        g2 = pfTm.add_rule(l2,r2)


        incl01a = GraphM(l0,l1,{
            nl0: nl1a
        })

        inc01a = pfTm.add_inclusion(g0,g1,incl01a,incl01a)


        incl01b = GraphM(l0,l1,{
            nl0: nl1b
        })

        inc01b = pfTm.add_inclusion(g0,g1,incl01b,incl01b)

        incl22a = GraphM(l2,l2,{
            nl2a : nl2a,
            nl2b : nl2b,
            el2ab : el2abp,
            el2abp : el2ab
        })

        incr22a = GraphM(r2, r2, {
            nl1a : nl1a,
            nl1b : nl2b,
            el1ab : el1ab
        })

        inc22a = pfTm.add_inclusion(g2,g2,incl22a,incr22a)

        incl12a = GraphM(l1,l2,{
            nl1a: nl2a,
            nl1b: nl2b,
            el1ab: el2ab
        })
        incr12a = incr22a

        inc12a = pfTm.add_inclusion(g1,g2,incl12a,incr12a)

        inc12b = pfTm.add_inclusion(g1,g2,incl12a.compose(incl22a),incr12a.compose(incr22a))

        g = GraphO()
        n1 = g.add_node()
        n2 = g.add_node()
        n3 = g.add_node()
        e12 = g.add_edge(n1,n2)
        e23 = g.add_edge(n2,n3)
        e31 = g.add_edge(n3,n1)
        e31p = g.add_edge(n3,n1)
        e13 = g.add_edge(n1,n3)

        pfT = pfTm.get()
        T = GT_DU(pfT)

        options = {
            'node_color': 'black',
            'node_size': 20,
            'width': 1,
        }

        nx.draw_kamada_kawai(g.g, **options)
        # figManager = plt.get_current_fig_manager()
        # # figManager.window.showMaximized()
        print(len(g.nodes))
        print(len(g.edges))
        plt.show()
        GraphModule.show = False
        for i in range(3):
            # GraphModule.show = True
            g = T.extend(g).object
            # print(g_)
            # plt.subplot(121)
            # figManager = plt.get_current_fig_manager()
            # figManager.window.showMaximized()
            print(len(g.nodes))
            print(len(g.edges))
            nx.draw_kamada_kawai(g.g, **options)
            plt.show()