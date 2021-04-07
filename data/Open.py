import random
from .DataStructure import DataStructure
import random
import sys

seed = random.randrange(sys.maxsize) # = 862933594082592502 #
# print(" SEEEEEEEEED ", seed)
random.seed(seed)

class Open:

    @staticmethod
    def get(C):
        def object_init(self, LO, i = None):
            self.LO = LO
            self.i = i

        def object_repr(self):
            return "OO < " + str(self.LO) + " c: " + str(self.i) + " >"

        def object_eq(self, other):
            if not isinstance(other, ObjectClass):
                return False
            return self.LO == other.LO

        def object_hash(self):
            r = len(self.LO)
            for v in self.LO:
                r ^= 31 * hash(v)
            return r

        def object_eval(self, incsl, incsr): # efficacity vs intersection method ??
            r = [ ]
            for i in range(0, len(self.LO)):
                keep = True
                for j in range(0, len(incsl)):
                    incl = incsl[j]
                    incr = incsr[j]
                    assert incl.cod.i is not None
                    if incl.projL[incl.cod.i] != incr.projL[i]:
                        keep = False
                if keep:
                    r.append(i)
            if len(r) == 0:
                raise "CORRELATIONS ???"
            rand = random.randrange(len(r))
            return ObjectClass(self.LO, r[rand])

        ObjectClass = type("O" + C.__name__ + "O", (), {
            '__init__'     : object_init,
            '__repr__'     : object_repr,
            '__hash__'     : object_hash,
            '__eq__'       : object_eq,
            'eval'         : object_eval,
        })

        def morphism_init(self, s, t, projL, ev):
            self.s = s
            self.t = t
            self.projL = projL
            self.ev = ev
            hash(self)

        def morphism_compose(self, h):
            # TODO 
            c_projL = []
            c_ev = []
            for i in range(0, len(h.projL)):
                c_projL.append(self.projL[h.projL[i]])
                comp_e = self.ev[h.projL[i]].compose(h.ev[i])
                c_ev.append(comp_e)
                assert comp_e.dom == self.s.LO[self.projL[h.projL[i]]]
            return MorphismClass(self.s, h.t, c_projL, c_ev)

        def morphism_eq(self, other):
            if not isinstance(other, MorphismClass):
                return False
            return self.projL == other.projL and self.ev == other.ev and self.s == other.s and self.t == other.t

        def morphism_hash(self):
            r = hash(self.s) ^ hash(self.t)
            for i in self.projL:
                r ^= 31 * hash(i)
            for i in self.ev:
                r ^= 31 * hash(i)
            return r
        
        def morphism_dom(self):
            return self.s

        def morphism_cod(self):
            return self.t

        def morphism_repr(self):
            return "OM " + repr(self.s) + " -> " + repr(self.t) + " : (" + str(self.projL) + ", " + str(self.ev) + " )"

        MorphismClass = type("O" + C.__name__ + "M", (), {
            '__init__'  : morphism_init,
            'compose'   : morphism_compose,
            '__eq__'    : morphism_eq,
            '__hash__'  : morphism_hash,
            'dom'       : property(morphism_dom),
            'cod'       : property(morphism_cod),
            '__repr__'  : morphism_repr,
#            'eval'      : morphism_eval
        })

        def Category_TO():
            return ObjectClass

        def Category_TM():
            return MorphismClass

        def Category_pattern_match(p, s):
            raise "Not implemented"

        def Category_multi_merge(m1s, m2s):
            old = m1s[0].cod
            new = m2s[0].cod
            m1sc = []
            m2sc = []

            eold = old.eval([], [])
            m1sp = []
            for i in range(len(m1s)):
                m1sc.append(m1s[i].ev[eold.i])
                # information not stored in m1s because not merge has happened : 
                m1sp.append(MorphismClass(m1s[i].s, eold, m1s[i].projL, m1s[i].ev)) 
                # m1s[i].t = eold # this should not work, it modifies rule morphisms right ?
                # m1s[i].val = "aaaah"

            enew = new.eval(m1sp, m2s)
            for i in range(len(m2s)):
                m2sc.append(m2s[i].ev[enew.i])

            r, m_old, m_new = C.multi_merge(m1sc, m2sc)
            ro = ObjectClass([r], 0)
            return ro, MorphismClass(old, ro, [eold.i], [m_old]), MorphismClass(enew, ro, [enew.i], [m_new])

        def Category_multi_merge_2_in_1(m1s, m2s):
            old = m1s[0].cod
            new = m2s[0].cod
            m1sc = []
            m2sc = []

            for i in range(len(m1s)):
                m1sc.append(m1s[i].ev[old.i])

            enew = new.eval(m1s, m2s)
            for i in range(len(m2s)):
                m2sc.append(m2s[i].ev[enew.i])

            r, m_new = C.multi_merge_2_in_1(m1sc, m2sc)
            ro = ObjectClass([r], 0)
            return ro, MorphismClass(enew, ro, [enew.i], [m_new])

        CategoryClass = type("O" + C.__name__, (DataStructure,), {
            'TO'                  : Category_TO,
            'TM'                  : Category_TM,
            'pattern_match'       : Category_pattern_match,
            'multi_merge'         : Category_multi_merge,
            'multi_merge_2_in_1'  : Category_multi_merge_2_in_1,
        })

        return ObjectClass, MorphismClass, CategoryClass
