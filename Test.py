import Graph as GraphModule
from Graph import *
from GT import *
from PFunctor import *
import matplotlib.pyplot as plt
from Sequence import *

def test_graph():
    pfTm = PartialFunctor.Maker(Graph, Graph)

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

    # for n in T.G.nodes(): print(n)
    # print()
    # for e in T.G.edges(keys=True): print(e)
    #
    # print()

    g = GraphO()
    # n0 = g.add_node()
    # n0 = g.add_node()
    # n0 = g.add_node()
    # n0 = g.add_node()
    # n0 = g.add_node()
    # n0 = g.add_node()
    # n0 = g.add_node()
    # n0 = g.add_node()
    # n0 = g.add_node()
    # n0 = g.add_node()
    n1 = g.add_node()
    n2 = g.add_node()
    n3 = g.add_node()
    #n4 = g.add_node()
    e12 = g.add_edge(n1,n2)
    # e21 = g.add_edge(n2,n1)
    e23 = g.add_edge(n2,n3)
    e31 = g.add_edge(n3,n1)
    #e34 = g.add_edge(n3,n4)
    #e42 = g.add_edge(n4,n2)

    # g = GraphO()
    # n1 = g.add_node()
    # n12 = g.add_node()
    # n2 = g.add_node()
    # n23 = g.add_node()
    # n3 = g.add_node()
    # n31 = g.add_node()
    # #n4 = g.add_node()
    # e112 = g.add_edge(n1,n12)
    # e122 = g.add_edge(n12,n2)
    # e223 = g.add_edge(n2,n23)
    # e233 = g.add_edge(n23,n3)
    # e331 = g.add_edge(n3,n31)
    # e311 = g.add_edge(n31,n1)

    pfT = pfTm.get()
    T = GT(pfT)

    plt.subplot(121)
    options = {
        'node_color': 'black',
        'node_size': 20,
        'width': 1,
    }

    nx.draw_kamada_kawai(g.g, **options)
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()
    GraphModule.show = False
    for i in range(4):
        if i == 3:
            GraphModule.show = True
        print("------------------------------------------COMPUTE START", i)
        g_ = T.extend(g)
        # print(g_)
        g = tuple(g_)[0].object
        plt.subplot(121)
        figManager = plt.get_current_fig_manager()
        figManager.window.showMaximized()
        nx.draw_kamada_kawai(g.g, **options)
        plt.show()

    print(len(g.nodes))
    print(len(g.edges))
    print(1 + len(g.edges) - len(g.nodes))
    # print()
    # for n in T.G.nodes(): print(n)
    # print()
    # for e in T.G.edges(keys=True): print(e)

# SEQUENCES
def test_seq():
    l0 = SequenceO([])
    r0 = SequenceO([])

    l1 = SequenceO(['a'])
    r1 = SequenceO(['a', 'b'])

    l2 = SequenceO(['b'])
    r2 = SequenceO(['a'])

    incl01a = SequenceM(l0, l1, 0)
    incl01b = SequenceM(l0, l1, 1)

    incr01a = SequenceM(r0, r1, 0)
    incr01b = SequenceM(r0, r1, 2)

    incl02a = SequenceM(l0, l2, 0)
    incl02b = SequenceM(l0, l2, 1)

    incr02a = SequenceM(r0, r2, 0)
    incr02b = SequenceM(r0, r2, 1)

    pfTm = PartialFunctor.Maker(Sequence, Sequence)
    g0 = pfTm.add_rule(l0, r0)
    g1 = pfTm.add_rule(l1, r1)
    g2 = pfTm.add_rule(l2, r2)

    pfTm.add_inclusion(g0, g1, incl01a, incr01a)
    pfTm.add_inclusion(g0, g1, incl01b, incr01b)

    pfTm.add_inclusion(g0, g2, incl02a, incr02a)
    pfTm.add_inclusion(g0, g2, incl02b, incr02b)

    pfT = pfTm.get()
    T = GT(pfT)

    s = SequenceO(['b'])
    print(s)

    for _ in range(8):
        s_ = T.extend(s)
        s = tuple(s_)[0].object
        print(s)

def test_seq_graph():
    pfTm = PartialFunctor.Maker(Sequence, Graph)
    l0 = SequenceO([])
    r0 = GraphO()
    nr0 = r0.add_node()

    l1 = SequenceO([None])
    r1 = GraphO()
    nr1a = r1.add_node()
    nr1b = r1.add_node()
    er1ab = r1.add_edge(nr1a,nr1b)

    incl01a = SequenceM(l0, l1, 0)
    incl01b = SequenceM(l0, l1, 1)

    incr01a = GraphM(r0,r1,{
        nr0: nr1a
    })
    incr01b = GraphM(r0,r1,{
        nr0: nr1b
    })
    g0 = pfTm.add_rule(l0, r0)
    g1 = pfTm.add_rule(l1, r1)

    pfTm.add_inclusion(g0, g1, incl01a, incr01a)
    pfTm.add_inclusion(g0, g1, incl01b, incr01b)

    pfT = pfTm.get()
    T = GT(pfT)

    s = SequenceO([None] * 1000)
    g_ = T.apply(s)
    print(g_)
    g = tuple(g_)[0].object
    # nx.draw_kamada_kawai(g.g, **options)
    # plt.show()

    # print(len(g.nodes))
    # print(len(g.edges))
    # print(1 + len(g.edges) - len(g.nodes))

# test_seq()
test_graph()













#
