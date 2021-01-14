import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from DataStructure import Lazy
from Sheaf import Parametrisation
import Graph as GraphModule
from Graph import *
from GT import *
from PFunctor import *
import matplotlib.pyplot as plt
from Sequence import *
from random import *

def test_graph_old():
    from GT import GT
    from PFunctor import FlatPFunctor
    pf = FlatPFunctor.Maker(Graph, Graph)

    l0 = GraphO()
    nl0 = l0.add_node()
    r0 = GraphO()
    n0r0 = r0.add_node()
    n1r0 = r0.add_node()
    e0r0 = r0.add_edge(n0r0, n1r0)

    g0 = pf.add_rule(l0,r0)

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

    g1 = pf.add_rule(l1,r1)

    il01a = GraphM(l0, l1, {
        nl0 : nl1a
    })

    ir01a = GraphM(r0, r1, {
        n0r0 : nr1a,
        n1r0 : nr1ab,
        e0r0 : er1aab
    })

    il01b = GraphM(l0, l1, {
        nl0 : nl1b
    })

    ir01b = GraphM(r0, r1, {
        n0r0 : nr1ab,
        n1r0 : nr1b,
        e0r0 : er1abb
    })

    inc01a = pf.add_inclusion(g0,g1,il01a,ir01a)
    inc01b = pf.add_inclusion(g0,g1,il01b,ir01b)
    p = pf.get()

    g = GraphO()
    n1 = g.add_node()
    n2 = g.add_node()
    n3 = g.add_node()
    e12 = g.add_edge(n1,n2)
    e23 = g.add_edge(n2,n3)
    e31 = g.add_edge(n3,n1)

    T = GT(p)

    plt.subplot(121)
    options = {
        'node_color': 'black',
        'node_size': 20,
        'width': 1,
    }

    # nx.draw_kamada_kawai(g.g, **options)
    # figManager = plt.get_current_fig_manager()
    # # figManager.window.showMaximized()
    #plt.show()
    GraphModule.show = False
    for i in range(3):
        GraphModule.show = True
        print("------------------------------------------COMPUTE START", i)
        g_ = T.extend(g)
        # print(g_)
        g = g_.object
        plt.subplot(121)
        # figManager = plt.get_current_fig_manager()
        # figManager.window.showMaximized()
        print(len(g.nodes))
        print(len(g.edges))
        # nx.draw_kamada_kawai(g.g, **options)
        # plt.show()

    

def test_graph():
    from GT_DU_2 import FlatPFunctor, GT_DU
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
    T = GT_DU(pfT)

    plt.subplot(121)
    options = {
        'node_color': 'black',
        'node_size': 20,
        'width': 1,
    }

    # nx.draw_kamada_kawai(g.g, **options)
    # figManager = plt.get_current_fig_manager()
    # # figManager.window.showMaximized()
    #plt.show()
    GraphModule.show = False
    for i in range(3):
        GraphModule.show = True
        print("------------------------------------------COMPUTE START", i)
        g_ = T.extend(g)
        # print(g_)
        g = g_.object
        plt.subplot(121)
        # figManager = plt.get_current_fig_manager()
        # figManager.window.showMaximized()
        print(len(g.nodes))
        print(len(g.edges))
        # nx.draw_kamada_kawai(g.g, **options)
        # plt.show()

    # print(1 + len(g.edges) - len(g.nodes))
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

    pfTm = FlatPFunctor.Maker(Sequence, Sequence)
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
    pfTm = FlatPFunctor.Maker(Sequence, Graph)
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
    g_ = T.extend(s)
    print(g_)
    g = tuple(g_)[0].object
    # nx.draw_kamada_kawai(g.g, **options)
    # plt.show()

    # print(len(g.nodes))
    # print(len(g.edges))
    # print(1 + len(g.edges) - len(g.nodes))

def test_graph_nd():
    LGraph = Lazy(Graph)

    epf = FamExpPFunctor.Maker(Graph, LGraph)

    l0 = GraphO()
    nl0 = l0.add_node()
    r0 = l0
    nr0 = nl0

    r0 = l0
    def er_0(lp):
        assert lp == l0
        def er_0_exp():
            return (r0, [], [])
        return er_0_exp
    g_0 = epf.add_fam_exp_rule(l0, er_0, 0)

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

    l01_0 = GraphM(l0, l1, {
        nl0 : nl1_0
    })
    r01_0a = l01_0

    r01_0b = GraphM(r0, r1b, {
        nl0 : nr1b_0
    })

    l01_1 = GraphM(l0, l1, {
        nl0 : nl1_1
    })

    r01_1a = l01_1

    r01_1b = GraphM(r0, r1b, {
        nl0 : nr1b_2
    })

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

    cptsub = 0
    def er_1(lp):
        assert lp == l1
        def er_1_exp(r0_inc1, r0_inc2):
            nonlocal cptsub
            if random() > 0.5:
                print("no sub")
                return (r1a, [r01_0a, r01_1a], [r11a])
            else:
                print("sub")
                cptsub += 1
                return (r1b, [r01_0b, r01_1b], [r11b])
        return er_1_exp
    g_1 = epf.add_fam_exp_rule(l1, er_1, 1)

    ###

    g_0_1_0 = epf.add_fam_exp_inclusion(g_0, g_1, l01_0, 0)

    g_0_1_1 = epf.add_fam_exp_inclusion(g_0, g_1, l01_1, 1)

    g_1_1 = epf.add_fam_exp_inclusion(g_1, g_1, l11, 0)

    epf = epf.get()
    T = GT(epf)

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
        #    GraphModule.show = True
        g_ = T.extend(g)
        g = tuple(g_)[0].object
        print("sub", cptsub)
        # plt.subplot(121)
        nx.draw_kamada_kawai(g.g, **options)
        plt.show()

def test_graph_nda_sheaf():
    def restriction(f, q):
        ret = {}
        # TODO :genericity with element operator ?
        for e in f.dom.edges:
            ret[e] = q[f.apply(e)]
        return ret

    def amalgamation(f, p, g, q):
        assert f.cod == g.cod
        ret = {}
        for e in f.dom.edges:
            ret[f.apply(e)] = p[e]

        for e in g.dom.edges:
            if ret.get(g.apply(e)) == None:
                ret[g.apply(e)] = q[e]
            elif ret[g.apply(e)] != q[e]:
                raise Exception("fail amalgamation")

        return ret

    def amalgamation_2_in_1(ret, g, q):
        for e in g.dom.edges:
            if ret.get(g.apply(e)) == None:
                ret[g.apply(e)] = q[e]
            elif ret[g.apply(e)] != q[e]:
                raise Exception("fail amalgamation 2 in 1")

    def amalgamation_quotient(f, p):
        ret = {}
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

    ParameterEdgesGraph = {
        'name'                  : "ParGraph",
        'parhash'               : phash,
        'restriction'           : restriction,
        'amalgamation'          : amalgamation,
        'amalgamation_2_in_1'   : amalgamation_2_in_1,
        'amalgamation_quotient' : amalgamation_quotient
    }
    ParGraphO, ParGraphM, ParGraph = Parametrisation.get(Graph, ParameterEdgesGraph)
    LParGraph = Lazy(ParGraph)

    epf = FamExpPFunctor.Maker(ParGraph, LParGraph)

    l0 = GraphO()
    nl0 = l0.add_node()
    r0 = l0
    nr0 = nl0

    r0 = l0
    def er_0(lp):
        assert lp.OC == l0
        def er_0_exp():
            return (ParGraphO(r0, {}), [], [])
        return er_0_exp
    g_0 = epf.add_fam_exp_rule(l0, er_0, 0)

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

    l01_0 = GraphM(l0, l1, {
        nl0 : nl1_0
    })
    r01_0a = l01_0

    r01_0b = GraphM(r0, r1b, {
        nl0 : nr1b_0
    })

    l01_1 = GraphM(l0, l1, {
        nl0 : nl1_1
    })

    r01_1a = l01_1

    r01_1b = GraphM(r0, r1b, {
        nl0 : nr1b_2
    })

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

    cptsub = 0
    def er_1(lp):
        assert lp.OC == l1
        def er_1_exp(s1, s2):
            nonlocal cptsub
            if lp.ET[el1_0] == 0:
                res = ParGraphO(r1a, {el1_0 : lp.ET[el1_0], el1_1 : lp.ET[el1_1]})
                m1 = ParGraphM(s1, res, r01_0a)
                m2 = ParGraphM(s2, res, r01_1a)
                ma = ParGraphM(res, res, r11a)
                return (res, [m1, m2], [ma])
            else:
                if random() > 0.5:
                    print("no sub")
                    res = ParGraphO(r1a, {el1_0 : lp.ET[el1_0], el1_1 : lp.ET[el1_1]})
                    m1 = ParGraphM(s1, res, r01_0a)
                    m2 = ParGraphM(s2, res, r01_1a)
                    ma = ParGraphM(res, res, r11a)
                    return (res, [m1, m2], [ma])
                else:
                    print("sub")
                    cptsub += 1
                    res = ParGraphO(r1b, {er1b_0 : lp.ET[el1_0], er1b_1 : lp.ET[el1_1], er1b_2 : lp.ET[el1_0], er1b_3 : lp.ET[el1_1]})
                    m1 = ParGraphM(s1, res, r01_0b)
                    m2 = ParGraphM(s2, res, r01_1b)
                    ma = ParGraphM(res, res, r11b)
                    return (res, [m1, m2], [ma])
        return er_1_exp
    g_1 = epf.add_fam_exp_rule(l1, er_1, 1)

    ###

    g_0_1_0 = epf.add_fam_exp_inclusion(g_0, g_1, l01_0, 0)

    g_0_1_1 = epf.add_fam_exp_inclusion(g_0, g_1, l01_1, 1)

    g_1_1 = epf.add_fam_exp_inclusion(g_1, g_1, l11, 0)

    epf = epf.get()
    T = GT(epf)

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
    g = ParGraphO(g, {e12: 0, e21 : 0, e23 : 1, e32 : 1, e31 : 1, e13 : 1})
    # print(len(g.g.nodes))

    #plt.subplot(121)
    options = {
        'node_color': 'black',
        'node_size': 20,
        'width': 1,
    }

    GraphModule.show = False
    # options['edge_colors'] = g.ET
    ec = [ 'red' if g.ET[v] == 1 else 'blue' for v in g.OC.edges(keys = True)]
    print(ec)
    nx.draw(g.OC.g, layout=nx.spring_layout(g.OC.g), node_color= 'blue', node_size = 20, width = 1, edge_color = ec)#**options)
    plt.show()
    print("drawed")
    for i in range(0, 2):
        #if i == 3:
        #    GraphModule.show = True
        g_ = T.extend(g)
        g = tuple(g_)[0].object
        print("sub", cptsub)
        # options['edge_colors'] = g.ET
        # plt.subplot(121)
        ec = [ 'red' if g.ET[v] == 1 else 'blue' for v in g.OC.edges(keys = True)]
        print(ec)
        nx.draw(g.OC.g, layout=nx.spring_layout(g.OC.g), node_color= 'blue', node_size = 20, width = 1, edge_color = ec)#**options)
        plt.show()

    print(len(g.OC.nodes))
    print(len(g.OC.edges))


def test_graph_nda_sheaf_2():
    def restriction(f, q):
        ret = {}
        # TODO :genericity with element operator ?
        for n in f.dom.nodes:
            ret[n] = q[f.apply(n)]
        return ret

    def amalgamation(f, p, g, q):
        assert f.cod == g.cod
        ret = {}
        for n in f.dom.nodes:
            ret[f.apply(n)] = p[n]

        for n in g.dom.nodes:
            if ret.get(g.apply(n)) == None:
                ret[g.apply(n)] = q[n]
            elif ret[g.apply(n)] != q[n]:
                raise Exception("fail amalgamation")

        return ret

    def amalgamation_2_in_1(ret, g, q):
        for n in g.dom.nodes:
            if ret.get(g.apply(n)) == None:
                ret[g.apply(n)] = q[n]
            elif ret[g.apply(n)] != q[n]:
                raise Exception("fail amalgamation 2 in 1")

    def amalgamation_quotient(f, p):
        ret = {}
        for n in f.dom.nodes:
            ret[f.apply(n)] = p[n]

        return ret

    def phash(p): # TODO WHY NOT NEEDED, REMOVE ?
        r = 1
        # r = 31 * len(p.items())
        # for k, v in p.items():
        #     r ^= 31 * hash(k)
        #     r ^= 31 * hash(v)
        return r

    ParameterNodesGraph = {
        'name'                  : "ParGraph",
        'parhash'               : phash,
        'restriction'           : restriction,
        'amalgamation'          : amalgamation,
        'amalgamation_2_in_1'   : amalgamation_2_in_1,
        'amalgamation_quotient' : amalgamation_quotient
    }
    ParGraphO, ParGraphM, ParGraph = Parametrisation.get(Graph, ParameterNodesGraph)
    LParGraph = Lazy(ParGraph)

    epf = FamExpPFunctor.Maker(ParGraph, LParGraph)

    l0 = GraphO()
    nl0 = l0.add_node()

    r0 = l0
    nr0 = nl0

    r0 = l0
    def er_0(lp):
        assert lp.OC == l0
        def er_0_exp():
            return (ParGraphO(r0, { nr0: random() > 0.5 }), [], [])
        return er_0_exp
    
    def er_0_auto(auto):
        def er_0_exp():
            raise Exception("Should not be called")
    
    g_0 = epf.add_fam_exp_rule(l0, er_0, er_0_auto, 0)

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

    l01_0 = GraphM(l0, l1, {
        nl0 : nl1_0
    })
    r01_0a = l01_0

    r01_0b = GraphM(r0, r1b, {
        nl0 : nr1b_0
    })

    l01_1 = GraphM(l0, l1, {
        nl0 : nl1_1
    })

    r01_1a = l01_1

    r01_1b = GraphM(r0, r1b, {
        nl0 : nr1b_2
    })

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

    cptsub = 0
    def er_1(lp):
        assert lp.OC == l1
        def er_1_exp(s1, s2):
            nonlocal cptsub
            if s1.ET[nr0] and s2.ET[nr0]:
                print("sub")
                cptsub += 1
                res = ParGraphO(r1b, {nr1b_0 : True, nr1b_1 : True, nr1b_2 : True})
                m1 = ParGraphM(s1, res, r01_0b)
                m2 = ParGraphM(s2, res, r01_1b)
                ma = ParGraphM(res.restrict(r11b).dom, res, r11b)
                return (res, [m1, m2], [ma])
            else:
                res = ParGraphO(r1a, {nl1_0 : s1.ET[nr0], nl1_1 : s2.ET[nr0]})
                m1 = ParGraphM(s1, res, r01_0a)
                m2 = ParGraphM(s2, res, r01_1a)
                ma = ParGraphM(res.restrict(r11a).dom, res, r11a)
                return (res, [m1, m2], [ma])
        return er_1_exp
    
    def er_1_auto(auto):
        def er_1_exp(s1, s2):
            if s1.ET[nr0] and s2.ET[nr0]:
                res = auto.dom
                m1 = ParGraphM(s1, res, r01_0b)
                m2 = ParGraphM(s2, res, r01_1b)
                ma = ParGraphM(res.restrict(r11b).dom, res, r11b)
                return (res, [m1, m2], [ma])
            else:
                res = auto.dom
                m1 = ParGraphM(s1, res, r01_0a)
                m2 = ParGraphM(s2, res, r01_1a)
                ma = ParGraphM(res.restrict(r11a).dom, res, r11a)
                return (res, [m1, m2], [ma])
        return er_1_exp
    g_1 = epf.add_fam_exp_rule(l1, er_1, er_1_auto, 1)

    g_0_1_0 = epf.add_fam_exp_inclusion(g_0, g_1, l01_0, 0)

    g_0_1_1 = epf.add_fam_exp_inclusion(g_0, g_1, l01_1, 1)

    g_1_1 = epf.add_fam_exp_inclusion(g_1, g_1, l11, 0)

    ###

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

    l12_0 = GraphM(l1, l2, {
        nl1_0 : nl2_0,
        nl1_1 : nl2_1,
        el1_0 : el2_0,
        el1_1 : el2_1
    })

    l12_0p = l11.compose(l12_0)

    l12_1 = GraphM(l1, l2, {
        nl1_0 : nl2_1,
        nl1_1 : nl2_2,
        el1_0 : el2_2,
        el1_1 : el2_3
    })

    l12_1p = l11.compose(l12_1)

    l12_2 = GraphM(l1, l2, {
        nl1_0 : nl2_2,
        nl1_1 : nl2_0,
        el1_0 : el2_4,
        el1_1 : el2_5
    })

    l12_2p = l11.compose(l12_2)

    l22_1 = GraphM(l2, l2, {
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

    l22_2 = l22_1.compose(l22_1)

    l22_3 = GraphM(l2, l2, {
        nl2_0 : nl2_0,
        nl2_1 : nl2_2,
        nl2_2 : nl2_1,
        el2_0 : el2_5,
        el2_1 : el2_4,
        el2_2 : el2_3,
        el2_3 : el2_2,
        el2_4 : el2_1,
        el2_5 : el2_0
    })

    l22_4 = l22_3.compose(l22_1)

    l22_5 = l22_3.compose(l22_2)

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
    er2b_6 = r2b.add_edge(nr2b_3, nr2b_0)
    er2b_7 = r2b.add_edge(nr2b_0, nr2b_3)

    r2b2b3 = GraphM(r2b, r2b, {
        nr2b_0 : nr2b_0,
        nr2b_1 : nr2b_3,
        nr2b_2 : nr2b_2,
        nr2b_3 : nr2b_1,
        er2b_0 : er2b_7,
        er2b_1 : er2b_6,
        er2b_2 : er2b_5,
        er2b_3 : er2b_4,
        er2b_4 : er2b_3,
        er2b_5 : er2b_2,
        er2b_6 : er2b_1,
        er2b_7 : er2b_0
    })

    r2c = GraphO()
    nr2c_0 = r2c.add_node()
    nr2c_1 = r2c.add_node()
    nr2c_2 = r2c.add_node()
    nr2c_3 = r2c.add_node()
    nr2c_4 = r2c.add_node()
    nr2c_5 = r2c.add_node()
    er2c_0 = r2b.add_edge(nr2c_0, nr2c_1)
    er2c_1 = r2b.add_edge(nr2c_1, nr2c_0)
    er2c_2 = r2b.add_edge(nr2c_1, nr2c_2)
    er2c_3 = r2b.add_edge(nr2c_2, nr2c_1)
    er2c_4 = r2b.add_edge(nr2c_2, nr2c_3)
    er2c_5 = r2b.add_edge(nr2c_3, nr2c_2)
    er2c_6 = r2b.add_edge(nr2c_3, nr2c_4)
    er2c_7 = r2b.add_edge(nr2c_4, nr2c_3)
    er2c_8 = r2b.add_edge(nr2c_4, nr2c_5)
    er2c_9 = r2b.add_edge(nr2c_5, nr2c_4)
    er2c_10 = r2b.add_edge(nr2c_5, nr2c_0)
    er2c_11 = r2b.add_edge(nr2c_0, nr2c_5)

    r2c2c_1 = GraphM(r2c, r2c, {
        nr2c_0 : nr2c_2,
        nr2c_1 : nr2c_3,
        nr2c_2 : nr2c_4,
        nr2c_3 : nr2c_5,
        nr2c_4 : nr2c_0,
        nr2c_5 : nr2c_1,
        er2c_0 : er2c_2,
        er2c_1 : er2c_3,
        er2c_2 : er2c_4,
        er2c_3 : er2c_5,
        er2c_4 : er2c_6,
        er2c_5 : er2c_7,
        er2c_6 : er2c_8,
        er2c_7 : er2c_9,
        er2c_8 : er2c_10,
        er2c_9 : er2c_11,
        er2c_10 : er2c_0,
        er2c_11 : er2c_1
    })

    r2c2c_2 = r2c2c_1.compose(r2c2c_1)

    r2c2c_3 = GraphM(r2c, r2c, {
        nr2c_0 : nr2c_0,
        nr2c_1 : nr2c_5,
        nr2c_2 : nr2c_4,
        nr2c_3 : nr2c_3,
        nr2c_4 : nr2c_2,
        nr2c_5 : nr2c_1,
        er2c_0 : er2c_11,
        er2c_1 : er2c_10,
        er2c_2 : er2c_9,
        er2c_3 : er2c_8,
        er2c_4 : er2c_7,
        er2c_5 : er2c_6,
        er2c_6 : er2c_5,
        er2c_7 : er2c_4,
        er2c_8 : er2c_3,
        er2c_9 : er2c_2,
        er2c_10 : er2c_1,
        er2c_11 : er2c_0
    })

    r2c2c_4 = r2c2c_3.compose(r2c2c_1)

    r2c2c_5 = r2c2c_3.compose(r2c2c_2)

    r1a2a_0 = l12_0
    r1a2a_0p = l12_0p
    r1a2a_1 = l12_1
    r1a2a_1p = l12_1p
    r1a2a_2 = l12_2
    r1a2a_2p = l12_2p
    
    r1a2b_0 = GraphM(r1a, r2b, {
        nl1_0 : nr2b_0,
        nl1_1 : nr2b_1,
        el1_0 : er2b_0,
        el1_1 : er2b_1
    })

    r1a2b_0p = r11a.compose(r1a2b_0)

    r1b2b_1 = GraphM(r1b, r2b, {
        nr1b_0 : nr2b_1,
        nr1b_1 : nr2b_2,
        nr1b_2 : nr2b_3,
        er1b_0 : er2b_2,
        er1b_1 : er2b_3,
        er1b_2 : er2b_4,
        er1b_3 : er2b_5
    })

    r1b2b_1p = r11b.compose(r1b2b_1)

    r1a2b_2 = GraphM(r1a, r2b, {
        nl1_0 : nr2b_3,
        nl1_1 : nr2b_0,
        el1_0 : er2b_6,
        el1_1 : er2b_7
    })

    r1a2b_2p = r11a.compose(r1a2b_2)

    r1b2c_1 = GraphM(r1b, r2c, {
        nr1b_0 : nr2c_0,
        nr1b_1 : nr2c_1,
        nr1b_2 : nr2c_2,
        er1b_0 : er2c_0,
        er1b_1 : er2c_1,
        er1b_2 : er2c_2,
        er1b_3 : er2c_3
    })

    r1b2c_1p = r11b.compose(r1b2c_1)
    
    r1b2c_2 = GraphM(r1b, r2c, {
        nr1b_0 : nr2c_2,
        nr1b_1 : nr2c_3,
        nr1b_2 : nr2c_4,
        er1b_0 : er2c_4,
        er1b_1 : er2c_5,
        er1b_2 : er2c_6,
        er1b_3 : er2c_7
    })

    r1b2c_2p = r11b.compose(r1b2c_2)
    
    r1b2c_3 = GraphM(r1b, r2c, {
        nr1b_0 : nr2c_4,
        nr1b_1 : nr2c_5,
        nr1b_2 : nr2c_0,
        er1b_0 : er2c_8,
        er1b_1 : er2c_9,
        er1b_2 : er2c_10,
        er1b_3 : er2c_11
    })

    r1b2c_3p = r11b.compose(r1b2c_3)

    def er_2(lp):
        def er_2_exp(e1, e1p, e2, e2p, e3, e3p):
            if e1.OC == r1a and e2.OC == r1a and e3.OC == r1a:
                ret = ParGraphO(r2a, {nl2_0 : e1.ET[nl1_0],
                                      nl2_1 : e2.ET[nl1_0],
                                      nl2_2 : e3.ET[nl1_0],
                                     })
                return (ret, [
                                 ParGraphM(r1a, r2a, r1a2a_0),
                                 ParGraphM(r1a, r2a, r1a2a_0p),
                                 ParGraphM(r1a, r2a, r1a2a_1),
                                 ParGraphM(r1a, r2a, r1a2a_1p),
                                 ParGraphM(r1a, r2a, r1a2a_2),
                                 ParGraphM(r1a, r2a, r1a2a_2p),
                             ],
                             [
                                 ParGraphM(r2a.restrict(l22_1).dom, r2a, l22_1),
                                 ParGraphM(r2a.restrict(l22_2).dom, r2a, l22_2),
                                 ParGraphM(r2a.restrict(l22_3).dom, r2a, l22_3),
                                 ParGraphM(r2a.restrict(l22_4).dom, r2a, l22_4),
                                 ParGraphM(r2a.restrict(l22_5).dom, r2a, l22_5)
                             ])
            elif e1.OC == r1a and e2.OC == r1b and e3.OC == r1a:
                ret = ParGraphO(r2b, {nr2b_0 : False,
                                      nr2b_1 : True,
                                      nr2b_2 : True,
                                      nr2b_3 : True
                                     })
                return (ret, [
                                 ParGraphM(r1a, r2b, r1a2b_0),
                                 ParGraphM(r1a, r2b, r1a2b_0p),
                                 ParGraphM(r1b, r2b, r1b2b_1),
                                 ParGraphM(r1b, r2b, r1b2b_1p),
                                 ParGraphM(r1a, r2b, r1a2b_2),
                                 ParGraphM(r1a, r2b, r1a2b_2p),
                             ],
                             [
                                 None,
                                 None,
                                 ParGraphM(r2b.restrict(r2c2c_3).dom, r2b, r2c2c_3),
                                 None,
                                 None
                             ])
            elif e1.OC == r1a and e2.OC == r1a and e3.OC == r1b:
                ret = ParGraphO(r2b, {nr2b_0 : False,
                                      nr2b_1 : True,
                                      nr2b_2 : True,
                                      nr2b_3 : True
                                     })
                return (ret, [
                                 ParGraphM(r1a, r2b, r1a2b_2),
                                 ParGraphM(r1a, r2b, r1a2b_2p),
                                 ParGraphM(r1a, r2b, r1a2b_0),
                                 ParGraphM(r1a, r2b, r1a2b_0p),
                                 ParGraphM(r1b, r2b, r1b2b_1),
                                 ParGraphM(r1b, r2b, r1b2b_1p),
                             ],
                             [
                                 None,
                                 None,
                                 ParGraphM(r2b.restrict(r2c2c_3).dom, r2b, r2c2c_3),
                                 None,
                                 None
                             ])
            elif e1.OC == r1b and e2.OC == r1a and e3.OC == r1a:
                ret = ParGraphO(r2b, {nr2b_0 : False,
                                      nr2b_1 : True,
                                      nr2b_2 : True,
                                      nr2b_3 : True
                                     })
                return (ret, [
                                 ParGraphM(r1b, r2b, r1b2b_1),
                                 ParGraphM(r1b, r2b, r1b2b_1p),
                                 ParGraphM(r1a, r2b, r1a2b_2),
                                 ParGraphM(r1a, r2b, r1a2b_2p),
                                 ParGraphM(r1a, r2b, r1a2b_0),
                                 ParGraphM(r1a, r2b, r1a2b_0p),
                             ],
                             [
                                 None,
                                 None,
                                 ParGraphM(r2b.restrict(r2c2c_3).dom, r2b, r2c2c_3),
                                 None,
                                 None
                             ])
            else:
                pass
        return er_2_exp

    def er_2_auto(auto):
        def er_2_exp(e1, e1p, e2, e2p, e3, e3p):
            ret = auto.dom
            if e1.OC == r1a and e2.OC == r1a and e3.OC == r1a:
                ret_test = ParGraphO(r2a, {nl2_0 : e1.ET[nl1_0],
                                      nl2_1 : e2.ET[nl1_0],
                                      nl2_2 : e3.ET[nl1_0],
                                     })
                assert ret == ret_test
                return (ret, [
                                 ParGraphM(r1a, r2a, r1a2a_0),
                                 ParGraphM(r1a, r2a, r1a2a_0p),
                                 ParGraphM(r1a, r2a, r1a2a_1),
                                 ParGraphM(r1a, r2a, r1a2a_1p),
                                 ParGraphM(r1a, r2a, r1a2a_2),
                                 ParGraphM(r1a, r2a, r1a2a_2p),
                             ],
                             [
                                 ParGraphM(r2a.restrict(l22_1).dom, r2a, l22_1),
                                 ParGraphM(r2a.restrict(l22_2).dom, r2a, l22_2),
                                 ParGraphM(r2a.restrict(l22_3).dom, r2a, l22_3),
                                 ParGraphM(r2a.restrict(l22_4).dom, r2a, l22_4),
                                 ParGraphM(r2a.restrict(l22_5).dom, r2a, l22_5)
                             ])
            elif e1.OC == r1a and e2.OC == r1b and e3.OC == r1a:
                ret_test = ParGraphO(r2b, {nr2b_0 : False,
                                      nr2b_1 : True,
                                      nr2b_2 : True,
                                      nr2b_3 : True
                                     })
                assert ret == ret_test
                return (ret, [
                                 ParGraphM(r1a, r2b, r1a2b_0),
                                 ParGraphM(r1a, r2b, r1a2b_0p),
                                 ParGraphM(r1b, r2b, r1b2b_1),
                                 ParGraphM(r1b, r2b, r1b2b_1p),
                                 ParGraphM(r1a, r2b, r1a2b_2),
                                 ParGraphM(r1a, r2b, r1a2b_2p),
                             ],
                             [
                                 None,
                                 None,
                                 ParGraphM(r2b.restrict(r2c2c_3).dom, r2b, r2c2c_3),
                                 None,
                                 None
                             ])
            elif e1.OC == r1a and e2.OC == r1a and e3.OC == r1b:
                ret_test = ParGraphO(r2b, {nr2b_0 : False,
                                      nr2b_1 : True,
                                      nr2b_2 : True,
                                      nr2b_3 : True
                                     })
                assert ret == ret_test
                return (ret, [
                                 ParGraphM(r1a, r2b, r1a2b_2),
                                 ParGraphM(r1a, r2b, r1a2b_2p),
                                 ParGraphM(r1a, r2b, r1a2b_0),
                                 ParGraphM(r1a, r2b, r1a2b_0p),
                                 ParGraphM(r1b, r2b, r1b2b_1),
                                 ParGraphM(r1b, r2b, r1b2b_1p),
                             ],
                             [
                                 None,
                                 None,
                                 ParGraphM(r2b.restrict(r2c2c_3).dom, r2b, r2c2c_3),
                                 None,
                                 None
                             ])
            elif e1.OC == r1b and e2.OC == r1a and e3.OC == r1a:
                ret_test = ParGraphO(r2b, {nr2b_0 : False,
                                      nr2b_1 : True,
                                      nr2b_2 : True,
                                      nr2b_3 : True
                                     })
                assert ret == ret_test
                return (ret, [
                                 ParGraphM(r1b, r2b, r1b2b_1),
                                 ParGraphM(r1b, r2b, r1b2b_1p),
                                 ParGraphM(r1a, r2b, r1a2b_2),
                                 ParGraphM(r1a, r2b, r1a2b_2p),
                                 ParGraphM(r1a, r2b, r1a2b_0),
                                 ParGraphM(r1a, r2b, r1a2b_0p),
                             ],
                             [
                                 None,
                                 None,
                                 ParGraphM(r2b.restrict(r2c2c_3).dom, r2b, r2c2c_3),
                                 None,
                                 None
                             ])
            else:
                pass
        return er_2_exp

    g_2 = epf.add_fam_exp_rule(l2, er_2, er_2_auto, 5)

    g_1_2_0 = epf.add_fam_exp_inclusion(g_1, g_2, l12_0, 0)
    g_1_2_0p = epf.add_fam_exp_inclusion(g_1, g_2, l12_0p, 1)
    g_1_2_1 = epf.add_fam_exp_inclusion(g_1, g_2, l12_1, 2)
    g_1_2_1p = epf.add_fam_exp_inclusion(g_1, g_2, l12_1p, 3)
    g_1_2_2 = epf.add_fam_exp_inclusion(g_1, g_2, l12_2, 4)
    g_1_2_2p = epf.add_fam_exp_inclusion(g_1, g_2, l12_2p, 5)

    g_2_2_1 = epf.add_fam_exp_inclusion(g_2, g_2, l22_1, 0)
    g_2_2_2 = epf.add_fam_exp_inclusion(g_2, g_2, l22_2, 1)
    g_2_2_3 = epf.add_fam_exp_inclusion(g_2, g_2, l22_3, 2)
    g_2_2_4 = epf.add_fam_exp_inclusion(g_2, g_2, l22_4, 3)
    g_2_2_5 = epf.add_fam_exp_inclusion(g_2, g_2, l22_5, 4)

    epf = epf.get()
    T = GT(epf)

    g = GraphO()
    n1 = g.add_node()
    n2 = g.add_node()
    n3 = g.add_node()
    e1 = g.add_edge(n1, n2)
    e2 = g.add_edge(n2, n1)
    e3 = g.add_edge(n2, n3)
    e4 = g.add_edge(n3, n2)
    e5 = g.add_edge(n3, n1)
    e6 = g.add_edge(n1, n3)

    g = ParGraphO(g, {n1 : False, n2 : False, n3 : False})
    # print(len(g.g.nodes))

    #plt.subplot(121)
    options = {
        'node_color': 'black',
        'node_size': 20,
        'width': 1,
    }

    GraphModule.show = False
    # options['edge_colors'] = g.ET
    #ec = [ 'red' if g.ET[v] else 'blue' for v in g.OC.nodes()]
    #print(ec)
    nx.draw(g.OC.g, layout=nx.spring_layout(g.OC.g), node_size = 20, width = 1)#**options)
    plt.show()
    print("drawed")
    for i in range(0, 6):
        #if i == 3:
        #    GraphModule.show = True
        g_ = T.extend(g)
        g = tuple(g_)[0].object
        print("sub", cptsub)
        # options['edge_colors'] = g.ET
        # plt.subplot(121)
        ec = [ 'red' if g.ET[v] else 'blue' for v in g.OC.nodes()]
        print(ec)
        nx.draw(g.OC.g, layout=nx.spring_layout(g.OC.g), node_color= ec, node_size = 20, width = 1)#**options)
        plt.show()

    print(len(g.OC.nodes))
    print(len(g.OC.edges))

def test_graph_ndv2():
    from GT_DU_2 import GT_DU, OPFunctor
    # seed(10)

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

    g0 = fpfm.add_o_rule(l0, r0C, lambda c, incs : r0)

    g1 = fpfm.add_o_rule(l1, r1C, lambda c, incs : r1a if random() > 0.5 else r1b)

    fpfm.add_o_inclusion(g0, g1, l01_0)
    fpfm.add_o_inclusion(g0, g1, l01_1)

    fpfm.add_o_inclusion(g1, g1, l11)
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
        s = T.extend(s).object
        # print(len(sp))
        # s = tuple(sp)[0].object
        nx.draw_kamada_kawai(s.g, **options)
        plt.show()
        # print(s)
    
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
    from GT_DU_2 import GT_DU, OPFunctor
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
        s = T.extend(s).object
        print(s)
        print(type(s))
        nx.draw_kamada_kawai(s.g, **options)
        plt.show()
        # print(s)

# test_seq()
test_graph_old() # basic bugged gt
# test_graph() # basic triang mesh refinement
# test_graph_nd()
# test_graph_nda_sheaf_2()
# test_graph_ndv2()
# test_graph_ndv2_2()
# test_graph_ndv2_AC()


#
