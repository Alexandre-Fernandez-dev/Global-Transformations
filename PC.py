class P:

    @staticmethod
    def get(C):
        def object_init(self, OL):
            for o in OL:
                assert isinstance(o, C.TO())
            # TODO need check ET.dom == OC.elements ?
            self.OL = OL

        def object_repr(self):
            return "P__ < " + str(self.OL) + " >"

        def object_eq(self, other):
            if not isinstance(other, ObjectClass):
                return False
            return self.OL == other.OL

        def object_hash(self):
            r = 17
            for o in self.OL:
                r ^= 31 * hash(o)
            return r

        def object_restrict(self, h):
            if isinstance(h, MorphismClass):
                return h
            else:
                raise "Prout"

        ObjectClass = type("P__" + C.__name__ + "O", (), {
            '__init__'     : object_init,
            '__repr__'     : object_repr,
            '__hash__'     : object_hash,
            '__eq__'       : object_eq,
            'restrict'     : object_restrict
        })

        def morphism_init(self, s, t, ML):
            # print("type")
            # print(ObjectClass.__name__)
            assert isinstance(s, ObjectClass)
            assert isinstance(t, ObjectClass)
            # CHECK if the inverse of ML (seen as a set function) is a morphism
            b = { o : False for o in t.OL }
            self.s_out = { }
            self.t_in = { }
            for m in ML:
                assert isinstance(m, C.TM())
                assert b[m.cod] == False # this check ensures it is functionnal (#should be removed for correlations)
                b[m.cod] = True
                self.s_out.setdefault(m.dom, []).append(m)
                self.t_in[m.cod] = m
            for o in t.OL:
                assert b[o] == True # this check ensures everything is mapped (every object in t has a (unique) justification
            self.s = s
            self.t = t
            self.ML = ML
            hash(self)

        def morphism_compose(self, h):
            ML = []
            for o in h.s.OL:
                for hm in h.s_out[o]:
                    ML.append(self.t_in[o].compose(hm))
            return MorphismClass(self.s, h.t, ML)

        def morphism_eq(self, other):
            if not isinstance(other, MorphismClass):
                return False
            return self.ML == other.ML and self.s == other.s and self.t == other.t

        def morphism_hash(self):
            r = 17
            for m in self.ML:
                r ^= 31 * hash(m)
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
            return "P__ " + repr(self.s) + " -> " + repr(self.t) + " : " + str(self.ML)

        MorphismClass = type("P__" + C.__name__ + "O", (), {
            '__init__'  : morphism_init,
            'compose'   : morphism_compose,
            '__eq__'    : morphism_eq,
            '__hash__'  : morphism_hash,
            'dom'       : property(morphism_dom),
            'cod'       : property(morphism_cod),
            'clean'     : morphism_clean,
            '__repr__'  : morphism_repr
        })
    
        def Category_TO():
            return ObjectClass

        def Category_TM():
            return MorphismClass

        def Category_pattern_match(p, s): # correlation free: inverse is a morphism of sets
            print("enter")
            def f(i, l):
                print("loop")
                if i == len(s.OL):
                    print("got ", l)
                    yield MorphismClass(p, s, l)
                else:
                    osi = s.OL[i]
                    for op in p.OL:
                        for m in C.pattern_match(op, osi):
                            print("match")
                            lp = l + [ m ]
                            yield from f(i+1, lp)
            yield from f(0, [])

        CategoryClass = type("P__" + C.__name__, (), {
            'TO'                  : Category_TO,
            'TM'                  : Category_TM,
            'pattern_match'       : Category_pattern_match,
        })

        return ObjectClass, MorphismClass, CategoryClass

def test():
    from Graph import Graph, GraphO, GraphM
    from Sheaf import Parametrisation

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

    PParGraphO, PParGraphM, PParGraph = P.get(ParGraph)

    r1a = GraphO()
    r1an0 = r1a.add_node()
    r1an1 = r1a.add_node()
    r1ae0 = r1a.add_edge(r1an0, r1an1)
    r1ae1 = r1a.add_edge(r1an1, r1an0)

    r1ap = ParGraphO(r1a, {r1an0 : 0, r1an1 : 0})

    r1b = GraphO()
    r1bn0 = r1b.add_node()
    r1bn1 = r1b.add_node()
    r1bn2 = r1b.add_node()
    r1be0 = r1b.add_edge(r1bn0, r1bn1)
    r1be1 = r1b.add_edge(r1bn1, r1bn0)
    r1be2 = r1b.add_edge(r1bn1, r1bn2)
    r1be3 = r1b.add_edge(r1bn2, r1bn1)

    r1bp = ParGraphO(r1b, {r1bn0 : 0, r1bn1 : 1, r1bn2 : 0})

    pr1 = PParGraphO([r1ap, r1bp])

    for m in PParGraph.pattern_match(pr1, pr1):
        # print(m)
        pass

    r2a = GraphO()
    nr2a_0 = r2a.add_node()
    nr2a_1 = r2a.add_node()
    nr2a_2 = r2a.add_node()
    er2a_0 = r2a.add_edge(nr2a_0, nr2a_1)
    er2a_1 = r2a.add_edge(nr2a_1, nr2a_0)
    er2a_2 = r2a.add_edge(nr2a_1, nr2a_2)
    er2a_3 = r2a.add_edge(nr2a_2, nr2a_1)
    er2a_4 = r2a.add_edge(nr2a_2, nr2a_0)
    er2a_5 = r2a.add_edge(nr2a_0, nr2a_2)
    
    r2ap = ParGraphO(r2a, { n : 0 for n in range(0, 3) })

    r2b = GraphO()
    nr2b = [ r2b.add_node() for _ in range(0, 4)]
    er2b = []
    for i in range(0, 4):
        er2b.append(r2b.add_edge(i, ( i+1 ) % 4))
        er2b.append(r2b.add_edge( (i+1) % 4, i))
    er2b.append(r2b.add_edge(nr2b[1], nr2b[3]))
    er2b.append(r2b.add_edge(nr2b[3], nr2b[1]))

    p = { n : 0 for n in nr2b }
    p[nr2b[3]] = 1

    r2bp = ParGraphO(r2b, p)

    r2b_rot1 = GraphO()
    r2b_rot1.g = r2b.g.copy()

    r2b_rot1p = ParGraphO(r2b_rot1, p)

    r2b_rot2 = GraphO()
    r2b_rot2.g = r2b.g.copy()

    r2b_rot2p = ParGraphO(r2b_rot2, p)

    print("------------")
    pr2 = PParGraphO([r2ap, r2bp, r2b_rot1p, r2b_rot2p])
    l = []
    for m in PParGraph.pattern_match(pr2, pr2):
        # print(m)
        l.append(m)
        pass
    print(len(l), len(set(l)))

test()