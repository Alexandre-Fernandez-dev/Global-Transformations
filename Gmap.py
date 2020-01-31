import math
from DataStructure import DataStructure
from itertools import chain
import time

class PremapO():
    def __init__(self, N):
        self.D = 0
        self.N = N
        self.Np1 = N + 1
        self.__alpha = [ ]
        self.__pattern = None

    def copy(self):
        p = PremapO(self.N)
        for d in self:
            p.add_dart()
        for d in self:
            for i in range(0,self.Np1):
                dd = self.__alpha[d][i]
                if (dd != None):
                    p.sew(i,d,dd)
        return p

    def add_dart(self):
        d = self.D
        self.__alpha.append([None] * self.Np1)
        self.D += 1
        return d

    def alpha(self,i,d):
        dd = self.__alpha[d][i]
        return d if dd == None else dd

    def sew(self,i,d,dd):
        self.__alpha[d][i] = dd
        self.__alpha[dd][i] = d

    def unsew(self,i,d):
        dd = self.__alpha[d][i]
        self.__alpha[d][i] = None
        self.__alpha[dd][i] = None

    def __iter__(self):
        yield from range(0,self.D)

    def __len__(self):
        return self.D

    def __repr__(self):
        return "{ premap:" + repr(self.__alpha) +  " }";

    def pattern(self):
        if self.__pattern == None:
            self.__pattern = []
            flag = [False]*self.D
            wl = [0]
            flag[0] = True
            while len(wl) > 0:
                d = wl.pop()
                for i in range(0,self.Np1):
                    dd = self.__alpha[d][i]
                    if dd == None:
                        continue
                    elif flag[dd]:
                        self.__pattern.append((True,d,i,dd))
                    else:
                        wl.insert(0, dd)
                        flag[dd] = True
                        self.__pattern.append((False,d,i,dd))
            print(self.__pattern)
        return self.__pattern

class PremapM:
    def __init__(self, s, t, l):
        assert s.N == t.N
        # for d in s:
        #     for i in range(0,s.Np1):
        #         aid = s.alpha(i,d)
        #         ld = l[d]
        #         assert l[aid] == ld or l[aid] == t.alpha(i,ld)
        self.s = s
        self.t = t
        self.l = l
        self.__pattern = None
        hash(self)

    def compose(self,h):
        assert self.t == h.s
        l = [ h.l[ld] for ld in self.l ]
        return PremapM(self.s,h.t,l)

    def __eq__(self, other):
        if not isinstance(other,PremapM):
            return False
        return self.s == other.s and self.t == other.t and self.l == other.l

    def __hash__(self):
        r = hash(self.s) ^ hash(self.t)
        for ld in self.l:
            r ^= 31 * ld
        return r

    def __repr__(self):
        return "[ premapMorph: " + repr(self.l) +  " ]"

    @property
    def dom(self):
        return self.s

    @property
    def cod(self):
        return self.t

    def pattern(self):
        return None

    def clean(self):
        self.l = self.l.copy()

    def pattern(self):
        if self.__pattern == None:
            self.__pattern = []
            flag = [False]*self.cod.D
            wl = []
            for ld in self.l:
                wl.append(ld)
                flag[ld] = True
            while len(wl) > 0:
                d = wl.pop()
                for i in range(0,self.cod.Np1):
                    dd = self.cod.alpha(i,d)
                    if dd == None:
                        continue
                    elif flag[dd]:
                        self.__pattern.append((True,d,i,dd))
                    else:
                        wl.insert(0, dd)
                        flag[dd] = True
                        self.__pattern.append((False,d,i,dd))
            print(self.__pattern)
        return self.__pattern

class Premap(DataStructure):

    @staticmethod
    def TO():
        return PremapO

    @staticmethod
    def TM():
        return PremapM

    class Ctx():
        def __init__(self,X,l):
            self.l = l
            self.X = X
            self.c = set()

        def curse(self,i):
            self.c.add(i)

        def is_cursed(self,i):
            return i in self.c

        def uncurse_all(self):
            self.c.clear()

    @staticmethod
    def pattern_match(p, X):
        if isinstance(p,PremapO):
            # WARNING: p is supposed connected
            if p.D == 0:
                yield PremapM(p,X,[])
            else:
                ctx = Premap.Ctx(X, p.D * [None])
                for ld in X:
                    ctx.l[0] = ld
                    ctx.curse(ld)
                    ok = True
                    for (b,d,i,dd) in p.pattern():
                        if b:
                            ld = ctx.l[d]
                            ldd = ctx.l[dd]
                            if ldd != X.alpha(i,ld):
                                ok = False
                                break
                        else:
                            ld = ctx.l[d]
                            ldd = X.alpha(i,ld)
                            if ctx.is_cursed(ldd):
                                ok = False
                                break
                            else:
                                ctx.l[dd] = ldd
                                ctx.curse(ldd)
                    ctx.uncurse_all()
                    if ok:
                        yield PremapM(p,X,ctx.l)
        else:
            # WARNING: dom and cod of p are supposed connected
            if p.dom.D == 0:
                return Premap.pattern_match(p.cod, X.cod)
            else:
                assert X.dom == p.dom
                ctx = Premap.Ctx(X.cod, p.cod.D * [None])
                for d, ld in enumerate(X.l):
                    ctx.curse(ld)
                    ctx.l[p.l[d]] = ld
                ok = True
                for (b,d,i,dd) in p.pattern():
                    if b:
                        ld = ctx.l[d]
                        ldd = ctx.l[dd]
                        if ldd != X.cod.alpha(i,ld):
                            ok = False
                            break
                    else:
                        ld = ctx.l[d]
                        ldd = X.cod.alpha(i,ld)
                        if ctx.is_cursed(ldd):
                            ok = False
                            break
                        else:
                            ctx.l[dd] = ldd
                            ctx.curse(ldd)
                ctx.uncurse_all()
                if ok:
                    yield PremapM(p.cod,X.cod,ctx.l)


    @staticmethod
    def multi_merge(m1s, m2s):
        t1 = m1s[0].t
        t2 = m2s[0].t
        r = t1.copy()
        lr1 = [ d for d in t1 ]
        lr2 = [None] * t2.D
        for m1, m2 in zip(m1s, m2s):
            assert m1.s == m2.s and m1.t == t1 and m2.t == t2
            s = m1.s
            for d in s:
                if lr2[m2.l[d]] != None:
                    if lr2[m2.l[d]] != m1.l[d]:
                        raise Exception("multi_merge collapse")
                lr2[m2.l[d]] = m1.l[d]
        for d in t2:
            if lr2[d] == None:
                dd = r.add_dart()
                lr2[d] = dd
            else:
                dd = lr2[d]
            for i in range(0,r.Np1):
                ad = t2.alpha(i,d)
                if ad == d:
                    continue
                elif lr2[ad] == None:
                    continue
                else:
                    r.sew(i,dd,lr2[ad])
        return r, PremapM(t1, r, lr1), PremapM(t2, r, lr2)


    @staticmethod
    def multi_merge_2_in_1(m1s, m2s):
        t1 = m1s[0].t
        t2 = m2s[0].t
        r = t1
        lr2 = [None] * t2.D
        for m1, m2 in zip(m1s, m2s):
            assert m1.s == m2.s and m1.t == t1 and m2.t == t2
            s = m1.s
            for d in s:
                if lr2[m2.l[d]] != None:
                    if lr2[m2.l[d]] != m1.l[d]:
                        raise Exception("multi_merge collapse")
                lr2[m2.l[d]] = m1.l[d]
        for d in t2:
            if lr2[d] == None:
                dd = r.add_dart()
                lr2[d] = dd
            else:
                dd = lr2[d]
            for i in range(0,r.Np1):
                ad = t2.alpha(i,d)
                if ad == d:
                    continue
                elif lr2[ad] == None:
                    continue
                else:
                    r.sew(i,dd,lr2[ad])
        return r, PremapM(t2, r, lr2)


def test_pmatching():
    p0 = PremapO(2)
    d0a = p0.add_dart()
    d0b = p0.add_dart()
    p0.sew(0,d0a,d0b)

    p1 = PremapO(2)
    d1a = p1.add_dart()
    d1b = p1.add_dart()
    d1c = p1.add_dart()
    d1d = p1.add_dart()
    d1e = p1.add_dart()
    d1f = p1.add_dart()
    p1.sew(0,d1a,d1b)
    p1.sew(1,d1b,d1c)
    p1.sew(0,d1c,d1d)
    p1.sew(1,d1d,d1e)
    p1.sew(0,d1e,d1f)
    p1.sew(1,d1f,d1a)

    p2 = PremapO(2)
    d2a = p2.add_dart()
    d2b = p2.add_dart()
    d2c = p2.add_dart()
    d2d = p2.add_dart()
    p2.sew(0,d2a,d2b)
    p2.sew(0,d2c,d2d)
    p2.sew(2,d2a,d2c)
    p2.sew(2,d2b,d2d)

    print(p0)
    print(p1)
    print(p2)

    idp0 = PremapM(p0,p0,[ d for d in p0 ])
    idp1 = PremapM(p1,p1,[ d for d in p1 ])
    idp2 = PremapM(p2,p2,[ d for d in p2 ])

    for m in Premap.pattern_match(p0,p1):
        print(m)
        for mm in Premap.pattern_match(m,m):
            print('  * ', mm)

    h1 = PremapM(p0,p1,[0,1])
    h2 = PremapM(p0,p2,[0,1])

    p2 = Premap.multi_merge([h1],[h2])

    print(p2)


if __name__ == "__main__":
    # test_merge()
    # test_pmatching()
    # test_pmatching2()
    test_pmatching()
