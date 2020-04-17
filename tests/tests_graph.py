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
from random import random

def test_graph():
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
    T = GT(pfT)

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
    for i in range(4):
        if i == 3:
            GraphModule.show = True
        # print("------------------------------------------COMPUTE START", i)
        g_ = T.extend(g)
        # print(g_)
        g = tuple(g_)[0].object
        plt.subplot(121)
        # figManager = plt.get_current_fig_manager()
        # figManager.window.showMaximized()
        nx.draw_kamada_kawai(g.g, **options)
        plt.show()

    print(len(g.nodes))
    print(len(g.edges))
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
                ma = ParGraphM(res, res, r11b)
                return (res.restrict(r11b).dom, [m1, m2], [ma])
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
                ma = ParGraphM(res, res, r11b)
                return (res.restrict(r11b).dom, [m1, m2], [ma])
            else:
                res = auto.dom
                m1 = ParGraphM(s1, res, r01_0a)
                m2 = ParGraphM(s2, res, r01_1a)
                ma = ParGraphM(res.restrict(r11a).dom, res, r11a)
                return (res, [m1, m2], [ma])
        return er_1_exp
    g_1 = epf.add_fam_exp_rule(l1, er_1, er_1_auto, 1)

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

# test_seq()
# test_graph()
# test_graph_nd()
test_graph_nda_sheaf_2()


#
