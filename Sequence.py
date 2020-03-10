from DataStructure import DataStructure

class NkSeqO:
    def __init__(self, i):
        self.i = i

    def __eq__(self, other):
        if not isinstance(other, NkSeqO):
            return False
        return self.i == other.i

    def __hash__(self):
        return hash(self.i)

    def __repr__(self):
        return "NkSO( " + str(self.i) +" )"

class SequenceO:
    def __init__(self, s):
        self.s = s
        self.partial = None # memoized partials matches

    def naked(self):
        return NkSeqO(len(self.s))

    def restrict(self, h):
        assert h.cod.i == len(self)
        if h.dom == h.cod:
            return SequenceM(self, self, h.i)
        else:
            return SequenceM(SequenceO(self.s[h.i:h.i+h.dom.i]), self, h.i)

    # # new
    # def __eq__(self, other):
    #     if not isinstance(other, SequenceO):
    #         return False
    #     return self.s == other.s
    #
    # # new
    # def __hash__(self):
    #     r = len(self.s)
    #     for i in self.s:
    #         r ^= 31 * hash(i)
    #     return r

    def __len__(self):
        return len(self.s)

    def __repr__(self):
        return str(len(self.s)) + " " + repr(self.s)

class NkSeqM:
    def __init__(self, s, t, i):
        self.s = s
        self.t = t
        self.i = i

    def __eq__(self, other):
        if not isinstance(other, NkSeqM):
            return False
        return self.s == other.s and self.t == other.t and self.i == other.i

    def __hash__(self):
        r = hash(self.s)
        r ^= 31 * hash(self.t)
        r ^= 31 * hash(self.i)
        return r

    def compose(self, h):
        assert self.t == h.s
        return NkSeqM(self.s, h.t, self.i + h.i)

    @property
    def dom(self):
        return self.s

    @property
    def cod(self):
        return self.t

    def __repr__(self):
        return "NkSM( " + str(self.s) + ", " + str(self.t) + ", " + str(self.i) +" )"

class SequenceM:
    def __init__(self, s, t, i):
        self.s = s
        self.t = t
        self.i = i
        self.__pattern = None
        hash(self)

    def naked(self):
        return NkSeqM(self.s.naked(), self.t.naked(), self.i)

    def compose(self, h):
        assert self.t == h.s
        return SequenceM(self.s, h.t, self.i + h.i)

    def __eq__(self, other):
        if not isinstance(other, SequenceM):
            return False
        return self.s == other.s and self.t == other.t and self.i == other.i

    def __hash__(self):
        r = hash(self.s) ^ hash(self.t)
        r ^= 31 * self.i
        return r

    def apply(self, e):
        return self.i + e

    @property
    def dom(self):
        return self.s

    @property
    def cod(self):
        return self.t

    def clean(self):
        pass

    def __repr__(self):
        return repr(self.s) + " -> " + repr(self.t) + " : " + str(self.i)

class KMP:
    def partial(self, pattern):
            """ Calculate partial match table: String -> [Int]"""
            ret = [0]

            for i in range(1, len(pattern)):
                j = ret[i - 1]
                while j > 0 and pattern[j] != pattern[i]:
                    j = ret[j - 1]
                ret.append(j + 1 if pattern[j] == pattern[i] else j)
            return ret

    def search(self, T, P):
        """
        KMP search main algorithm: String -> String -> [Int]
        Return all the matching position of pattern string P in T
        """
        if P.partial == None:
            P.partial = self.partial(P.s)
        j = 0

        for i in range(len(T.s)):
            while j > 0 and T.s[i] != P.s[j]:
                j = P.partial[j - 1]
            if T.s[i] == P.s[j]: j += 1
            if j == len(P.s):
                yield (i - (j - 1))
                j = P.partial[j - 1]

k = KMP()

class Sequence(DataStructure):

    @staticmethod
    def TO():
        return SequenceO

    @staticmethod
    def TM():
        return SequenceM

    @staticmethod
    def pattern_match_fam(p_fam, s):
        if isinstance(p_fam, NkSeqO):
            assert isinstance(s, SequenceO)
            for i in range(0, len(s.s)-p_fam.i+1):
                yield SequenceM(SequenceO(s.s[i:i+p_fam.i]), s, i)
        else:
            cod = p_fam.cod
            i = p_fam.i
            start1 = s.i - i
            end2 = start1 + cod.i
            if start1 < 0 or end2 > len(s.cod.s):
                return
            yield SequenceM(SequenceO(s.cod.s[start1:end2]), s.cod, start1)

    @staticmethod
    def pattern_match(p, s):
        if isinstance(p, SequenceO):
            if(p.s == []):
                for i in range(0, len(s.s) + 1):
                    yield SequenceM(p, s, i)
            else:
                for i in k.search(s, p):
                    yield SequenceM(p, s, i)
        else:
            start1 = s.i - p.i
            end1 = s.i
            start2 = start1 + len(p.dom.s) + p.i
            end2 = start1 + len(p.cod.s)
            if start1 < 0 or end2 > len(s.cod.s):
               return
            for i in range(start1, end1):
                if s.cod.s[i] != p.cod.s[i - start1]:
                    return
            for i in range(start2, end2):
                if s.cod.s[i] != p.cod.s[i - start1]:
                    return

            yield SequenceM(p.cod, s.cod, start1)

    @staticmethod
    def multi_merge_2_in_1(m1s, m2s):
        assert len(m1s) == len(m2s)
        for i in range(0, len(m1s) - 1):
            assert m1s[i+1].i - m1s[i].i == m2s[i+1].i - m2s[i]
        return Sequence.merge_2_in_1(m1s[0], m2s[0])

    @staticmethod
    def merge_2_in_1(m1, m2):
        if m1.s != m2.s:
                raise Exception("Not same source")
        assert m2.i <= m1.i
        if len(m1.t) - m1.i < len(m2.t) - m2.i:
            for i in range(m1.i - m2.i, len(m1.t)):
                if m1.t.s[i] != m2.t.s[i - (m1.i - m2.i)]:
                    return None
            for i in range(len(m1.t) - (m1.i - m2.i), len(m2.t)):
                m1.t.s.append(m2.t.s[i])
        else:
            for i in range(m1.i - m2.i, len(m2.t) + (m1.i - m2.i)):
                if m1.t.s[i] != m2.t.s[i - (m1.i - m2.i)]:
                    return None
                else:
                    for i in range(len(m2.t) - (m1.i - m2.i), len(m2.t)):
                        if m1.t.s[i] != m2.t.s[i - (m1.i - m2.i)]:
                            return None
        return m1.t, SequenceM(m2.t, m1.t, m1.i - m2.i)

    @staticmethod
    def multi_merge(m1s, m2s):
        assert len(m1s) == len(m2s)
        # print(m1s)
        # print(m2s)
        # very weird multi merge need check gt :
        # ms1 : [1 [5.0] -> 3 [0, 2.5, 5.0] : 2, 0 [] -> 3 [0, 2.5, 5.0] : 3]
        # ms2 : [1 [5.0] -> 3 [5.0, 7.5, 10] : 0, 0 [] -> 3 [5.0, 7.5, 10] : 2]
        for i in range(0, len(m1s) - 1):
            assert m1s[i+1].i - m1s[i].i == m2s[i+1].i - m2s[i].i
        return Sequence.merge(m1s[0], m2s[0])

    @staticmethod
    def merge(m1, m2):
        if m1.s != m2.s:
            raise Exception("Not same source")
        s = m1.s
        if m1.i < m2.i:
            mo1 = m2
            mo2 = m1
        else:
            mo1 = m1
            mo2 = m2
        l = []
        for i in range(0, mo1.i - mo2.i):
            l.append(mo1.t.s[i])
        for i in range(mo1.i - mo2.i, mo1.i):
            if mo1.t.s[i] != mo2.t.s[i - (mo1.i - mo2.i)]:
                # print('fail1')
                return None
            l.append(mo1.t.s[i])
        for i in range(mo1.i, mo1.i + len(s)):
            l.append(mo1.t.s[i])
        if len(mo1.t) - mo1.i < len(mo2.t) - mo2.i:
            temp = mo1
            mo1 = mo2
            mo2 = temp
        for i in range(mo1.i + len(s), mo1.i + len(mo2.t) - mo2.i):
            if mo1.t.s[i] != mo2.t.s[i - (mo1.i - mo2.i)]:
                # print('fail2')
                return None
            l.append(mo1.t.s[i])
        for i in range(mo1.i + len(mo2.t) - mo2.i, len(mo1.t)):
            l.append(mo1.t.s[i])
        res = SequenceO(l)
        return res, SequenceM(m1.t, res, max(m1.i, m2.i) - m1.i), SequenceM(m2.t, res, max(m1.i, m2.i) - m2.i)


def test():
    test = ['b', 'o', 'n', 'j', 'o', 'n', 'r']
    pat =  ['o', 'n']
    for i in Sequence.pattern_match(SequenceO(pat), SequenceO(test)):
        print(i.i)
        r1 = i

    patdest = ['n', 'j', 'o', 'n', 'r']
    for i in Sequence.pattern_match(SequenceO(pat), SequenceO(patdest)):
        print(i.i)
        r2 = i

    for i in Sequence.pattern_match(r2, r1):
        print(i.i)

    merge1 = ['e', 'y', 'l', 'e'] #, 'a', 'l', 'e', 'x']
    merge2 = ['h', 'e', 'y', 'l', 'e', 'a']
    mergeon = ['l', 'e']
    m1 = SequenceM(SequenceO(mergeon), SequenceO(merge1), 2)
    m2 = SequenceM(SequenceO(mergeon), SequenceO(merge2), 3)

    # t = Sequence.merge(m2, m1)
    # print(t)

    # print(merge1)
    # print(merge2)
    # print(mergeon)
    # t = Sequence.merge_2_in_1(m2, m1)
    # print(t)

    # for i in Sequence.pattern_match_fam((2, 4, 2), m2):
    #     print(i)

    # for i in Sequence.pattern_match_fam(0, SequenceO(test)):
    #     print(i)

    import PFunctor
    import GT

    pfm = PFunctor.FamPFunctor.Maker(Sequence, Sequence)

    l0 = NkSeqO(0)
    r0 = lambda x : x

    g0 = pfm.add_fam_rule(l0, r0)

    l1 = NkSeqO(1)
    r1 = lambda x : SequenceO(['a', 'b']) if x.s == ['a'] else SequenceO(['a'])

    g1 = pfm.add_fam_rule(l1, r1)

    def rhs0(lps, lpo, rs, ro):
        return SequenceM(rs, ro, 0)

    def rhs1(lps, lpo, rs, ro):
        if ro.s == ['a', 'b']:
            return SequenceM(rs, ro, 2)
        elif ro.s == ['a']:
            return SequenceM(rs, ro, 1)

    _, _, inc1 = pfm.add_fam_inclusion(g0, g1, NkSeqM(NkSeqO(0), NkSeqO(1), 0), rhs0)
    # print(">>> inc1 lhs", inc1.lhs)
    pfm.add_fam_inclusion(g0, g1, NkSeqM(NkSeqO(0), NkSeqO(1), 1), rhs1)

    pf = pfm.get()

    T = GT.GT(pf)

    g = SequenceO(['a'])
    # print(g)
    for i in range(0, 10):
        gr = T.extend(g)
        assert len(gr) == 1
        g = list(gr)[0].object
        print(g)

    pfm = PFunctor.FamPFunctor.Maker(Sequence, Sequence)

    l1 = NkSeqO(1)
    r1 = lambda x : x

    g1 = pfm.add_fam_rule(l1, r1)

    l2 = NkSeqO(2)
    r2 = lambda x : SequenceO([x.s[0], (x.s[0] + x.s[1])/2, x.s[1]])

    g2 = pfm.add_fam_rule(l2, r2)

    def rhs120(lps, lpo, rs, ro):
        return SequenceM(rs, ro, 0)

    def rhs122(lps, lpo, rs, ro):
        return SequenceM(rs, ro, 2)

    pfm.add_fam_inclusion(g1, g2, NkSeqM(NkSeqO(1), NkSeqO(2), 0), rhs120)
    pfm.add_fam_inclusion(g1, g2, NkSeqM(NkSeqO(1), NkSeqO(2), 1), rhs122)

    pf = pfm.get()

    T = GT.GT(pf)

    g = SequenceO([0, 5, 0, 5])
    print(g)
    for i in range(0, 3):
        gr = T.extend(g)
        assert len(gr) == 1
        g = list(gr)[0].object
        print(g)



from random import random

def test2():
    from DataStructure import Lazy
    LSequence = Lazy(Sequence)
    def s1exp():
        return (SequenceO(['a','a']), []) if random() <= 0.5  else (SequenceO(['a']), [])
    s1 = LSequence.TO()(s1exp)

    def s2exp():
        return (SequenceO(['b','b']), []) if random() <= 0.5  else (SequenceO(['b']), [])
    s2 = LSequence.TO()(s2exp)

    def s3exp(s1,s2):
        ret = SequenceO(s1.s + s2.s)
        return (ret, [ SequenceM(s1,ret,0) , SequenceM(s2,ret,len(s1.s)) ])
    s3 = LSequence.TO()(s3exp)
    h13 = s3.setSubobject(0,s1)
    h23 = s3.setSubobject(1,s2)

    def s4exp(s3):
        ret = SequenceO(['c'] + s3.s + ['c'])
        return (ret, [ SequenceM(s3,ret,1) ])
    s4 = LSequence.TO()(s4exp)
    h34 = s4.setSubobject(0,s3)

    h = h13.compose(h34)

    print(h.force())


def test3():
    from PFunctor import ExpPFunctor
    from GT import GT
    from DataStructure import Lazy
    LSequence = Lazy(Sequence)

    epf = ExpPFunctor.Maker(Sequence, LSequence)

    l_a = SequenceO(['a'])
    def er_a():
        return (SequenceO(['a','a']), []) if random() <= 0.5  else (SequenceO(['a']), [])
    g_a = epf.add_exp_rule(l_a, er_a)

    l_aa = SequenceO(['a','a'])
    def er_aa(s1,s2):
        ret = SequenceO(s1.s + s2.s)
        return (ret, [ SequenceM(s1,ret,0) , SequenceM(s2,ret,len(s1.s)) ])
    g_aa = epf.add_exp_rule(l_aa, er_aa)

    l_a_aa_0 = SequenceM(l_a,l_aa,0)
    ir_a_aa_0 = 0
    g_a_aa_0 = epf.add_exp_inclusion(g_a, g_aa, l_a_aa_0, ir_a_aa_0)

    l_a_aa_1 = SequenceM(l_a,l_aa,1)
    ir_a_aa_1 = 1
    g_a_aa_1 = epf.add_exp_inclusion(g_a, g_aa, l_a_aa_1, ir_a_aa_1)

    epf = epf.get()

    T = GT(epf)

    sz = {}
    for i in range(0,100):
        s = len(tuple(T.extend(SequenceO(['a','a','a'])))[0].object)
        sz[s] = sz.setdefault(s,0) + 1
    print({s: 8*n/100 for (s,n) in sz.items() })
    print((tuple(T.extend(SequenceO(['a','a','a'])))[0].object))

if __name__ == "__main__":
    test3()

#
# let g1 =
#   a => a if random() else aa
#
# let g2 = 
#   aa => i * j
#
# and i: g1 -> g2 = 
#   (0: g1 -> g2) => (0: g1 -> g2)
#
# and j: g1 -> g2 = 
#   (1: a -> aa) => (len(i.dom): g1 -> g2)
# 
# 
# let g1 = a => b
# 
# and g2 = b => ab
# 
# and g3 = . => .
#
# and _: g3 -> g1 = 0 => 0
# 
# 
