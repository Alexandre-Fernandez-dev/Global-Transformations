from .DataStructure import DataStructure

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
        return "NkSO( " + str(self.i) + " )"

class SequenceO:
    def __init__(self, s):
        self.s = s
        self.partial = None # memoized partials matches

    def naked(self):
        return NkSeqO(len(self.s))

    def restrict(self, h):
        if isinstance(h, NkSeqM):
            assert h.cod.i == len(self)
            if h.dom == h.cod:
                return SequenceM(self, self, h.i)
            return SequenceM(SequenceO(self.s[h.i:h.i+h.dom.i]), self, h.i)
        if isinstance(h, SequenceM):
            return h
        raise Exception("Cannot restrict")

    # new
    def __eq__(self, other):
        if not isinstance(other, SequenceO):
            return False
        return self.s == other.s

    # new
    def __hash__(self):
        r = len(self.s)
        for i in self.s:
            r ^= 31 * hash(i)
        return r

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
        # print("s == s", self.s == other.s)
        # print("t == t", self.t == other.t)
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
        if P.partial is None:
            P.partial = self.partial(P.s)
        j = 0

        for i in range(len(T.s)):
            while j > 0 and T.s[i] != P.s[j]:
                j = P.partial[j - 1]
            if T.s[i] == P.s[j]:
                j += 1
            if j == len(P.s):
                yield i - (j - 1)
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
    def pattern_match(p, X):
        # print(">>>>", type(p))
        # print(isinstance(p, NkSeqO))
        # print(isinstance(p, NkSeqM))
        # if isinstance(p, NkSeqM) or isinstance(p, NkSeqO):
        #     print("IF YIELD FAM")
        if isinstance(p, NkSeqO):
            assert isinstance(X, SequenceO)
            for i in range(0, len(X.s)-p.i+1):
                yield SequenceM(SequenceO(X.s[i:i+p.i]), X, i)
        elif isinstance(p, NkSeqM):
            cod = p.cod
            i = p.i
            start1 = X.i - i
            end2 = start1 + cod.i
            if start1 < 0 or end2 > len(X.cod.s):
                return
            yield SequenceM(SequenceO(X.cod.s[start1:end2]), X.cod, start1)
        elif isinstance(p, SequenceO):
            if p.s == []:
                for i in range(0, len(X.s) + 1):
                    yield SequenceM(p, X, i)
            else:
                for i in k.search(X, p):
                    yield SequenceM(p, X, i)
        elif isinstance(p, SequenceM):
            # print(type(p))
            start1 = X.i - p.i
            end1 = X.i
            start2 = start1 + len(p.dom.s) + p.i
            end2 = start1 + len(p.cod.s)
            if start1 < 0 or end2 > len(X.cod.s):
                return
            for i in range(start1, end1):
                if X.cod.s[i] != p.cod.s[i - start1]:
                    return
            for i in range(start2, end2):
                if X.cod.s[i] != p.cod.s[i - start1]:
                    return
            yield SequenceM(p.cod, X.cod, start1)

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
            mo1, mo2 = (mo2, mo1)
        for i in range(mo1.i + len(s), mo1.i + len(mo2.t) - mo2.i):
            if mo1.t.s[i] != mo2.t.s[i - (mo1.i - mo2.i)]:
                # print('fail2')
                return None
            l.append(mo1.t.s[i])
        for i in range(mo1.i + len(mo2.t) - mo2.i, len(mo1.t)):
            l.append(mo1.t.s[i])
        res = SequenceO(l)
        return res, SequenceM(m1.t, res, max(m1.i, m2.i) - m1.i), SequenceM(m2.t, res, max(m1.i, m2.i) - m2.i)
