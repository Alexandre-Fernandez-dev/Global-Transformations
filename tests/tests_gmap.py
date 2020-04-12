import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from PFunctor import FlatPFunctor, FamPFunctor, ExpPFunctor, FamExpPFunctor
from Gmap import Premap, PremapO, PremapM
from GT import GT
import Sheaf
import math
from DataStructure import Lazy
from random import random

def test_pmatching():
    p0 = PremapO(2)
    d0a = p0.add_dart()
    d0b = p0.add_dart()
    p0.sew(0,d0a,d0b)

    p1 = PremapO(2)
    d1a = p1.add_dart()
    d1b = p1.add_dart()
    d1c = p1.add_dart()
    d1d = p1.add_dart()
    d1e = p1.add_dart()
    d1f = p1.add_dart()
    p1.sew(0,d1a,d1b)
    p1.sew(1,d1b,d1c)
    p1.sew(0,d1c,d1d)
    p1.sew(1,d1d,d1e)
    p1.sew(0,d1e,d1f)
    p1.sew(1,d1f,d1a)

    p2 = PremapO(2)
    d2a = p2.add_dart()
    d2b = p2.add_dart()
    d2c = p2.add_dart()
    d2d = p2.add_dart()
    p2.sew(0,d2a,d2b)
    p2.sew(0,d2c,d2d)
    p2.sew(2,d2a,d2c)
    p2.sew(2,d2b,d2d)

    print(p0)
    print(p1)
    print(p2)

    idp0 = PremapM(p0,p0,[ d for d in p0 ])
    idp1 = PremapM(p1,p1,[ d for d in p1 ])
    idp2 = PremapM(p2,p2,[ d for d in p2 ])

    for m in Premap.pattern_match(p0,p1):
        print(m)
        print("morph")
        for mm in Premap.pattern_match(m,m):
            print('  * ', mm)

    print("-------")
    h1 = PremapM(p0,p1,[0,1])
    h2 = PremapM(p0,p2,[0,1])
    print(Premap.multi_merge([h1],[h2]))

    print("-------")
    h1 = PremapM(p0,p1,[0,1])
    h2 = PremapM(p0,p1,[0,1])
    h3 = PremapM(p0,p1,[3,2])
    h4 = PremapM(p0,p1,[3,2])
    print(Premap.multi_merge([h1,h3],[h2,h4]))

def gt():

    fpf = FlatPFunctor.Maker(Premap, Premap)

    l0 = PremapO(2)
    l0d0 = l0.add_dart()
    l0d1 = l0.add_dart()
    l0.sew(0, l0d0, l0d1)

    r0 = PremapO(2)
    r0d0 = r0.add_dart()
    r0d1 = r0.add_dart()
    r0d2 = r0.add_dart()
    r0d3 = r0.add_dart()
    r0.sew(0, r0d0, r0d1)
    r0.sew(1, r0d1, r0d2)
    r0.sew(0, r0d2, r0d3)

    g0 = fpf.add_rule(l0, r0)

    l1 = PremapO(2)
    l1d0 = l1.add_dart()
    l1d1 = l1.add_dart()
    l1.sew(0, l1d0, l1d1)
    l1d2 = l1.add_dart()
    l1d3 = l1.add_dart()
    l1.sew(0, l1d2, l1d3)
    l1.sew(2, l1d0, l1d2)
    l1.sew(2, l1d1, l1d3)

    r1 = PremapO(2)
    r1d0 = r1.add_dart()
    r1d1 = r1.add_dart()
    r1d2 = r1.add_dart()
    r1d3 = r1.add_dart()
    r1.sew(0, r1d0, r1d1)
    r1.sew(1, r1d1, r1d2)
    r1.sew(0, r1d2, r1d3)
    r1d4 = r1.add_dart()
    r1d5 = r1.add_dart()
    r1d6 = r1.add_dart()
    r1d7 = r1.add_dart()
    r1.sew(0, r1d4, r1d5)
    r1.sew(1, r1d5, r1d6)
    r1.sew(0, r1d6, r1d7)
    r1.sew(2, r1d0, r1d4)
    r1.sew(2, r1d1, r1d5)
    r1.sew(2, r1d2, r1d6)
    r1.sew(2, r1d3, r1d7)

    g1 = fpf.add_rule(l1, r1)

    l2 = PremapO(2)
    l2d0 = l2.add_dart()
    l2d1 = l2.add_dart()
    l2.sew(0, l2d0, l2d1)
    l2d2 = l2.add_dart()
    l2d3 = l2.add_dart()
    l2.sew(0, l2d2, l2d3)
    l2.sew(1, l2d1, l2d2)
    l2d4 = l2.add_dart()
    l2d5 = l2.add_dart()
    l2.sew(0, l2d4, l2d5)
    l2.sew(1, l2d3, l2d4)
    l2.sew(1, l2d5, l2d0)

    r2 = PremapO(2)
    r2d0 = r2.add_dart()
    r2d1 = r2.add_dart()
    r2.sew(0, r2d0, r2d1)
    r2d2 = r2.add_dart()
    r2d3 = r2.add_dart()
    r2.sew(0, r2d2, r2d3)
    r2.sew(1, r2d1, r2d2)
    r2d4 = r2.add_dart()
    r2d5 = r2.add_dart()
    r2.sew(0, r2d4, r2d5)
    r2.sew(1, r2d3, r2d4)
    r2.sew(1, r2d5, r2d0)
    r2d6 = r2.add_dart()
    r2d7 = r2.add_dart()
    r2.sew(0, r2d6, r2d7)
    r2d8 = r2.add_dart()
    r2d9 = r2.add_dart()
    r2.sew(0, r2d8, r2d9)
    r2.sew(1, r2d7, r2d8)
    r2d10 = r2.add_dart()
    r2d11 = r2.add_dart()
    r2.sew(0, r2d10, r2d11)
    r2.sew(1, r2d9, r2d10)
    r2.sew(1, r2d11, r2d6)
    r2d12 = r2.add_dart()
    r2d13 = r2.add_dart()
    r2.sew(0, r2d12, r2d13)
    r2d14 = r2.add_dart()
    r2d15 = r2.add_dart()
    r2.sew(0, r2d14, r2d15)
    r2.sew(1, r2d13, r2d14)
    r2d16 = r2.add_dart()
    r2d17 = r2.add_dart()
    r2.sew(0, r2d16, r2d17)
    r2.sew(1, r2d15, r2d16)
    r2.sew(1, r2d17, r2d12)
    r2d18 = r2.add_dart()
    r2d19 = r2.add_dart()
    r2.sew(0, r2d18, r2d19)
    r2d20 = r2.add_dart()
    r2d21 = r2.add_dart()
    r2.sew(0, r2d20, r2d21)
    r2.sew(1, r2d19, r2d20)
    r2d22 = r2.add_dart()
    r2d23 = r2.add_dart()
    r2.sew(0, r2d22, r2d23)
    r2.sew(1, r2d21, r2d22)
    r2.sew(1, r2d23, r2d18)
    r2.sew(2, r2d3, r2d18)
    r2.sew(2, r2d2, r2d19)
    r2.sew(2, r2d11, r2d20)
    r2.sew(2, r2d10, r2d21)
    r2.sew(2, r2d13, r2d22)
    r2.sew(2, r2d12, r2d23)

    g2 = fpf.add_rule(l2, r2)

    incl01a = PremapM(l0, l1, [l1d0, l1d1])
    incl01b = PremapM(l0, l1, [l1d2, l1d3])

    incr01a = PremapM(r0, r1, [r1d0, r1d1, r1d2, r1d3])
    incr01b = PremapM(r0, r1, [r1d4, r1d5, r1d6, r1d7])

    inc01a = fpf.add_inclusion(g0, g1, incl01a, incr01a)
    inc01b = fpf.add_inclusion(g0, g1, incl01b, incr01b)

    incl02a = PremapM(l0, l2, [l2d0, l2d1])
    incl02b = PremapM(l0, l2, [l2d2, l2d3])
    incl02c = PremapM(l0, l2, [l2d4, l2d5])

    incr02a = PremapM(r0, r2, [r2d0, r2d1, r2d6, r2d7])
    incr02b = PremapM(r0, r2, [r2d8, r2d9, r2d14, r2d15])
    incr02c = PremapM(r0, r2, [r2d16, r2d17, r2d4, r2d5])

    inc02a = fpf.add_inclusion(g0, g2, incl02a, incr02a)
    inc02b = fpf.add_inclusion(g0, g2, incl02b, incr02b)
    inc02c = fpf.add_inclusion(g0, g2, incl02c, incr02c)

    fl00 = PremapM(l0, l0, [l0d1, l0d0])
    fr00 = PremapM(r0, r0, [r0d3, r0d2, r0d1, r0d0])

    auto0 = fpf.add_inclusion(g0, g0, fl00, fr00)

    f1l1 = PremapM(l1, l1, [l1d1, l1d0, l1d3, l1d2])
    f1r1 = PremapM(r1, r1, [r1d3, r1d2, r1d1, r1d0, r1d7, r1d6, r1d5, r1d4])

    autof11 = fpf.add_inclusion(g1, g1, f1l1, f1r1)

    f2l1 = PremapM(l1, l1, [l1d2, l1d3, l1d0, l1d1])
    f2r1 = PremapM(r1, r1, [r1d4, r1d5, r1d6, r1d7, r1d0, r1d1, r1d2, r1d3])

    autof21 = fpf.add_inclusion(g1, g1, f2l1, f2r1)

    f12l1 = f1l1.compose(f2l1)
    f12r1 = f1r1.compose(f2r1)

    autof121 = fpf.add_inclusion(g1, g1, f12l1, f12r1)

    rl22a = PremapM(l2, l2, [l2d2, l2d3, l2d4, l2d5, l2d0, l2d1])
    rr22a = PremapM(r2, r2, [r2d8, r2d9, r2d10, r2d11, r2d6, r2d7, r2d14, r2d15, r2d16, r2d17, r2d12, r2d13, r2d2, r2d3, r2d4, r2d5, r2d0, r2d1, r2d20, r2d21, r2d22, r2d23, r2d18, r2d19])

    auto2ra = fpf.add_inclusion(g2, g2, rl22a, rr22a)

    rl22b = rl22a.compose(rl22a)
    rr22b = rr22a.compose(rr22a)

    auto2rb = fpf.add_inclusion(g2, g2, rl22b, rr22b)

    fl22 = PremapM(l2, l2, [l2d5, l2d4, l2d3, l2d2, l2d1, l2d0])
    fr22 = PremapM(r2, r2, [r2d5, r2d4, r2d3, r2d2, r2d1, r2d0, r2d17, r2d16, r2d15, r2d14, r2d13, r2d12, r2d11, r2d10, r2d9, r2d8, r2d7, r2d6, r2d19, r2d18, r2d23, r2d22, r2d21, r2d20])

    auto2f = fpf.add_inclusion(g2, g2, fl22, fr22)

    rfl22a = fl22.compose(rl22a)
    rfr22a = fr22.compose(rr22a)

    auto2fra = fpf.add_inclusion(g2, g2, rfl22a, rfr22a)

    rfl22b = rfl22a.compose(rl22a)
    rfr22b = rfr22a.compose(rr22a)

    auto2frb = fpf.add_inclusion(g2, g2, rfl22b, rfr22b)

    f = fpf.get()

    tri = PremapO(2)
    trid0 = tri.add_dart()
    trid1 = tri.add_dart()
    tri.sew(1, trid0, trid1)
    trid2 = tri.add_dart()
    trid3 = tri.add_dart()
    tri.sew(1, trid2, trid3)
    tri.sew(0, trid1, trid2)
    trid4 = tri.add_dart()
    trid5 = tri.add_dart()
    tri.sew(1, trid4, trid5)
    tri.sew(0, trid3, trid4)
    tri.sew(0, trid5, trid0)

    T = GT(f)

    res1 = tuple(T.extend(tri))[0].object
    print("1", len(res1))
    res2 = tuple(T.extend(res1))[0].object
    print("2", len(res2))
    res3 = tuple(T.extend(res2))[0].object
    print("3", len(res3))
    res4 = tuple(T.extend(res3))[0].object
    print("4", len(res4))
    res5 = tuple(T.extend(res4))[0].object
    print("5", len(res5))
    res6 = tuple(T.extend(res5))[0].object
    print("6", len(res6))
    print()
    print(tri)
    print()
    print(res1)
    print(len(res1))
    print(len(list(res1.iter_icells(0))))
    print(len(list(res1.iter_icells(1))))
    print(len(list(res1.iter_icells(2))))
    print()
    print(res2)
    print(len(res2))
    print(len(list(res2.iter_icells(0))))
    print(len(list(res2.iter_icells(1))))
    print(len(list(res2.iter_icells(2))))
    # for m in Premap.pattern_match(l1, res1):
    #     print(m)

    # print("sew triangles test")

    # dsidedtri, lifttri, liftdside = Premap.multi_merge([incl02a], [incl01a])
    # print(dsidedtri, liftdside)

    # incprime = incl01b.compose(liftdside)
    # print(incprime)

    # # # C'est là les test de pattern match qui marchent pas !!
    # doubletri, _, _, = Premap.multi_merge([incl02a], [incprime]) #deux triangles collés par alpha2
    # print("DOUBLE TRI", doubletri)
    # print(len(doubletri))
    # print(len(list(doubletri.iter_icells(0))))
    # print(len(list(doubletri.iter_icells(1))))
    # print(len(list(doubletri.iter_icells(2))))
    # print(list(doubletri.iter_icells(0)))

    # for m in Premap.pattern_match(l0, doubletri):
    #     print("=====")
    #     print("match", m)
    #     print("now matching up :")
    #     for mp in Premap.pattern_match(incl01a, m):
    #         print("  returned", mp)
    # r = tuple(T.extend(doubletri))[0].object
    # print(len(doubletri))

    # print(len(r), r)

class Test:
    @staticmethod
    def sheaf_nodes():

        def restriction(f, q):
            ret = {}
            # TODO :genericity with element operator ?
        #  for n in f.dom.iter_icells(0):
        #      print("fdomic", n)
        #  for n in f.cod.iter_icells(0):
        #      print("fcodic", n)
            for n in f.dom.iter_icells(0):
                # print(n)
                # print(q)
                # print("f.l", f.l)
                ret[n] = q[f.cod.get_icell(0, f.apply(n))]
            return ret

        def amalgamation(f, p, g, q):
            assert f.cod == g.cod
            ret = {}
            for n in f.dom.iter_icells(0):
                ret[f.cod.get_icell(0, f.apply(n))] = p[n]

            for n in g.dom.iter_icells(0):
                gn = g.cod.get_icell(0, g.apply(n))
                if gn not in ret:
                    ret[gn] = q[n]
                elif ret[gn] != q[n]:
                    raise Exception("fail amalgamation")

            # print('amalgamation', len(list(g.cod.iter_icells(0))), len(ret))
            return ret

        def amalgamation_2_in_1(ret, g, q):
            # ugly HARD FIX need to investigate, the ret is not valid as his object as been modified by a merge2in1
            # old = list(ret.keys())
            # for i in range(0, len(old)):
            #     k = old[i]
            #     kp = g.cod.get_icell(0, k)
            #     if kp != k:
            #         if kp in ret:
            #             assert ret[k] == ret[kp]
            #         else:
            #             ret[kp] = ret[k]
            #         del ret[k]
            # end ugly fixe
            for n in g.dom.iter_icells(0):
                gn = g.cod.get_icell(0, g.apply(n))
                if gn not in ret:
                    ret[gn] = q[n]
                elif ret[gn] != q[n]:
                    raise Exception("fail amalgamation 2 in 1")

        def phash(p): # TODO WHY NOT NEEDED, REMOVE ?
            r = 1
            # r = 31 * len(p.items())
            # for k, v in p.items():
            #     r ^= 31 * hash(k)
            #     r ^= 31 * hash(v)
            return r

        ParNodesGmap = {
            'name'                  : "ParNodeGmap",
            'parhash'               : phash,
            'restriction'           : restriction,
            'amalgamation'          : amalgamation,
            'amalgamation_2_in_1'   : amalgamation_2_in_1
        }

        CO, CM, C = Sheaf.Parametrisation.get(Premap, ParNodesGmap)

        fpf = FamPFunctor.Maker(C, C)

        l0 = PremapO(2)
        l0d0 = l0.add_dart()
        l0d1 = l0.add_dart()
        l0.sew(0, l0d0, l0d1)

        r0 = PremapO(2)
        r0d0 = r0.add_dart()
        r0d1 = r0.add_dart()
        r0d2 = r0.add_dart()
        r0d3 = r0.add_dart()
        r0.sew(0, r0d0, r0d1)
        # r0.sew(1, r0d1, r0d2)
        r0.sew(0, r0d2, r0d3)
        def r0_(x):
            assert x.OC == l0
            p = {r0d0: x.ET[l0d0],
                r0d1: ((x.ET[l0d0][0] + x.ET[l0d1][0])/2, (x.ET[l0d0][1] + x.ET[l0d1][1])/2, (x.ET[l0d0][2] + x.ET[l0d1][2])/2),
                r0d2: ((x.ET[l0d0][0] + x.ET[l0d1][0])/2, (x.ET[l0d0][1] + x.ET[l0d1][1])/2, (x.ET[l0d0][2] + x.ET[l0d1][2])/2),
                r0d3: x.ET[l0d1]}
            r0p = CO(r0, p)
            return r0p

        g0 = fpf.add_fam_exp_rule(l0, r0_)

        l1 = PremapO(2)
        l1d0 = l1.add_dart()
        l1d1 = l1.add_dart()
        l1.sew(0, l1d0, l1d1)
        l1d2 = l1.add_dart()
        l1d3 = l1.add_dart()
        l1.sew(0, l1d2, l1d3)
        l1.sew(2, l1d0, l1d2)
        l1.sew(2, l1d1, l1d3)

        r1 = PremapO(2)
        r1d0 = r1.add_dart()
        r1d1 = r1.add_dart()
        r1d2 = r1.add_dart()
        r1d3 = r1.add_dart()
        r1.sew(0, r1d0, r1d1)
        # r1.sew(1, r1d1, r1d2)
        r1.sew(0, r1d2, r1d3)
        r1d4 = r1.add_dart()
        r1d5 = r1.add_dart()
        r1d6 = r1.add_dart()
        r1d7 = r1.add_dart()
        r1.sew(0, r1d4, r1d5)
        # r1.sew(1, r1d5, r1d6)
        r1.sew(0, r1d6, r1d7)
        r1.sew(2, r1d0, r1d4)
        r1.sew(2, r1d1, r1d5)
        r1.sew(2, r1d2, r1d6)
        r1.sew(2, r1d3, r1d7)

        def r1_(x):
            assert x.OC == l1
            p = {r1d0: x.ET[l1d0],
                r1d1: ((x.ET[l1d0][0] + x.ET[l1d1][0])/2, (x.ET[l1d0][1] + x.ET[l1d1][1])/2, (x.ET[l1d0][2] + x.ET[l1d1][2])/2),
                r1d2: ((x.ET[l1d0][0] + x.ET[l1d1][0])/2, (x.ET[l1d0][1] + x.ET[l1d1][1])/2, (x.ET[l1d0][2] + x.ET[l1d1][2])/2),
                r1d3: x.ET[l1d1]}
            r1p = CO(r1, p)
            return r1p

        g1 = fpf.add_fam_rule(l1, r1_)

        l2 = PremapO(2)
        l2d0 = l2.add_dart()
        l2d1 = l2.add_dart()
        l2.sew(0, l2d0, l2d1)
        l2d2 = l2.add_dart()
        l2d3 = l2.add_dart()
        l2.sew(0, l2d2, l2d3)
        l2.sew(1, l2d1, l2d2)
        l2d4 = l2.add_dart()
        l2d5 = l2.add_dart()
        l2.sew(0, l2d4, l2d5)
        l2.sew(1, l2d3, l2d4)
        l2.sew(1, l2d0, l2d5)

        r2 = PremapO(2)
        r2d0 = r2.add_dart()
        r2d1 = r2.add_dart()
        r2.sew(0, r2d0, r2d1)
        r2d2 = r2.add_dart()
        r2d3 = r2.add_dart()
        r2.sew(0, r2d2, r2d3)
        r2.sew(1, r2d1, r2d2)
        r2d4 = r2.add_dart()
        r2d5 = r2.add_dart()
        r2.sew(0, r2d4, r2d5)
        r2.sew(1, r2d3, r2d4)
        r2.sew(1, r2d0, r2d5)
        r2d6 = r2.add_dart()
        r2d7 = r2.add_dart()
        r2.sew(0, r2d6, r2d7)
        r2d8 = r2.add_dart()
        r2d9 = r2.add_dart()
        r2.sew(0, r2d8, r2d9)
        r2.sew(1, r2d7, r2d8)
        r2d10 = r2.add_dart()
        r2d11 = r2.add_dart()
        r2.sew(0, r2d10, r2d11)
        r2.sew(1, r2d9, r2d10)
        r2.sew(1, r2d6, r2d11)
        r2d12 = r2.add_dart()
        r2d13 = r2.add_dart()
        r2.sew(0, r2d12, r2d13)
        r2d14 = r2.add_dart()
        r2d15 = r2.add_dart()
        r2.sew(0, r2d14, r2d15)
        r2.sew(1, r2d13, r2d14)
        r2d16 = r2.add_dart()
        r2d17 = r2.add_dart()
        r2.sew(0, r2d16, r2d17)
        r2.sew(1, r2d15, r2d16)
        r2.sew(1, r2d12, r2d17)
        r2d18 = r2.add_dart()
        r2d19 = r2.add_dart()
        r2.sew(0, r2d18, r2d19)
        r2d20 = r2.add_dart()
        r2d21 = r2.add_dart()
        r2.sew(0, r2d20, r2d21)
        r2.sew(1, r2d19, r2d20)
        r2d22 = r2.add_dart()
        r2d23 = r2.add_dart()
        r2.sew(0, r2d22, r2d23)
        r2.sew(1, r2d21, r2d22)
        r2.sew(1, r2d18, r2d23)
        r2.sew(2, r2d3, r2d18)
        r2.sew(2, r2d2, r2d19)
        r2.sew(2, r2d20, r2d11)
        r2.sew(2, r2d10, r2d21)
        r2.sew(2, r2d22, r2d13)
        r2.sew(2, r2d23, r2d12)

        def r2_(x):
            assert x.OC == l2
            p = {r2d0: x.ET[l2d0],
                r2d1: ((x.ET[l2d0][0] + x.ET[l2d1][0])/2, (x.ET[l2d0][1] + x.ET[l2d1][1])/2, (x.ET[l2d0][2] + x.ET[l2d1][2])/2),
                r2d7: x.ET[l2d1],
                r2d9: ((x.ET[l2d1][0] + x.ET[l2d3][0])/2, (x.ET[l2d1][1] + x.ET[l2d3][1])/2, (x.ET[l2d1][2] + x.ET[l2d3][2])/2),
                r2d15: x.ET[l1d3],
                r2d3: ((x.ET[l2d3][0] + x.ET[l2d0][0])/2, (x.ET[l2d3][1] + x.ET[l2d0][1])/2, (x.ET[l2d3][2] + x.ET[l2d0][2])/2)
            }
            r2p = CO(r2, p)
            return r2p

        g2 = fpf.add_fam_rule(l2, r2_)

        incl01a = PremapM(l0, l1, [l1d0, l1d1])
        incl01b = PremapM(l0, l1, [l1d2, l1d3])
        incl01c = PremapM(l0, l1, [l1d1, l1d0])
        incl01d = PremapM(l0, l1, [l1d3, l1d2])


        def incr01a(lps, lpo, rs, ro):
            gm = PremapM(rs.OC, ro.OC, [r1d0, r1d1, r1d2, r1d3])
            return CM(rs, ro, gm)

        def incr01b(lps, lpo, rs, ro):
            gm = PremapM(rs.OC, ro.OC, [r1d4, r1d5, r1d6, r1d7])
            return CM(rs, ro, gm)

        def incr01c(lps, lpo, rs, ro):
            gm = PremapM(rs.OC, ro.OC, [r1d3, r1d2, r1d1, r1d0])
            return CM(rs, ro, gm)

        def incr01d(lps, lpo, rs, ro):
            gm = PremapM(rs.OC, ro.OC, [r1d7, r1d6, r1d5, r1d4])
            return CM(rs, ro, gm)

        inc01a = fpf.add_fam_inclusion(g0, g1, incl01a, incr01a)
        inc01b = fpf.add_fam_inclusion(g0, g1, incl01b, incr01b)
        inc01c = fpf.add_fam_inclusion(g0, g1, incl01c, incr01c)
        inc01d = fpf.add_fam_inclusion(g0, g1, incl01d, incr01d)

        incl02a = PremapM(l0, l2, [l2d0, l2d1])
        incl02b = PremapM(l0, l2, [l2d2, l2d3])
        incl02c = PremapM(l0, l2, [l2d4, l2d5])
        incl02d = PremapM(l0, l2, [l2d1, l2d0])
        incl02e = PremapM(l0, l2, [l2d3, l2d2])
        incl02f = PremapM(l0, l2, [l2d5, l2d4])

        def incr02a(lps, lpo, rs, ro):
            gm = PremapM(rs.OC, ro.OC, [r2d0, r2d1, r2d6, r2d7])
            return CM(rs, ro, gm)

        def incr02b(lps, lpo, rs, ro):
            gm = PremapM(rs.OC, ro.OC, [r2d8, r2d9, r2d14, r2d15])
            return CM(rs, ro, gm)

        def incr02c(lps, lpo, rs, ro):
            gm = PremapM(rs.OC, ro.OC, [r2d16, r2d17, r2d4, r2d5])
            return CM(rs, ro, gm)

        def incr02d(lps, lpo, rs, ro):
            gm = PremapM(rs.OC, ro.OC, [r2d7, r2d6, r2d1, r2d0])
            return CM(rs, ro, gm)

        def incr02e(lps, lpo, rs, ro):
            gm = PremapM(rs.OC, ro.OC, [r2d15, r2d14, r2d9, r2d8])
            return CM(rs, ro, gm)

        def incr02f(lps, lpo, rs, ro):
            gm = PremapM(rs.OC, ro.OC, [r2d5, r2d4, r2d17, r2d16])
            return CM(rs, ro, gm)

        inc02a = fpf.add_fam_inclusion(g0, g2, incl02a, incr02a)
        inc02b = fpf.add_fam_inclusion(g0, g2, incl02b, incr02b)
        inc02c = fpf.add_fam_inclusion(g0, g2, incl02c, incr02c)
        inc02d = fpf.add_fam_inclusion(g0, g2, incl02d, incr02d)
        inc02e = fpf.add_fam_inclusion(g0, g2, incl02e, incr02e)
        inc02f = fpf.add_fam_inclusion(g0, g2, incl02f, incr02f)

        fl00 = PremapM(l0, l0, [l0d1, l0d0])

        def fr00(lps, lpo, rs, ro):
            gm = PremapM(rs.OC, ro.OC, [r0d3, r0d2, r0d1, r0d0])
            return CM(rs, ro, gm)

        auto0 = fpf.add_fam_inclusion(g0, g0, fl00, fr00)

        f1l1 = PremapM(l1, l1, [l1d1, l1d0, l1d3, l1d2])
        def f1r1(lps, lpo, rs, ro):
            gm = PremapM(rs.OC, ro.OC, [r1d3, r1d2, r1d1, r1d0, r1d7, r1d6, r1d5, r1d4])
            return CM(rs, ro, gm)

        autof11 = fpf.add_fam_inclusion(g1, g1, f1l1, f1r1)

        f2l1 = PremapM(l1, l1, [l1d2, l1d3, l1d0, l1d1])
        def f2r1(lps, lpo, rs, ro):
            gm = PremapM(rs.OC, ro.OC, [r1d4, r1d5, r1d6, r1d7, r1d0, r1d1, r1d2, r1d3])
            return CM(rs, ro, gm)

        autof21 = fpf.add_fam_inclusion(g1, g1, f2l1, f2r1)

        f12l1 = f1l1.compose(f2l1)
        def f12r1(lps, lpo, rs, ro):
            gm = PremapM(rs.OC, ro.OC, [r1d3, r1d2, r1d1, r1d0, r1d7, r1d6, r1d5, r1d4])
            gm1 = PremapM(rs.OC, ro.OC, [r1d4, r1d5, r1d6, r1d7, r1d0, r1d1, r1d2, r1d3])
            gm2 = gm.compose(gm1)
            return CM(rs, ro, gm2)

        autof121 = fpf.add_fam_inclusion(g1, g1, f12l1, f12r1)

        rl22a = PremapM(l2, l2, [l2d2, l2d3, l2d4, l2d5, l2d0, l2d1])
        def rr22a(lps, lpo, rs, ro):
            gm = PremapM(rs.OC, ro.OC, [r2d8, r2d9, r2d10, r2d11, r2d6, r2d7, r2d14, r2d15, r2d16, r2d17, r2d12, r2d13, r2d2, r2d3, r2d4, r2d5, r2d0, r2d1, r2d20, r2d21, r2d22, r2d23, r2d18, r2d19])
            return CM(rs, ro, gm)

        auto2ra = fpf.add_fam_inclusion(g2, g2, rl22a, rr22a)

        rl22b = rl22a.compose(rl22a)
        def rr22b(lps, lpo, rs, ro):
            gm1 = PremapM(rs.OC, ro.OC, [r2d8, r2d9, r2d10, r2d11, r2d6, r2d7, r2d14, r2d15, r2d16, r2d17, r2d12, r2d13, r2d2, r2d3, r2d4, r2d5, r2d0, r2d1, r2d20, r2d21, r2d22, r2d23, r2d18, r2d19])
            gm2 = gm1.compose(gm1)
            return CM(rs, ro, gm2)

        auto2rb = fpf.add_fam_inclusion(g2, g2, rl22b, rr22b)

        fl22 = PremapM(l2, l2, [l2d5, l2d4, l2d3, l2d2, l2d1, l2d0])
        def fr22(lps, lpo, rs, ro):
            gm = PremapM(rs.OC, ro.OC, [r2d5, r2d4, r2d3, r2d2, r2d1, r2d0, r2d17, r2d16, r2d15, r2d14, r2d13, r2d12, r2d11, r2d10, r2d9, r2d8, r2d7, r2d6, r2d19, r2d18, r2d23, r2d22, r2d21, r2d20])
            return CM(rs, ro, gm)

        auto2f = fpf.add_fam_inclusion(g2, g2, fl22, fr22)

        rfl22a = fl22.compose(rl22a)
        def rfr22a(lps, lpo, rs, ro):
            gm = PremapM(rs.OC, ro.OC, [r2d5, r2d4, r2d3, r2d2, r2d1, r2d0, r2d17, r2d16, r2d15, r2d14, r2d13, r2d12, r2d11, r2d10, r2d9, r2d8, r2d7, r2d6, r2d19, r2d18, r2d23, r2d22, r2d21, r2d20])
            gm1 = PremapM(rs.OC, ro.OC, [r2d8, r2d9, r2d10, r2d11, r2d6, r2d7, r2d14, r2d15, r2d16, r2d17, r2d12, r2d13, r2d2, r2d3, r2d4, r2d5, r2d0, r2d1, r2d20, r2d21, r2d22, r2d23, r2d18, r2d19])
            gm2 = gm.compose(gm1)
            return CM(rs, ro, gm2)

        auto2fra = fpf.add_fam_inclusion(g2, g2, rfl22a, rfr22a)

        rfl22b = rfl22a.compose(rl22a)
        def rfr22b(lps, lpo, rs, ro):
            gm = PremapM(rs.OC, ro.OC, [r2d5, r2d4, r2d3, r2d2, r2d1, r2d0, r2d17, r2d16, r2d15, r2d14, r2d13, r2d12, r2d11, r2d10, r2d9, r2d8, r2d7, r2d6, r2d19, r2d18, r2d23, r2d22, r2d21, r2d20])
            gm1 = PremapM(rs.OC, ro.OC, [r2d8, r2d9, r2d10, r2d11, r2d6, r2d7, r2d14, r2d15, r2d16, r2d17, r2d12, r2d13, r2d2, r2d3, r2d4, r2d5, r2d0, r2d1, r2d20, r2d21, r2d22, r2d23, r2d18, r2d19])
            gm2 = gm.compose(gm1)
            gm3 = PremapM(rs.OC, ro.OC, [r2d8, r2d9, r2d10, r2d11, r2d6, r2d7, r2d14, r2d15, r2d16, r2d17, r2d12, r2d13, r2d2, r2d3, r2d4, r2d5, r2d0, r2d1, r2d20, r2d21, r2d22, r2d23, r2d18, r2d19])
            gm4 = gm2.compose(gm3)
            return CM(rs, ro, gm4)

        auto2frb = fpf.add_fam_inclusion(g2, g2, rfl22b, rfr22b)

        f = fpf.get()

        tri = PremapO(2)
        trid0 = tri.add_dart()
        trid1 = tri.add_dart()
        tri.sew(0, trid0, trid1)
        trid2 = tri.add_dart()
        trid3 = tri.add_dart()
        tri.sew(0, trid2, trid3)
        tri.sew(1, trid1, trid2)
        trid4 = tri.add_dart()
        trid5 = tri.add_dart()
        tri.sew(0, trid4, trid5)
        tri.sew(1, trid3, trid4)
        tri.sew(1, trid0, trid5)
        p = {trid0: (0.0, 0.0, 0.0),
            trid1: (1.0, 0.0, 0.0),
            trid3: (0.5, 0.5, 0.0)
            }
        trip = CO(tri, p)

        T = GT(f)

        dsidedtri, lifttri, liftdside = Premap.multi_merge([incl02a], [incl01a])
        # print(dsidedtri, liftdside)
        p = {0: (0.0, 0.0, 0.0),
            1: (1.0, 0.0, 0.0),
            3: (0.5, 0.5, 0.0)
            }
        wtri = CO(dsidedtri, p)
        res1 = tuple(T.extend(wtri))[0].object
        # print(len(res1.OC))
        # print(res1)
        tt = PremapO(2)
        ttd0 = tt.add_dart()
        ttd1 = tt.add_dart()
        tt.sew(0, ttd0, ttd1)
        ttd2 = tt.add_dart()
        ttd3 = tt.add_dart()
        tt.sew(0, ttd2, ttd3)
        tt.sew(1, ttd1, ttd2)
        ttd4 = tt.add_dart()
        ttd5 = tt.add_dart()
        tt.sew(0, ttd4, ttd5)
        tt.sew(1, ttd3, ttd4)
        tt.sew(1, ttd0, ttd5)
        ttd6 = tt.add_dart()
        ttd7 = tt.add_dart()
        tt.sew(0, ttd6, ttd7)
        ttd8 = tt.add_dart()
        ttd9 = tt.add_dart()
        tt.sew(0, ttd8, ttd9)
        tt.sew(1, ttd7, ttd8)
        ttd10 = tt.add_dart()
        ttd11 = tt.add_dart()
        tt.sew(0, ttd10, ttd11)
        tt.sew(1, ttd9, ttd10)
        tt.sew(1, ttd6, ttd11)
        ttd12 = tt.add_dart()
        ttd13 = tt.add_dart()
        tt.sew(0, ttd12, ttd13)
        ttd14 = tt.add_dart()
        ttd15 = tt.add_dart()
        tt.sew(0, ttd14, ttd15)
        tt.sew(1, ttd13, ttd14)
        ttd16 = tt.add_dart()
        ttd17 = tt.add_dart()
        tt.sew(0, ttd16, ttd17)
        tt.sew(1, ttd15, ttd16)
        tt.sew(1, ttd12, ttd17)
        ttd18 = tt.add_dart()
        ttd19 = tt.add_dart()
        tt.sew(0, ttd18, ttd19)
        ttd20 = tt.add_dart()
        ttd21 = tt.add_dart()
        tt.sew(0, ttd20, ttd21)
        tt.sew(1, ttd19, ttd20)
        ttd22 = tt.add_dart()
        ttd23 = tt.add_dart()
        tt.sew(0, ttd22, ttd23)
        tt.sew(1, ttd21, ttd22)
        tt.sew(1, ttd18, ttd23)
        tt.sew(2, ttd3, ttd18)
        tt.sew(2, ttd2, ttd19)
        tt.sew(2, ttd20, ttd11)
        tt.sew(2, ttd10, ttd21)
        tt.sew(2, ttd22, ttd13)
        tt.sew(2, ttd23, ttd12)
        tt.sew(2, ttd0, ttd7)
        tt.sew(2, ttd1, ttd6)
        tt.sew(2, ttd8, ttd15)
        tt.sew(2, ttd9, ttd14)
        tt.sew(2, ttd5, ttd16)
        tt.sew(2, ttd4, ttd17)
        p = {r2d0: (-0.5, 0, 0),
             r2d1: (0.5, 0, 0),
             ttd9: (0, math.sqrt(3/4), 0),
             r2d3: (0, math.sqrt(3/4)/3, math.sqrt(2/3))
             }
        ttp = CO(tt, p)

        return T, ttp
        # res1 = tuple(T.extend(trip))[0].object
        # print("1", len(res1.OC))
        # res2 = tuple(T.extend(res1))[0].object
        # return res2
        # print("2", len(res2.OC))
        # res3 = tuple(T.extend(res2))[0].object
        # print("3", len(res3.OC))
        # res4 = tuple(T.extend(res3))[0].object
        # print("4", len(res4.OC))
        # res5 = tuple(T.extend(res4))[0].object
        # print("5", len(res5.OC))
        # res6 = tuple(T.extend(res5))[0].object
        # print("6", len(res6.OC))

        # print()
        # print("trip", trip)
        # print(len(trip.OC))
        # print(len(trip.ET))
        # print(len(list(trip.OC.iter_icells(0))))
        # print(len(list(trip.OC.iter_icells(1))))
        # print(len(list(trip.OC.iter_icells(2))))
        # print()
        # print("res1", res1)
        # print(len(res1.OC))
        # print(len(res1.ET))
        # print(len(list(res1.OC.iter_icells(0))))
        # print(len(list(res1.OC.iter_icells(1))))
        # print(len(list(res1.OC.iter_icells(2))))
        # print()
        # print("res2", res2)
        # print()
        # print(len(res2.OC))
        # print(len(res2.ET))
        # print(len(list(res2.OC.iter_icells(0))))
        # print(len(list(res2.OC.iter_icells(1))))
        # print(len(list(res2.OC.iter_icells(2))))
        #
        # l = set()
        # for i in res2.OC.iter_icells(0):
        #     print(res2.ET[i])
        # for j in res2.ET:
        #     print(j, res2.OC.get_icell(0, j))
        #     l.add(res2.OC.get_icell(0, j))
        # print(sorted(list(l)))
        # print(sorted(list(res2.OC.iter_icells(0))))
        # for i in sorted(list(res2.OC.iter_icells(0))):
        #     print(i)
        #     print(res2.ET[i])
        #
        # for d in range(0, res2.OC.D):
        #     print(d)
        #     a0 = res2.OC.alpha(0, d)
        #     a00 = res2.OC.alpha(0, a0)
        #     a1 = res2.OC.alpha(1, d)
        #     a11 = res2.OC.alpha(1, a1)
        #     a2 = res2.OC.alpha(2, d)
        #     a22 = res2.OC.alpha(2, a2)
        #     print(a00 == d, d, a0, a00)
        #     print(a11 == d, d, a1, a11)
        #     print(a22 == d, d, a2, a22)


        ################

        # for t in sorted(list(res2.OC.iter_icells(2))):
        #     print(t)
        #     print("nodes :")
        #     cont = True
        #     t0i = t
        #     print(res2.ET[res2.OC.get_icell(0, t0i)])
        #     while cont:
        #         t0ip = res2.OC.alpha(1, t0i)
        #         print(t0ip)
        #         t0i = res2.OC.alpha(0, t0ip)
        #         print(t0i, t)
        #         # print(res2.OC.get_icell(0, t0i), res2.OC.get_icell(0, t))
        #         if t == t0i:
        #             cont = False
        #         else:
        #             print(res2.ET[res2.OC.get_icell(0, t0i)])
        #             print(res2.ET[res2.OC.get_icell(0, t)])
        #             print(res2.OC.alpha(1, t))
        # for m in Premap.pattern_match(l1, res1):
        #     print(m)

        # print("sew triangles test")

        # dsidedtri, lifttri, liftdside = Premap.multi_merge([incl02a], [incl01a])
        # print(dsidedtri, liftdside)

        # incprime = incl01b.compose(liftdside)
        # print(incprime)

        # # C'est là les test de pattern match qui marchent pas !!
        # doubletri, _, _, = Premap.multi_merge([incl02a], [incprime]) #deux triangles collés par alpha2
        # print("DOUBLE TRI", doubletri)

        # # for m in Premap.pattern_match(l0, doubletri):
        # #     print("=====")
        # #     print("match", m)
        # #     print("now matching up :")
        # #     for mp in Premap.pattern_match(incl01a, m):
        # #         print("  returned", mp)
        # r = tuple(T.extend(doubletri))[0].object
        # print(len(doubletri))

        # print(len(r), r)

    @staticmethod
    def rivers():

        def restriction(f, q):
            ret = {}
            for n in f.dom.iter_icells(0):
                ret[(0, n)] = q[(0, f.cod.get_icell(0, f.apply(n)))]
            for e in f.dom.iter_icells(1):
                # print(q)
                # for qi in q:
                #     print(qi)
                #     print(qi[0], f.cod.get_icell(1, qi[1]))
                # # print({ (k[0], f.cod.get_icell(1, f.apply(k[1]))): v for k, v in q })
                ret[(1, e)] = q[(1, f.cod.get_icell(1, f.apply(e)))]
            return ret

        def amalgamation(f, p, g, q):
            assert f.cod == g.cod
            ret = {}
            for n in f.dom.iter_icells(0):
                ret[(0, f.cod.get_icell(0, f.apply(n)))] = p[(0, n)]

            for e in f.dom.iter_icells(1):
                ret[(1, f.cod.get_icell(1, f.apply(e)))] = p[(1, e)]

            for n in g.dom.iter_icells(0):
                gn = g.cod.get_icell(0, g.apply(n))
                if (0, gn) not in ret:
                    ret[(0, gn)] = q[(0, n)]
                elif ret[(0, gn)] != q[(0, n)]:
                    raise Exception("fail amalgamation")

            sf = set(f.l)
            sg = set(g.l)
            print(len(sf))
            print(sf)
            print(len(sg))
            print(sg)
            d = {}
            for i in range(len(f.l)):
                d1 = f.l[i]
                for j in range(len(g.l)):
                    d2 = g.l[j]
                    if d1 == d2:
                        d[d1] = (i, j)
            print(sf.intersection(sg))
            for k, v in d.items():
                print(k)
                print(p[(1, f.dom.get_icell(1, v[0]))])
                print(q[(1, g.dom.get_icell(1, v[1]))])
            for e in g.dom.iter_icells(1):
                ge = g.cod.get_icell(1, g.apply(e))
                if (1, ge) not in ret:
                    ret[(1, ge)] = q[(1, e)]
                elif ret[(1, ge)] != q[(1, e)]:
                    print(ret[(1, ge)], q[(1, e)])
                    raise Exception("fail amalgamation")

            # print('amalgamation', len(list(g.cod.iter_icells(0))), len(ret))
            return ret

        def amalgamation_2_in_1(ret, g, q):
            for n in g.dom.iter_icells(0):
                gn = g.cod.get_icell(0, g.apply(n))
                if (0, gn) not in ret:
                    ret[(0, gn)] = q[(0, n)]
                elif ret[(0, gn)] != q[(0, n)]:
                    raise Exception("fail amalgamation 2 in 1")

            for e in g.dom.iter_icells(1):
                ge = g.cod.get_icell(1, g.apply(e))
                if (1, ge) not in ret:
                    ret[(1, ge)] = q[(1, e)]
                elif ret[(1, ge)] != q[(1, e)]:
                    raise Exception("fail amalgamation 2 in 1")

        def phash(p):
            r = 1
            return r

        ParNodesEdgesGmap = {
            'name'                  : "ParNodeEdgeGmap",
            'parhash'               : phash,
            'restriction'           : restriction,
            'amalgamation'          : amalgamation,
            'amalgamation_2_in_1'   : amalgamation_2_in_1
        }

        CO, CM, C = Sheaf.Parametrisation.get(Premap, ParNodesEdgesGmap)
        LC = Lazy(C)

        epf = FamExpPFunctor.Maker(C, LC) # PRemap -> LC ???

        # l0 = PremapO(2)
        # l0d0 = l0.add_dart()
        # l0d1 = l0.add_dart()
        # l0.sew(0, l0d0, l0d1)

        # # l_a = SequenceO(['a'])
        # # def er_a():
        # #     return (SequenceO(['a','a']), []) if random() <= 0.5  else (SequenceO(['a']), [])
        # # g_a = epf.add_exp_rule(l_a, er_a)

        # r0 = PremapO(2)
        # r0d0 = r0.add_dart()
        # r0d1 = r0.add_dart()
        # r0d2 = r0.add_dart()
        # r0d3 = r0.add_dart()
        # r0.sew(0, r0d0, r0d1)
        # r0.sew(0, r0d2, r0d3)
        # def r0_(x):
        #     def r0__():
        #         assert x.OC == l0
        #         if x.ET[(1, l0d0)]:
        #             river = True
        #             r = random() > 0.5
        #         else:
        #             river = True
        #         p = {(0, r0d0): x.ET[(0, l0d0)],
        #             (0, r0d1): ((x.ET[(0, l0d0)][0] + x.ET[(0, l0d1)][0])/2, (x.ET[(0, l0d0)][1] + x.ET[(0, l0d1)][1])/2, (x.ET[(0, l0d0)][2] + x.ET[(0, l0d1)][2])/2),
        #             (0, r0d2): ((x.ET[(0, l0d0)][0] + x.ET[(0, l0d1)][0])/2, (x.ET[(0, l0d0)][1] + x.ET[(0, l0d1)][1])/2, (x.ET[(0, l0d0)][2] + x.ET[(0, l0d1)][2])/2),
        #             (0, r0d3): x.ET[(0, l0d1)],
        #             (1, r0d0): r if river == True else river,
        #             (1, r0d2): not r if river == True else river
        #             }
        #         return (CO(r0, p), [], [])
        #     return r0__

        l1 = PremapO(2)
        l1d0 = l1.add_dart()
        l1d1 = l1.add_dart()
        l1.sew(0, l1d0, l1d1)
        l1d2 = l1.add_dart()
        l1d3 = l1.add_dart()
        l1.sew(0, l1d2, l1d3)
        l1.sew(2, l1d0, l1d2)
        l1.sew(2, l1d1, l1d3)

        r1 = PremapO(2)
        r1d0 = r1.add_dart()
        r1d1 = r1.add_dart()
        r1d2 = r1.add_dart()
        r1d3 = r1.add_dart()
        r1.sew(0, r1d0, r1d1)
        # r1.sew(1, r1d1, r1d2)
        r1.sew(0, r1d2, r1d3)
        r1d4 = r1.add_dart()
        r1d5 = r1.add_dart()
        r1d6 = r1.add_dart()
        r1d7 = r1.add_dart()
        r1.sew(0, r1d4, r1d5)
        # r1.sew(1, r1d5, r1d6)
        r1.sew(0, r1d6, r1d7)
        r1.sew(2, r1d0, r1d4)
        r1.sew(2, r1d1, r1d5)
        r1.sew(2, r1d2, r1d6)
        r1.sew(2, r1d3, r1d7)

        # f1l1 = PremapM(l1, l1, [l1d1, l1d0, l1d3, l1d2])
        # f1r1 = PremapM(r1, r1, [r1d3, r1d2, r1d1, r1d0, r1d7, r1d6, r1d5, r1d4])

        f2l1 = PremapM(l1, l1, [l1d2, l1d3, l1d0, l1d1])
        f2r1 = PremapM(r1, r1, [r1d4, r1d5, r1d6, r1d7, r1d0, r1d1, r1d2, r1d3])

        # f3l1 = f1l1.compose(f2l1)
        # f3r1 = f1r1.compose(f2r1)

        def r1_(x):
            def r1__():
                assert x.OC == l1
                river = x.ET[(1, l1d0)]
                if river:
                    #assert x.ET[(1, l1d2)]
                    r = random() > 0.5
                p = {(0, r1d0): x.ET[(0, l1d0)],
                    (0, r1d1): ((x.ET[(0, l1d0)][0] + x.ET[(0, l1d1)][0])/2, (x.ET[(0, l1d0)][1] + x.ET[(0, l1d1)][1])/2, (x.ET[(0, l1d0)][2] + x.ET[(0, l1d1)][2])/2),
                    (0, r1d2): ((x.ET[(0, l1d0)][0] + x.ET[(0, l1d1)][0])/2, (x.ET[(0, l1d0)][1] + x.ET[(0, l1d1)][1])/2, (x.ET[(0, l1d0)][2] + x.ET[(0, l1d1)][2])/2),
                    (0, r1d3): x.ET[(0, l1d1)],
                    (1, r1d0): r if river == True else river,
                    (1, r1d2): not r if river == True else river}
                ret = CO(r1, p)
                return (ret, [], [CM(ret.restrict(f2r1).dom, ret, f2r1)])#[CM(ret, ret, f1r1), CM(ret, ret, f2r1), CM(ret, ret, f3r1)])
            return r1__

        g1 = epf.add_fam_exp_rule(l1, r1_, 1)#3)
        ag1_2 = epf.add_fam_exp_inclusion(g1, g1, f2l1, 0)

        # ag1_1 = epf.add_fam_exp_inclusion(g1, g1, f1l1, 0)
        # ag1_2 = epf.add_fam_exp_inclusion(g1, g1, f2l1, 1)
        # ag1_3 = epf.add_fam_exp_inclusion(g1, g1, f3l1, 2)

        l2 = PremapO(2)
        l2d0 = l2.add_dart()
        l2d1 = l2.add_dart()
        l2.sew(0, l2d0, l2d1)
        l2d2 = l2.add_dart()
        l2d3 = l2.add_dart()
        l2.sew(0, l2d2, l2d3)
        l2.sew(1, l2d1, l2d2)
        l2d4 = l2.add_dart()
        l2d5 = l2.add_dart()
        l2.sew(0, l2d4, l2d5)
        l2.sew(1, l2d3, l2d4)
        l2.sew(1, l2d0, l2d5)
        l2d0p = l2.add_dart()
        l2d1p = l2.add_dart()
        l2.sew(0, l2d0p, l2d1p)
        l2d2p = l2.add_dart()
        l2d3p = l2.add_dart()
        l2.sew(0, l2d2p, l2d3p)
        l2d4p = l2.add_dart()
        l2d5p = l2.add_dart()
        l2.sew(0, l2d4p, l2d5p)
        l2.sew(2, l2d0, l2d0p)
        l2.sew(2, l2d1, l2d1p)
        l2.sew(2, l2d2, l2d2p)
        l2.sew(2, l2d3, l2d3p)
        l2.sew(2, l2d4, l2d4p)
        l2.sew(2, l2d5, l2d5p)

        r2 = PremapO(2)
        r2d0 = r2.add_dart()
        r2d1 = r2.add_dart()
        r2.sew(0, r2d0, r2d1)
        r2d2 = r2.add_dart()
        r2d3 = r2.add_dart()
        r2.sew(0, r2d2, r2d3)
        r2.sew(1, r2d1, r2d2)
        r2d4 = r2.add_dart()
        r2d5 = r2.add_dart()
        r2.sew(0, r2d4, r2d5)
        r2.sew(1, r2d3, r2d4)
        r2.sew(1, r2d0, r2d5)
        r2d6 = r2.add_dart()
        r2d7 = r2.add_dart()
        r2.sew(0, r2d6, r2d7)
        r2d8 = r2.add_dart()
        r2d9 = r2.add_dart()
        r2.sew(0, r2d8, r2d9)
        r2.sew(1, r2d7, r2d8)
        r2d10 = r2.add_dart()
        r2d11 = r2.add_dart()
        r2.sew(0, r2d10, r2d11)
        r2.sew(1, r2d9, r2d10)
        r2.sew(1, r2d6, r2d11)
        r2d12 = r2.add_dart()
        r2d13 = r2.add_dart()
        r2.sew(0, r2d12, r2d13)
        r2d14 = r2.add_dart()
        r2d15 = r2.add_dart()
        r2.sew(0, r2d14, r2d15)
        r2.sew(1, r2d13, r2d14)
        r2d16 = r2.add_dart()
        r2d17 = r2.add_dart()
        r2.sew(0, r2d16, r2d17)
        r2.sew(1, r2d15, r2d16)
        r2.sew(1, r2d12, r2d17)
        r2d18 = r2.add_dart()
        r2d19 = r2.add_dart()
        r2.sew(0, r2d18, r2d19)
        r2d20 = r2.add_dart()
        r2d21 = r2.add_dart()
        r2.sew(0, r2d20, r2d21)
        r2.sew(1, r2d19, r2d20)
        r2d22 = r2.add_dart()
        r2d23 = r2.add_dart()
        r2.sew(0, r2d22, r2d23)
        r2.sew(1, r2d21, r2d22)
        r2.sew(1, r2d18, r2d23)
        r2.sew(2, r2d3, r2d18)
        r2.sew(2, r2d2, r2d19)
        r2.sew(2, r2d20, r2d11)
        r2.sew(2, r2d10, r2d21)
        r2.sew(2, r2d22, r2d13)
        r2.sew(2, r2d23, r2d12)
        r2d0p = r2.add_dart()
        r2d1p = r2.add_dart()
        r2.sew(0, r2d0p, r2d1p)
        r2d4p = r2.add_dart()
        r2d5p = r2.add_dart()
        r2.sew(0, r2d4p, r2d5p)
        r2d6p = r2.add_dart()
        r2d7p = r2.add_dart()
        r2.sew(0, r2d6p, r2d7p)
        r2d8p = r2.add_dart()
        r2d9p = r2.add_dart()
        r2.sew(0, r2d8p, r2d9p)
        r2d14p = r2.add_dart()
        r2d15p = r2.add_dart()
        r2.sew(0, r2d14p, r2d15p)
        r2d16p = r2.add_dart()
        r2d17p = r2.add_dart()
        r2.sew(0, r2d16p, r2d17p)
        r2.sew(2, r2d0, r2d0p)
        r2.sew(2, r2d1, r2d1p)
        r2.sew(2, r2d4, r2d4p)
        r2.sew(2, r2d5, r2d5p)
        r2.sew(2, r2d6, r2d6p)
        r2.sew(2, r2d7, r2d7p)
        r2.sew(2, r2d8, r2d8p)
        r2.sew(2, r2d9, r2d9p)
        r2.sew(2, r2d14, r2d14p)
        r2.sew(2, r2d15, r2d15p)
        r2.sew(2, r2d16, r2d16p)
        r2.sew(2, r2d17, r2d17p)

        incl12_1 = PremapM(l1, l2, [l2d0, l2d1, l2d0p, l2d1p])
        incl12_1p = PremapM(l1, l2, [l2d0p, l2d1p, l2d0, l2d1])
        incl12_2 = PremapM(l1, l2, [l2d2, l2d3, l2d2p, l2d3p])
        incl12_2p = PremapM(l1, l2, [l2d2p, l2d3p, l2d2, l2d3])
        incl12_3  = PremapM(l1, l2, [l2d4, l2d5, l2d4p, l2d5p])
        incl12_3p  = PremapM(l1, l2, [l2d4p, l2d5p, l2d4, l2d5])

        incr12_1 = PremapM(r1, r2, [r2d0, r2d1, r2d6, r2d7, r2d0p, r2d1p, r2d6p, r2d7p])
        incr12_1p = PremapM(r1, r2, [r2d0p, r2d1p, r2d6p, r2d7p, r2d0, r2d1, r2d6, r2d7])
        incr12_2 = PremapM(r1, r2, [r2d8, r2d9, r2d14, r2d15, r2d8p, r2d9p, r2d14p, r2d15p])
        incr12_2p = PremapM(r1, r2, [r2d8p, r2d9p, r2d14p, r2d15p, r2d8, r2d9, r2d14, r2d15])
        incr12_3 = PremapM(r1, r2, [r2d16, r2d17, r2d4, r2d5, r2d16p, r2d17p, r2d4p, r2d5p])
        incr12_3p = PremapM(r1, r2, [r2d16p, r2d17p, r2d4p, r2d5p, r2d16, r2d17, r2d4, r2d5])

        r1l2 = PremapM(l2, l2, [l2d2, l2d3, l2d4, l2d5, l2d0, l2d1, l2d2p, l2d3p, l2d4p, l2d5p, l2d0p, l2d1p])
        r1r2 = PremapM(r2, r2, [r2d8, r2d9, r2d10, r2d11, r2d6, r2d7, r2d14, r2d15, r2d16, r2d17, r2d12, r2d13, r2d2, r2d3, r2d4, r2d5, r2d0, r2d1, r2d20, r2d21, r2d22, r2d23, r2d18, r2d19, r2d8p, r2d9p, r2d6p, r2d7p, r2d14p, r2d15p, r2d16p, r2d17p, r2d4p, r2d5p, r2d0p, r2d1p])

        r2l2 = r1l2.compose(r1l2)
        r2r2 = r1r2.compose(r1r2)
        
        fl2 = PremapM(l2, l2, [l2d5, l2d4, l2d3, l2d2, l2d1, l2d0, l2d5p, l2d4p, l2d3p, l2d2p, l2d1p, l2d0p])
        fr2 = PremapM(r2, r2, [r2d5, r2d4, r2d3, r2d2, r2d1, r2d0, r2d17, r2d16, r2d15, r2d14, r2d13, r2d12, r2d11, r2d10, r2d9, r2d8, r2d7, r2d6, r2d19, r2d18, r2d23, r2d22, r2d21, r2d20, r2d5p, r2d4p, r2d1p, r2d0p, r2d17p, r2d16p, r2d15p, r2d14p, r2d9p, r2d8p, r2d7p, r2d6p])

        fr1l2 = fl2.compose(r1l2)
        fr1r2 = fr2.compose(r1r2)

        fr2l2 = fl2.compose(r2l2)
        fr2r2 = fr2.compose(r2r2)

        def incr02c(lps, lpo, rs, ro):
            gm = PremapM(rs.OC, ro.OC, [])
            return CM(rs, ro, gm)

        def r2_(x):
            def r2__(e1, e1p, e2, e2p, e3, e3p):
                assert x.OC == l2
                p = {(0, r2d0): x.ET[(0, l2d0)],
                    (0, r2d1): ((x.ET[(0, l2d0)][0] + x.ET[(0, l2d1)][0])/2, (x.ET[(0, l2d0)][1] + x.ET[(0, l2d1)][1])/2, (x.ET[(0, l2d0)][2] + x.ET[(0, l2d1)][2])/2),
                    (0, r2d7): x.ET[(0, l2d1)],
                    (0, r2d9): ((x.ET[(0, l2d1)][0] + x.ET[(0, l2d3)][0])/2, (x.ET[(0, l2d1)][1] + x.ET[(0, l2d3)][1])/2, (x.ET[(0, l2d1)][2] + x.ET[(0, l2d3)][2])/2),
                    (0, r2d15): x.ET[(0, l1d3)],
                    (0, r2d3): ((x.ET[(0, l2d3)][0] + x.ET[(0, l2d0)][0])/2, (x.ET[(0, l2d3)][1] + x.ET[(0, l2d0)][1])/2, (x.ET[(0, l2d3)][2] + x.ET[(0, l2d0)][2])/2),
                    (1, r2d0): e1.ET[(1, r1d0)],
                    (1, r2d2): e1.ET[(1, r1d0)] is not e3.ET[(1, r1d2)],
                    (1, r2d6): e1.ET[(1, r1d2)],
                    (1, r2d8): e2.ET[(1, r1d0)],
                    (1, r2d10): e1.ET[(1, r1d2)] is not e2.ET[(1, r1d0)],
                    (1, r2d12): e2.ET[(1, r1d2)] is not e3.ET[(1, r1d0)],
                    (1, r2d14): e2.ET[(1, r1d2)],
                    (1, r2d16): e3.ET[(1, r1d0)],
                    (1, r2d4): e3.ET[(1, r1d2)]
                }
                r2p = CO(r2, p)
                return (r2p, [CM(e1, r2p, incr12_1), CM(e1p, r2p, incr12_1p), CM(e2, r2p, incr12_2), CM(e2p, r2p, incr12_2p), CM(e3, r2p, incr12_3), CM(e3p, r2p, incr12_3p)], [CM(r2p.restrict(r1r2).dom, r2p, r1r2), CM(r2p.restrict(r2r2).dom, r2p, r2r2), CM(r2p.restrict(fr2).dom, r2p, fr2), CM(r2p.restrict(fr1r2).dom, r2p, fr1r2), CM(r2p.restrict(fr2r2).dom, r2p, fr2r2)])
            return r2__

        g2 = epf.add_fam_exp_rule(l2, r2_, 5)

        inc12_1 = epf.add_fam_exp_inclusion(g1, g2, incl12_1, 0)
        inc12_1p = epf.add_fam_exp_inclusion(g1, g2, incl12_1p, 1)
        inc12_2 = epf.add_fam_exp_inclusion(g1, g2, incl12_2, 2)
        inc12_2p = epf.add_fam_exp_inclusion(g1, g2, incl12_2p, 3)
        inc12_3 = epf.add_fam_exp_inclusion(g1, g2, incl12_3, 4)
        inc12_3p = epf.add_fam_exp_inclusion(g1, g2, incl12_3p, 5)

        ag2_1 = epf.add_fam_exp_inclusion(g2, g2, r1l2, 0)
        ag2_2 = epf.add_fam_exp_inclusion(g2, g2, r2l2, 1)
        ag2_3 = epf.add_fam_exp_inclusion(g2, g2, fl2, 2)
        ag2_4 = epf.add_fam_exp_inclusion(g2, g2, fr1l2, 3)
        ag2_5 = epf.add_fam_exp_inclusion(g2, g2, fr2l2, 4)
        
        f = epf.get()

        p = {(0, l2d0): (0.0, 0.0, 0.0),
            (0, l2d1): (1.0, 0.0, 0.0),
            (0, l2d3): (0.5, 0.5, 0.0),
            (1, l2d0): True,
            (1, l2d2): True,
            (1, l2d4): False
            }
        trip = CO(l2, p)

        T = GT(f)

        return T, trip

        # g0 = fpf.add_fam_rule(l0, r0_)

        # l_a = SequenceO(['a'])
        # def er_a():
        #     return (SequenceO(['a','a']), []) if random() <= 0.5  else (SequenceO(['a']), [])
        # g_a = epf.add_exp_rule(l_a, er_a)

        # l_aa = SequenceO(['a','a'])
        # def er_aa(s1,s2):
        #     ret = SequenceO(s1.s + s2.s)
        #     return (ret, [ SequenceM(s1,ret,0) , SequenceM(s2,ret,len(s1.s)) ])
        # g_aa = epf.add_exp_rule(l_aa, er_aa)

        # l_a_aa_0 = SequenceM(l_a,l_aa,0)
        # ir_a_aa_0 = 0
        # g_a_aa_0 = epf.add_exp_inclusion(g_a, g_aa, l_a_aa_0, ir_a_aa_0)

        # l_a_aa_1 = SequenceM(l_a,l_aa,1)
        # ir_a_aa_1 = 1
        # g_a_aa_1 = epf.add_exp_inclusion(g_a, g_aa, l_a_aa_1, ir_a_aa_1)

        # epf = epf.get()

        # T = GT(epf)

        # sz = {}
        # for i in range(0,100):
        #     s = len(tuple(T.extend(SequenceO(['a','a','a'])))[0].object)
        #     sz[s] = sz.setdefault(s,0) + 1
        # print({s: 8*n/100 for (s,n) in sz.items() })
        # print((tuple(T.extend(SequenceO(['a','a','a'])))[0].object))



if __name__ == "__main__":
    # test_merge()
    # test_pmatching()
    # test_pmatching2()
    # test_pmatching()
    # gt()
    T, gp = Test.sheaf_nodes()
    for i in range(0, 5):
        gp = tuple(T.extend(gp))[0].object
    # Test.rivers()