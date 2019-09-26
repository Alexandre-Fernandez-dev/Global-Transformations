
#
# 1, 2, 1, 2, 3
#
# a, b, c, d, e, f, g, h, i, j
# 1, x, ?, ?, ?
#    ^
# 1, 2, x, ?, ?
#          ^
# 1, 2, 1, x, ?
#          ^
# 1, 2, 1, 2, x
#       ^
# 1, 2, 1, 2, 3
#               ^
#
# 1, 2, 1, 2, 1
#
# a, b, c, d, e, f, g, h, i, j
# 1, x, ?, ?, ?
#    ^
# 1, 2, x, ?, ?
#          ^
# 1, 2, 1, x, ?
#          ^
# 1, 2, 1, 2, x
#       ^
# 1, 2, 1, 2, 3
#               ^
#

class SequenceO:
    def __init__(self, s):
        self.s = s
        self.partial = None # memoized partials matches

    # def __eq__(self, other):
    #     return self.s == other.s
    #
    # def __hash__(self):
    #     r = len(self.s)
    #     for i in self.s:
    #         r ^= 31 * hash(i)
    #     return r
    #
    def __len__(self):
        return len(self.s)

    def __repr__(self):
        return str(len(self.s)) + " " + repr(self.s)

class SequenceM:
    def __init__(self, s, t, i):
        self.s = s
        self.t = t
        self.i = i
        self.__pattern = None
        hash(self)

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
                # ret.append(i - (j - 1))
                yield (i - (j - 1))
                j = P.partial[j - 1]

        return ret

k = KMP()

class Sequence:

    @staticmethod
    def pattern_match(p, s):
        # print("match", p, s)
        if isinstance(p, SequenceO):
            # l = []
            # for i in range(0, len(s.s)-len(p.s)):
            #     valid = True
            #     for j in range(0, len(p.s)):
            #         if s.s[i+j] != p.s[j]:
            #             valid = False
            #             break
            #     if valid:
            #         l.append(i)
            if(p.s == []):
                for i in range(0, len(s.s) + 1):
                    yield SequenceM(p, s, i)
            else:
                for i in k.search(s, p):
                    yield SequenceM(p, s, i)
        else:
            # print(p.dom.s, p.cod.s, p.i)
            # print(s.dom.s, s.cod.s, s.i)
            start1 = s.i - p.i
            end1 = s.i
            # print(start1, end1)
            start2 = start1 + len(p.dom.s) + p.i
            end2 = start1 + len(p.cod.s)
            # print(start2, end2)
            if start1 < 0 or end2 > len(s.cod.s):
               return
            for i in range(start1, end1):
                # print("i : ", i, "s.cod: ", s.cod, "p.cod: ", p.cod, "i - p.i", i - p.i)
                if s.cod.s[i] != p.cod.s[i - start1]:
                    return
            for i in range(start2, end2):
                # print("i : ", i)
                if s.cod.s[i] != p.cod.s[i - start1]:
                    return

            yield SequenceM(p.cod, s.cod, start1)

    @staticmethod
    def quotient(m1, m2):
        print("quotient", m1, m2)

    @staticmethod
    def merge_2_in_1(m1, m2):
        if m1.s != m2.s:
                raise Exception("Not same source")
        s = m1.s
        assert m2.i <= m1.i
        end = min(len(m1.t) - m1.i, len(m2.t) - m2.i)
        if len(m1.t) - m1.i < len(m2.t) - m2.i:
            for i in range(m1.i - m2.i, len(m1.t)):
                if m1.t.s[i] != m2.t.s[i - (m1.i - m2.i)]:
                    # print('fail1')
                    return None
            for i in range(len(m1.t) - (m1.i - m2.i), len(m2.t)):
                m1.t.s.append(m2.t.s[i])
        else:
            for i in range(m1.i - m2.i, len(m2.t) + (m1.i - m2.i)):
                if m1.t.s[i] != m2.t.s[i - (m1.i - m2.i)]:
                    # print('fail2')
                    return None
                else:
                    for i in range(len(m2.t) - (m1.i - m2.i), len(m2.t)):
                        if m1.t.s[i] != m2.t.s[i - (m1.i - m2.i)]:
                            # print('fail3')
                            return None
        return m1.t, SequenceM(m2.t, m1.t, m1.i - m2.i)


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

    t = Sequence.merge(m2, m1)
    print(t)

    print(merge1)
    print(merge2)
    print(mergeon)
    t = Sequence.merge_2_in_1(m2, m1)
    print(t)
