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
            r = [ ]
            print("CHOOSE ")
            for i in range(0, len(self.LO)):
                print("CHOICE ", i)
                keep = True
                for ins_inc in underincs:
                    # print(type(ins_inc.s.new_subresult))
                    # print(ins_inc)
                    ins_rhs = ins_inc.get_rhs()
                    if ins_inc.s.new_subresult is not None:
                        if isinstance(ins_inc.s.new_subresult, MorphismeInterne):
                            om, index = ins_inc.s.new_subresult
                            # print()
                            # print(om.projL[index])
                            # print(ins_rhs)
                            # print(ins_rhs.projL[i])
                            if om.projL[index] != ins_rhs.projL[i]:
                                keep = False
                                # print("False")
                        else:
                            assert isinstance(ins_inc.s.new_subresult, C.TM())
                        #if ins_inc.s.new_subresult != None:
                        # print(ins_inc.s.new_subresult.dom, ins_inc.rhs.dom.LO[ins_inc.rhs.projL[i]])
                            if ins_inc.s.new_subresult.dom != ins_rhs.dom.LO[ins_rhs.projL[i]]:
                                keep = False
                if keep:
                    r.append(i)
            print(r)
            if len(r) == 0:
                raise "CORRELATIONS ???"
            #     rand = random.randrange
            # else:
            rand = random.randrange(len(r))
            print(" CHOOSEN : ", rand, self.LO[r[rand]])
            return (self, r[rand])

        ObjectClass = type("O" + C.__name__ + "O", (), {
            '__init__'     : object_init,
            '__repr__'     : object_repr,
            '__hash__'     : object_hash,
            '__eq__'       : object_eq,
            'eval'         : object_eval,
        })

        def morphism_init(self, s, t, projL, ev):
            # assert len(projL) == len(t.LO)
            # assert len(ev) == len(projL)
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
                # comp_e.name = "(" + self.ev[h.projL[i]].name + " ; " + h.ev[i].name + ")"
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
        
        class MorphismeInterne:
            def __init__(self, m, i):
                self.m = m
                self.i = i
                self.t = (m, i)
            
            def __iter__(self):
                return self.t.__iter__()

            def compose(self, h):
                if isinstance(h, MorphismeInterne):
                    return MorphismeInterne(self.m.compose(h.m), h.i)
                    #self.m.ev[self.i].compose(h.m.ev[h.i])
                elif isinstance(h, C.TM()):
                    print("lol")
                    print(self.m.ev[self.i])
                    print(h)
                    return self.m.ev[self.i].compose(h)
                else:
                    print(type(h))
                    assert False
                # raise "ERREUR"

        def morphism_eval(self, over_rhs):
            print("morphism_eval")
            _, i = over_rhs
            return MorphismeInterne(self, i)

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
            print("MULTI MERGE")
            for i in m1s:
                print(i)
            print("...")
            for i in m2s:
                print(i)
            for i in range(len(m1s)):
                if isinstance(m1s[i], MorphismeInterne):
                    om, j = m1s[i]
                    m1s[i] = om.ev[j]
                else:
                    assert isinstance(m1s[i], C.TM())
            for i in range(len(m2s)):
                if isinstance(m2s[i], MorphismeInterne):
                    om, j = m2s[i]
                    m2s[i] = om.ev[j]
                else:
                    assert isinstance(m2s[i], C.TM())
            return C.multi_merge(m1s, m2s)

        def Category_multi_merge_2_in_1(m1s, m2s):
            for i in range(len(m1s)):
                if isinstance(m1s[i], MorphismeInterne):
                    om, j = m1s[i]
                    m1s[i] = om.ev[j]
                else:
                    assert isinstance(m1s[i], C.TM())
            for i in range(len(m2s)):
                if isinstance(m2s[i], MorphismeInterne):
                    om, j = m2s[i]
                    m2s[i] = om.ev[j]
                else:
                    assert isinstance(m2s[i], C.TM())
            return C.multi_merge_2_in_1(m1s, m2s)

        CategoryClass = type("O" + C.__name__, (DataStructure,), {
            'TO'                  : Category_TO,
            'TM'                  : Category_TM,
            'pattern_match'       : Category_pattern_match,
            'multi_merge'         : Category_multi_merge,
            'multi_merge_2_in_1'  : Category_multi_merge_2_in_1,
        })

        return ObjectClass, MorphismClass, CategoryClass
