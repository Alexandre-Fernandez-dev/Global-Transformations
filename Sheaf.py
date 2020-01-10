from DataStructure import DataStructure
from GT import GT

# remove this useless class
class Parametrisation:

    @staticmethod
    def get(C, T):
        def object_init(self, OC, ET):
            # print(OC)
            # print(self.C.TO())
            assert isinstance(OC, C.TO()) 
            # TODO need check ET.dom == OC.elements ?
            # assert isinstance(ET, self.T.TE())
            self.OC = OC
            self.ET = ET

        def object_repr(self):
            return "PARO < " + str(self.OC) + ", " + str(self.ET) + " >"

        ObjectClass = type(C.__name__ + "__" + T['name'] + "O", (DataStructure,), {
            '__init__'  : object_init,
            '__repr__'  : object_repr
        })

        def morphism_init(self, s, t, MC):
            assert isinstance(MC, C.TM())
            # print("init : ", type(s), s, "\n", type(t), t)
            assert isinstance(s, ObjectClass)
            assert isinstance(t, ObjectClass)
            self.s = s
            self.t = t
            self.MC = MC
            hash(self)
        
        def morphism_compose(self, h):
            return MorphismClass(self.s, h.t, self.MC.compose(h.MC))
        
        def morphism_eq(self, other):
            # print("# eq")
            # print("#", self)
            # print("#", other)
            if not isinstance(other, MorphismClass):
                # print("# return false because not instance morphism")
                return False
            # print("#", self)
            # print("#", other)
            # print("# return ", self.s.ET == other.s.ET and self.t.ET == other.t.ET and self.MC == other.MC)
            # print("#", self.s.ET == other.s.ET)
            # print("#", self.t.ET == other.t.ET)
            # print("#", self.MC, other.MC)
            # print("#", self.MC == other.MC)
            return self.s.ET == other.s.ET and self.t.ET == other.t.ET and self.MC == other.MC
        
        def morphism_hash(self):
            r = hash(self.MC)
            r ^= 31 * hash(self.s)
            r ^= 31 * hash(self.t)
            # # print("hash before", r)
            # for k, v in self.s.ET.items():
            #     r ^= 31 * hash(k) + hash(v)
            # for k, v in self.t.ET.items():
            #     r ^= 31 * hash(k) + hash(v)
            # print("hash after", r)
            return r

        def morphism_dom(self):
            return self.s

        def morphism_cod(self):
            return self.t
        
        def morphism_clean(self):
            self.MC.clean()
        
        def morphism_repr(self):
            return "PARM " + repr(self.s) + " -> " + repr(self.t) + " : " + str(self.MC)

        MorphismClass = type(C.__name__ + "__" + T['name'] + "M", (DataStructure,), {
            '__init__'  : morphism_init,
            'compose'   : morphism_compose,
            '__eq__'    : morphism_eq,
            '__hash__'  : morphism_hash,
            'dom'       : property(morphism_dom),
            'cod'       : property(morphism_cod),
            'clean'     : morphism_clean,
            '__repr__'  : morphism_repr
        })

        def Category_pattern_match(p, s):
            # print(type(p), type(s))
            if isinstance(p, MorphismClass):
                # print("first", p.MC, s.MC)
                matches = C.pattern_match(p.MC, s.MC)
                p = p.cod
                s = s.cod
            else:
                # print("second")
                matches = C.pattern_match(p.OC, s.OC)
            for m in matches:
                restr = T['restriction'](m, s.ET)
                # print(restr)
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
        
        # def Category_merge(m1, m2):
        #     r, m1r, m2r = C.merge(m1.MC, m2.MC)
        #     amal = T['amalgamation'](m1r, m1.cod.ET, m2r, m2.cod.ET)
        #     res = ObjectClass(r, amal)
        #     m1p = MorphismClass(m1.cod, res, m1r)
        #     m2p = MorphismClass(m2.cod, res, m1r)
        #     return res, m1p, m2p

        def Category_multi_merge_2_in_1(m1s, m2s):
            m1sMC = [ m1.MC for m1 in m1s]
            m2sMC = [ m2.MC for m2 in m2s]
            m10 = m1s[0].cod
            m20 = m2s[0].cod
            _, m2r = C.multi_merge_2_in_1(m1sMC, m2sMC)
            T['amalgamation_2_in_1'](m10.ET, m2r, m20.ET)
            m2p = MorphismClass(m20, m10, m2r)
            return m10, m2p

        # def Category_merge_2_in_1(m1, m2):
        #     _, m2r = C.merge_2_in_1(m1.MC, m2.MC)
        #     T['amagamation_2_in_1'](m1.cod.ET, m2r, m2.cod.ET)
        #     m2p = MorphismClass(m2.cod, m1.cod, m2r)
        #     return m1.cod, m2p

        # def Category_quotient(m1, m2):
        #     r, mr = C.quotient(m1.MC, m2.MC)
        #     amal = T['amalgamation_quotient'](mr, m1.cod.ET)
        #     res = ObjectClass(r, amal)
        #     mrp = MorphismClass(m1.cod, res, mr)
        #     return res, mrp
        
        CategoryClass = type(C.__name__ + "__" + T['name'], (DataStructure,), {
            'pattern_match' : Category_pattern_match,
            'multi_merge'         : Category_multi_merge,
            'multi_merge_2_in_1'  : Category_multi_merge_2_in_1,
            #'merge'         : Category_merge,
            #'merge_2_in_1'  : Category_merge_2_in_1,
            #'quotient'      : Category_quotient
        })

        return ObjectClass, MorphismClass, CategoryClass

def test():
    from Graph import Graph

    def TE():
        return int

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

    ParameterGraphFloat = {
        'name'                  : "Float",
        'TE'                    : TE,
        'restriction'           : restriction,
        'amalgamation'          : amalgamation,
        'amalgamation_2_in_1'   : amalgamation_2_in_1,
        'amalgamation_quotient' : amalgamation_quotient
    }

    CO, CM, C = Parametrisation.get(Graph, ParameterGraphFloat)
    test = set()

    g = Graph.TO()()
    gn0 = g.add_node()
    gn1 = g.add_node()
    ge0 = g.add_edge(gn0, gn1)
    p = {gn0 : 0, gn1: 1, ge0 : -1}
    gp = CO(g, p)
    print(gp)

    g1 = Graph.TO()()
    g1n0 = g1.add_node()
    g1n1 = g1.add_node()
    g1n2 = g1.add_node()
    g1e0 = g1.add_edge(g1n0, g1n1)
    g1e1 = g1.add_edge(g1n1, g1n2)
    g1e2 = g1.add_edge(g1n2, g1n0)
    p1 =  {g1n0 : 0, g1n1 : 1, g1n2 : 2, g1e0 : -1, g1e1 : -2, g1e2 : -3}
    g1p = CO(g1, p1)
    print(g1p)

    g2 = g1.copy()
    p2 =  {g1n0 : 0, g1n1 : 1, g1n2 : 2, g1e0 : -1, g1e1 : -2, g1e2 : -3}
    g2p = CO(g2, p2)
    print(g1p)

    print()

    m1 = Graph.TM()(g, g1, {gn0 : g1n0, gn1 : g1n1, ge0 : g1e0})
    m1p = CM(gp, g1p, m1)
    print(m1p)
    test.add(m1p)

    m2 = Graph.TM()(g, g2, {gn0 : g1n0, gn1 : g1n1, ge0 : g1e0})
    m2p = CM(gp, g2p, m2)
    print(m2p)
    test.add(m2p)

    print(C.multi_merge([m1p], [m2p]))
    c, l1, l2 = C.multi_merge([m1p], [m2p])
    test.add(l1)
    test.add(l2)
    print(l1 in test, l2 in test, m1p in test, m2p in test)
    # return

    # m11 = Graph.TM()(g, g1, {gn0 : g1n0, gn1 : g1n1, ge0 : g1e0})
    # m11p = CM(gp, g1p, m11)
    # print(m11p)

    # m12 = Graph.TM()(g, g1, {gn0 : g1n1, gn1 : g1n2, ge0 : g1e1})
    # m12p = CM(gp, g1p, m12)
    # print(m12p)

    # print()
    # print(C.quotient(m11p, m12p))

    l0 = Graph.TO()()
    nl0 = l0.add_node()
    pl0 = {nl0 : 1}
    lp0 = CO(l0, pl0)

    print('lp0 : ', lp0)

    r0 = l0
    nr0 = nl0
    pr0 = {nr0 : 1}
    rp0 = CO(r0, pr0)

    print('rp0 : ', rp0)

    l1 = l0
    nl1 = nl0
    pl1 = {nl1 : 0}
    lp1 = CO(l1, pl1)

    print('lp1 : ', lp1)

    r1 = l1
    nr1 = nr0
    pr1 = {nr1 : 0}
    rp1 = CO(r1, pr1)

    print('rp1 : ', rp1)

    l2 = Graph.TO()()
    nl20 = l2.add_node()
    nl21 = l2.add_node()
    el2 = l2.add_edge(nl20, nl21)
    pl2 = {nl20 : 1, nl21 : 1, el2 : 0}
    lp2 = CO(l2, pl2)

    print('lp2 : ', lp2)

    r2 = Graph.TO()()
    nr20 = r2.add_node()
    nr21 = r2.add_node()
    nr22 = r2.add_node()
    er20 = r2.add_edge(nr20, nr21)
    er21 = r2.add_edge(nr21, nr22)
    pr2 = {nr20 : 1, nr21 : 1, nr22 : 1, er20 : 0, er21 : 0}
    rp2 = CO(r2, pr2)

    print('rp2 : ', rp2)

    l3 = l2
    nl30 = nl20
    nl31 = nl21
    el3 = el2
    pl3 = {nl30 : 1, nl31 : 0, el3 : 0}
    lp3 = CO(l3, pl3)

    print('lp3 : ', lp3)

    r3 = l2
    nr30 = nl20
    nr31 = nl21
    er3 = el2
    pr3 = {nr30 : 1, nr31 : 0, er3 : 0}
    rp3 = CO(r3, pr3)

    print('rp3 : ', rp3)

    l4 = l2
    nl40 = nl20
    nl41 = nl21
    el4 = el2
    pl4 = {nl40 : 0, nl41 : 1, el4 : 0}
    lp4 = CO(l4, pl4)

    print('lp4 : ', lp4)

    r4 = l2
    nr40 = nl20
    nr41 = nl21
    er4 = el2
    pr4 = {nr40 : 0, nr41 : 1, er4 : 0}
    rp4 = CO(r4, pr4)

    print('rp4 : ', rp4)

    l5 = l2
    nl50 = nl20
    nl51 = nl21
    el5 = el2
    pl5 = {nl50 : 0, nl51 : 0, el5 : 0}
    lp5 = CO(l5, pl5)

    print('lp5 : ', lp5)

    r5 = l2
    nr50 = nl20
    nr51 = nl21
    er5 = el2
    pr5 = {nr50 : 0, nr51 : 0, er5 : 0}
    rp5 = CO(r5, pr5)

    print('rp5 : ', rp5)

    inclfirst = Graph.TM()(l0, l2, {nl0 : nl20})
    inclsecond = Graph.TM()(l0, l2, {nl0 : nl21})

    incrfirsta = Graph.TM()(r0, r2, {nr0 : nr20})
    incrseconda = Graph.TM()(r0, r2, {nr0 : nr22})

    incrfirstb = Graph.TM()(r0, r3, {nr0 : nr30})
    incrsecondb = Graph.TM()(r0, r3, {nr0 : nr31})
    
    incl02a = CM(lp0, lp2, inclfirst)
    incr02a = CM(rp0, rp2, incrfirsta)

    incl02b = CM(lp0, lp2, inclsecond)
    incr02b = CM(rp0, rp2, incrseconda)

    incl03 = CM(lp0, lp3, inclfirst)
    incr03 = CM(rp0, rp3, incrfirstb)

    incl13 = CM(lp1, lp3, inclsecond)
    incr13 = CM(rp1, rp3, incrsecondb)
    
    incl14 = CM(lp1, lp4, inclfirst)
    incr14 = CM(rp1, rp4, incrfirstb)

    incl04 = CM(lp0, lp4, inclsecond)
    incr04 = CM(rp0, rp4, incrsecondb)

    incl15a = CM(lp1, lp5, inclfirst)
    incr15a = CM(rp1, rp5, incrfirstb)

    incl15b = CM(lp1, lp5, inclsecond)
    incr15b = CM(rp1, rp5, incrsecondb)

    T = GT(C, C)

    g0 = T.add_rule(lp0, rp0)
    g1 = T.add_rule(lp1, rp1)
    g2 = T.add_rule(lp2, rp2)
    g3 = T.add_rule(lp3, rp3)
    g4 = T.add_rule(lp4, rp4)
    g5 = T.add_rule(lp5, rp5)

    inc02a = T.add_inclusion(g0, g2, incl02a, incr02a)
    inc02b = T.add_inclusion(g0, g2, incl02b, incr02b)
    inc03 = T.add_inclusion(g0, g3, incl03, incr03)
    inc13 = T.add_inclusion(g1, g3, incl13, incr13)
    inc14 = T.add_inclusion(g1, g4, incl14, incr14)
    inc04 = T.add_inclusion(g0, g4, incl04, incr04)
    inc15a = T.add_inclusion(g1, g5, incl15a, incr15a)
    inc15b = T.add_inclusion(g1, g5, incl15b, incr15b)

    g = Graph.TO()()
    n1 = g.add_node()
    n2 = g.add_node()
    n3 = g.add_node()
    e12 = g.add_edge(n1,n2)
    e23 = g.add_edge(n2,n3)
    e31 = g.add_edge(n3,n1)
    p = {n1: 1, n2: 1, n3 : 0, e12 : 0, e23 : 0, e31 : 0}
    gp = CO(g, p)

    import matplotlib.pyplot as plt
    import networkx as nx

    plt.subplot(121)
    options = {
        'node_color': 'black',
        'node_size': 10,
        'width': 1,
    }
    nx.draw_kamada_kawai(g.g, **options)
    plt.show()
    for i in range(3):
        gp_ = T.apply(gp)
        print(gp_)
        g = tuple(gp_)[0].object
        nx.draw_kamada_kawai(g.OC.g, **options)
        plt.show()
        gp = g

test()