from .DataStructure import DataStructure

class Open:

    @staticmethod
    def get(C):
        import random
        def object_init(self, LO):
            self.LO = LO

        def object_repr(self):
            return "OO < " + str(self.LO) + " >"

        def object_eq(self, other):
            if not isinstance(other, ObjectClass):
                return False
            return self.LO == other.LO

        def object_hash(self):
            r = len(self.LO)
            for v in self.LO:
                r ^= 31 * hash(v)
            return r
        
        def object_eval(self, underincs): # efficacity vs intersection method ??
            r = self.LO.copy()
            for i in range(0, len(r)):
                ri = r[i]
                for ins_inc in underincs:
                    if ins_inc.s.old_subresult != ins_inc.rhs.dom.LO[ins_inc.rhs.projL[i]]:
                        ri = None
                r[i] = ri
            fr = list(filter(lambda x : (x != None), r))
            if len(fr) == 0:
                fr = self.LO
            rand = random.randrange(len(fr))
            return fr[rand]

        ObjectClass = type("O" + C.__name__ + "O", (), {
            '__init__'     : object_init,
            '__repr__'     : object_repr,
            '__hash__'     : object_hash,
            '__eq__'       : object_eq,
            'eval'         : object_eval,
        })

        def morphism_init(self, s, t, projL, ev):
            assert isinstance(s, ObjectClass)
            assert isinstance(t, ObjectClass)
            # assert len(projL) == len(t.LO)
            # assert len(ev) == len(projL)
            self.s = s
            self.t = t
            self.projL = projL
            self.ev = ev
            hash(self)

        def morphism_compose(self, h):
            c_projL = []
            c_ev = []
            for i in range(0, len(h.projL)):
                c_projL.append(self.projL[h.projL[i]])
                comp_e = self.ev[h.projL[i]].compose(h.ev[i])
                c_ev.append(comp_e)
                assert comp_e.dom() == self.s.LO[self.projL[h.projL[i]]]
            return MorphismClass(self.s, h.t, self.MC.compose(h.MC))

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
        
        def morphism_eval(self, over_rhs):
            i = -1
            for j in range(0, len(self.t.LO)): #TODO efficient reverse map LO : rhs -> id
                if self.t.LO[j] == over_rhs:
                    i = j
                    break
            return self.ev[i]

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
            'eval'      : morphism_eval
        })

        def Category_TO():
            return ObjectClass

        def Category_TM():
            return MorphismClass

        def Category_pattern_match(p, s):
            raise "Not implemented"

        def Category_multi_merge(m1s, m2s):
            return C.multi_merge(m1s, m2s)

        def Category_multi_merge_2_in_1(m1s, m2s):
            return C.multi_merge_2_in_1(m1s, m2s)

        CategoryClass = type("O" + C.__name__, (DataStructure,), {
            'TO'                  : Category_TO,
            'TM'                  : Category_TM,
            'pattern_match'       : Category_pattern_match,
            'multi_merge'         : Category_multi_merge,
            'multi_merge_2_in_1'  : Category_multi_merge_2_in_1,
        })

        return ObjectClass, MorphismClass, CategoryClass