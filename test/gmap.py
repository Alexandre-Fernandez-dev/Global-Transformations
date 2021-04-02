import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from engine.PFunctor import FlatPFunctor, FamPFunctor
from data.Gmap import Premap, PremapO, PremapM
import data.Sheaf as Sheaf
import math
from random import random

class Test:
    @staticmethod
    def sheaf_nodes():

        from engine import GT

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

        g0 = fpf.add_fam_rule(l0, r0_)

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

        T = GT.GT(f)

        dsidedtri, lifttri, liftdside = Premap.multi_merge([incl02a], [incl01a])
        # print(dsidedtri, liftdside)
        p = {0: (0.0, 0.0, 0.0),
            1: (1.0, 0.0, 0.0),
            3: (0.5, 0.5, 0.0)
            }
        wtri = CO(dsidedtri, p)
        res1 = T.extend(wtri).object
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

if __name__ == "__main__":
    T, gp = Test.sheaf_nodes()
    for i in range(0, 5):
        gp = T.extend(gp).object
