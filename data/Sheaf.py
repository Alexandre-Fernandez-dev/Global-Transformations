from .DataStructure import DataStructure

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
            if isinstance(h, C.TM()):
                assert h.cod == self.OC
                ET = T['restriction'](h, self.ET)
                if h.dom == h.cod and ET == self.ET:
                    # assert False # used in gmap
                    return MorphismClass(self, self, h)
                else:
                    return MorphismClass(ObjectClass(h.dom, ET), self, h)
            elif isinstance(h, MorphismClass):
                return h

        ObjectClass = type(C.__name__ + "__" + T['name'] + "O", (), {
            '__init__'     : object_init,
            '__repr__'     : object_repr,
            '__hash__'     : object_hash,
            '__eq__'       : object_eq,
            'naked'        : object_naked,
            'restrict'     : object_restrict
        })

        def morphism_init(self, s, t, MC):
            # print("type")
            # print(ObjectClass.__name__)
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

        def Category_TO():
            return ObjectClass

        def Category_TM():
            return MorphismClass

        # def Category_pattern_match_fam(p, s): #TODO remove when everything fixed
        #     if isinstance(p, C.TM()):
        #         matches = C.pattern_match(p, s.naked())
        #         p = p.cod
        #         s = s.cod
        #     else:
        #         matches = C.pattern_match(p, s.naked())
        #     for m in matches:
        #         restr = T['restriction'](m, s.ET)
        #         yield MorphismClass(ObjectClass(p, restr), s, m)

        def Category_pattern_match(p, s):
            if isinstance(p, MorphismClass) or isinstance(p, ObjectClass): #TODO clean conditions
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
            elif isinstance(p, C.TM()) or isinstance(p, C.TO()): #TODO clean conditions
                # print("pattern_match_fam")
                if isinstance(p, C.TM()):
                    matches = C.pattern_match(p, s.naked())
                    p = p.cod
                    s = s.cod
                else:
                    matches = C.pattern_match(p, s.naked())
                for m in matches:
                    restr = T['restriction'](m, s.ET)
                    yield MorphismClass(ObjectClass(p, restr), s, m)

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
            'TO'                  : Category_TO,
            'TM'                  : Category_TM,
            # 'pattern_match_fam'   : Category_pattern_match_fam,
            'pattern_match'       : Category_pattern_match,
            'multi_merge'         : Category_multi_merge,
            'multi_merge_2_in_1'  : Category_multi_merge_2_in_1,
        })

        return ObjectClass, MorphismClass, CategoryClass