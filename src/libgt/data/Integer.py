from .DataStructure import DataStructure

class IntegerM():

    def __init__(self, s, t):
        assert s <= t
        self.s = s
        self.t = t
        hash(self)

    def compose(self,h):
        assert self.t == h.s
        return IntegerM(self.s,h.t)

    def __eq__(self, other):
        if not isinstance(other,IntegerM):
            return False
        return self.s == other.s and self.t == other.t

    def __hash__(self):
        r = hash(self.s) ^ hash(self.t)
        return r

    def __repr__(self):
        return f"IntegerM({str(self.s)}, {str(self.t)})"

    @property
    def dom(self):
        return self.s

    @property
    def cod(self):
        return self.t

    def clean(self):
        pass


class Integer(DataStructure):

    @staticmethod
    def TO():
        return int

    @staticmethod
    def TM():
        return IntegerM

    @staticmethod
    def pattern_match(p, X):
        if isinstance(p, int):
            assert isinstance(X, int)
            if p <= X:
                yield IntegerM(p, X)
        elif isinstance(p, IntegerM):
            if p.cod <= X.cod:
                yield IntegerM(p.cod, X.cod)

    @staticmethod
    def multi_merge_2_in_1(m1s, m2s):
        n1 = m1s[0].cod
        n2 = m2s[0].cod
        n = max(n1, n2)
        return n, IntegerM(n,n2)

    @staticmethod
    def multi_merge(m1s, m2s):
        n1 = m1s[0].cod
        n2 = m2s[0].cod
        n = max(n1, n2)
        return n, IntegerM(n,n1), IntegerM(n,n2)

