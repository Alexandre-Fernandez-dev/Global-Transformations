from DataStructure import DataStructure
from GT import GT

# remove this useless class
class Parametrisation:

    @staticmethod
    def get(C, T):
        def object_init(self, OC, ET):
            assert isinstance(OC, C.TO())
            # TODO need check ET.dom == OC.elements ?
            self.OC = OC
            self.ET = ET

        def object_repr(self):
            return "PARO < " + str(self.OC) + ", " + str(self.ET) + " >"

        def object_naked(self):
            return self.OC

        def object_eq(self, other):
            if not isinstance(other, ObjectClass):
                return False
            return self.OC == other.OC and self.ET == other.ET

        def object_hash(self):
            return hash(self.OC) ^ 31 * T['parhash'](self.ET)

        def object_restrict(self, h):
            assert h.cod == self.OC
            ET = T['restriction'](h, self.ET)
            if h.dom == h.cod and ET == self.ET:
                # assert False # used in gmap
                return MorphismClass(self, self, h)
            else:
                return MorphismClass(ObjectClass(h.dom, ET), self, h)

        ObjectClass = type(C.__name__ + "__" + T['name'] + "O", (), {
            '__init__'     : object_init,
            '__repr__'     : object_repr,
            '__hash__'     : object_hash,
            '__eq__'       : object_eq,
            'naked'        : object_naked,
            'restrict'     : object_restrict
        })

        def morphism_init(self, s, t, MC):
            assert isinstance(MC, C.TM())
            assert isinstance(s, ObjectClass)
            assert isinstance(t, ObjectClass)
            self.s = s
            self.t = t
            self.MC = MC
            hash(self)

        def morphism_compose(self, h):
            return MorphismClass(self.s, h.t, self.MC.compose(h.MC))

        def morphism_eq(self, other):
            if not isinstance(other, MorphismClass):
                return False
            return self.MC == other.MC and self.s == other.s and self.t == other.t

        def morphism_hash(self):
            r = hash(self.MC)
            r ^= 31 * hash(self.s)
            r ^= 31 * hash(self.t)
            return r

        def morphism_dom(self):
            return self.s

        def morphism_cod(self):
            return self.t

        def morphism_clean(self):
            self.MC.clean()

        def morphism_repr(self):
            return "PARM " + repr(self.s) + " -> " + repr(self.t) + " : " + str(self.MC)

        def morphism_naked(self):
            return self.MC

        MorphismClass = type(C.__name__ + "__" + T['name'] + "M", (), {
            '__init__'  : morphism_init,
            'compose'   : morphism_compose,
            '__eq__'    : morphism_eq,
            '__hash__'  : morphism_hash,
            'dom'       : property(morphism_dom),
            'cod'       : property(morphism_cod),
            'clean'     : morphism_clean,
            '__repr__'  : morphism_repr,
            'naked'     : morphism_naked
        })

        def Category_pattern_match_fam(p, s):
            if isinstance(p, C.TM()):
                matches = C.pattern_match(p, s.naked())
                p = p.cod
                s = s.cod
            else:
                matches = C.pattern_match(p, s.naked())
            for m in matches:
                restr = T['restriction'](m, s.ET)
                yield MorphismClass(ObjectClass(p, restr), s, m)

        def Category_pattern_match(p, s):
            if isinstance(p, MorphismClass):
                matches = C.pattern_match(p.MC, s.MC)
                p = p.cod
                s = s.cod
            else:
                matches = C.pattern_match(p.OC, s.OC)
            for m in matches:
                restr = T['restriction'](m, s.ET)
                if restr.keys() != p.ET.keys():
                    continue
                ok = True
                for k, v in restr.items():
                    if p.ET[k] != v:
                        ok = False
                        break
                if ok:
                    yield MorphismClass(p, s, m)

        def Category_multi_merge(m1s, m2s):
            m1sMC = [ m1.MC for m1 in m1s]
            m2sMC = [ m2.MC for m2 in m2s]
            m10 = m1s[0].cod
            m20 = m2s[0].cod
            r, m1r, m2r = C.multi_merge(m1sMC, m2sMC)
            amal = T['amalgamation'](m1r, m10.ET, m2r, m20.ET)
            res = ObjectClass(r, amal)
            m1p = MorphismClass(m10, res, m1r)
            m2p = MorphismClass(m20, res, m2r)
            return res, m1p, m2p

        def Category_multi_merge_2_in_1(m1s, m2s):
            m1sMC = [ m1.MC for m1 in m1s]
            m2sMC = [ m2.MC for m2 in m2s]
            m10 = m1s[0].cod
            m20 = m2s[0].cod
            _, m2r = C.multi_merge_2_in_1(m1sMC, m2sMC)
            T['amalgamation_2_in_1'](m10.ET, m2r, m20.ET)
            m2p = MorphismClass(m20, m10, m2r)
            return m10, m2p

        CategoryClass = type(C.__name__ + "__" + T['name'], (DataStructure,), {
            'pattern_match_fam'   : Category_pattern_match_fam,
            'pattern_match'       : Category_pattern_match,
            'multi_merge'         : Category_multi_merge,
            'multi_merge_2_in_1'  : Category_multi_merge_2_in_1,
        })

        return ObjectClass, MorphismClass, CategoryClass

class Test:
    @staticmethod
    def triangle_mesh_refinement():
        from Graph import Graph

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
        import PFunctor

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