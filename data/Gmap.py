from .DataStructure import DataStructure

class PremapO():
    class icells:
        def __init__(self):
            self.normalMap = [ ]
            self.classes = set()

        def find(self, k):
            father = self.normalMap[k]
            if father == k:
                return k
            root = self.find(father)
            self.normalMap[k] = root
            return root

        def union(self, key1, key2):
            r1 = self.find(key1)
            r2 = self.find(key2)
            #print("r1, r2", r1, r2)
            if r1 < r2:
                self.normalMap[r2] = r1
                self.classes.remove(r2)
            elif r1 > r2:
                self.normalMap[r1] = r2
                self.classes.remove(r1)

        def __eq__(self, other):
            assert False
            return self.normalMap == other.normalMap and self.classes == other.classes

    def __init__(self, N):
        self.D = 0
        self.N = N
        self.Np1 = N + 1
        self.__cells = [ self.icells() for i in range(0, self.Np1) ]
        self.__alpha = [ ]
        self.__pattern = None

    def copy(self):
        p = PremapO(self.N)
        for d in self:
            p.add_dart()
        for d in self:
            for i in range(0,self.Np1):
                dd = self.__alpha[d][i]
                if dd is not None and p.__alpha[d][i] is None:
                    p.sew(i,d,dd)
        for d in p:
            for i in range(0, self.Np1):
                assert self.__cells[i].find(d) == p.__cells[i].find(d)
        return p

    def add_dart(self):
        d = self.D
        self.__alpha.append([None] * self.Np1)
        self.D += 1
        for i in range(0, self.Np1):
            self.__cells[i].normalMap.append(d)
            self.__cells[i].classes.add(d)
        return d

    def alpha(self,i,d):
        dd = self.__alpha[d][i]
        return d if dd is None else dd

    def sew(self,i,d,dd):
        # print(d, dd, self.__alpha[d][i], self.__alpha[dd][i])
        assert d != dd
        if self.__alpha[d][i] == dd and self.__alpha[dd][i] == d:
            return
        self.__alpha[d][i] = dd
        self.__alpha[dd][i] = d
        # if d == 6:
        #     print("d, dd", d, dd)

        for k in range(0, self.Np1):
            if k != i:
                # if d == 7 or dd == 7:
                #     print("sew", i)
                #     print("union", k, d, dd)
                self.__cells[k].union(d, dd)

    # def unsew(self,i,d):
    #     dd = self.__alpha[d][i]
    #     self.__alpha[d][i] = None
    #     self.__alpha[dd][i] = None

    def iter_icells(self, i):
        yield from self.__cells[i].classes

    def get_icell(self, i, d):
        #print(self.__cells[i].classes)
        return self.__cells[i].find(d)

    def __iter__(self):
        yield from range(0,self.D)

    def __len__(self):
        return self.D

    def __repr__(self):
        return "{ premap:" + repr(self.__alpha) +  " }"
    
    def restrict(self, h):
        return h.dom()

    def pattern(self):
        if self.__pattern is None:
            self.__pattern = []
            flag = [False]*self.D
            wl = [0]
            flag[0] = True
            while len(wl) > 0:
                d = wl.pop()
                for i in range(0,self.Np1):
                    dd = self.__alpha[d][i]
                    if dd is None:
                        continue
                    if flag[dd]:
                        self.__pattern.append((True,d,i,dd))
                    else:
                        wl.insert(0, dd)
                        flag[dd] = True
                        self.__pattern.append((False,d,i,dd))
            # print(self.__pattern)
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
        #print(self.t, h.s)
        assert self.t == h.s
        l = [ h.l[ld] for ld in self.l ]
        return PremapM(self.s,h.t,l)

    def apply(self, v):
        return self.l[v]

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

    # def pattern(self):
    #     return None

    def clean(self):
        self.l = self.l.copy()

    def pattern(self):
        if self.__pattern is None:
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
                    if dd == d:
                        continue
                    if flag[dd]:
                        self.__pattern.append((True,d,i,dd))
                    else:
                        wl.insert(0, dd)
                        flag[dd] = True
                        self.__pattern.append((False,d,i,dd))
            # print(self.__pattern)
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
        # print("pattern_match : ")
        if isinstance(p,PremapO):
            # print("match ", p)
            # print("in ", X)
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
                            ctx.l[dd] = ldd
                            ctx.curse(ldd)
                    ctx.uncurse_all()
                    if ok:
                        yield PremapM(p,X,ctx.l)
        else:
            # print("------------")
            # print("match ", p.dom, p, p.cod)
            # print("in ", X.dom, X, X.cod)
            # WARNING: dom and cod of p are supposed connected
            if p.dom.D == 0:
                return Premap.pattern_match(p.cod, X.cod)
            assert X.dom == p.dom
            ctx = Premap.Ctx(X.cod, p.cod.D * [None])
            for d, ld in enumerate(X.l):
                ctx.curse(ld)
                ctx.l[p.l[d]] = ld
            ok = True
            # print("pattern : ")
            # print(p.pattern())
            for (b,d,i,dd) in p.pattern():
                # print((b,d,i,dd))
                if b:
                    ld = ctx.l[d]
                    ldd = ctx.l[dd]
                    # print(ldd)
                    # print(X.cod.alpha(i,ld))
                    if ldd != X.cod.alpha(i,ld):
                        # print("failedif")
                        ok = False
                        break
                else:
                    ld = ctx.l[d]
                    ldd = X.cod.alpha(i,ld)
                    if ctx.is_cursed(ldd):
                        # print("failedelse")
                        ok = False
                        break
                    ctx.l[dd] = ldd
                    ctx.curse(ldd)
            ctx.uncurse_all()
            # print(ok)
            # print("------------")
            if ok:
                yield PremapM(p.cod,X.cod,ctx.l)


    @staticmethod
    def multi_merge(m1s, m2s):
        t1 = m1s[0].t
        t2 = m2s[0].t
        # print("multi :")
        # print("t1", t1)
        # print("t2", t2)
        # for ll1, ll2 in zip(m1s, m2s):
        #     print('m1', ll1)
        #     print('m1s', ll1.s)
        #     print('m2', ll2)
        #     print('m2s', ll2.s)
        r = t1.copy()
        lr1 = [ d for d in t1 ]
        lr2 = [None] * t2.D
        for m1, m2 in zip(m1s, m2s):
            assert m1.s == m2.s and m1.t == t1 and m2.t == t2
            s = m1.s
            for d in s:
                # if lr2[m2.l[d]] != None:
                #     if lr2[m2.l[d]] != m1.l[d]:
                #         raise Exception("multi_merge collapse")
                # else:
                wl = [ (m1.l[d], m2.l[d]) ]
                while len(wl) > 0:
                    (d1,d2) = wl.pop()
                    if lr2[d2] is None:
                        lr2[d2] = d1
                        for i in range(0, s.Np1):
                            dd1 = t1.alpha(i,d1)
                            dd2 = t2.alpha(i,d2)
                            if dd1 != d1 and dd2 != d2:
                                wl.append((dd1,dd2))
                    elif lr2[d2] != d1:
                        raise Exception("multi_merge collapse")
        for d in t2:
            if lr2[d] is None:
                dd = r.add_dart()
                lr2[d] = dd
            else:
                dd = lr2[d]
            for i in range(0,r.Np1):
                ad = t2.alpha(i,d)
                if ad == d:
                    continue
                if lr2[ad] is None:
                    continue
                if r.alpha(i, dd) == lr2[ad]:
                    continue
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
                # if lr2[m2.l[d]] != None:
                #     if lr2[m2.l[d]] != m1.l[d]:
                #         raise Exception("multi_merge collapse")
                # lr2[m2.l[d]] = m1.l[d]
                wl = [ (m1.l[d], m2.l[d]) ]
                while len(wl) > 0:
                    (d1,d2) = wl.pop()
                    if lr2[d2] is None:
                        lr2[d2] = d1
                        for i in range(0, s.Np1):
                            dd1 = t1.alpha(i,d1)
                            dd2 = t2.alpha(i,d2)
                            if dd1 != d1 and dd2 != d2:
                                wl.append((dd1,dd2))
                    elif lr2[d2] != d1:
                        raise Exception("multi_merge collapse")
        for d in t2:
            if lr2[d] is None:
                dd = r.add_dart()
                lr2[d] = dd
            else:
                dd = lr2[d]
            for i in range(0,r.Np1):
                ad = t2.alpha(i,d)
                if ad == d:
                    continue
                if lr2[ad] is None:
                    continue
                r.sew(i,dd,lr2[ad])
        return r, PremapM(t2, r, lr2)
