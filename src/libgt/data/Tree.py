from .DataStructure import DataStructure


class TreeO():
    pass

class TreeLeaf(TreeO):
    _leaf = None
    def __new__(class_, *args, **kwargs):
        if class_._leaf is None:
            class_._leaf = TreeO.__new__(class_, *args, **kwargs)
        return class_._leaf

    def __init__(self):
        pass

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return 11

    def __repr__(self):
        return f"TreeLeaf()"
    
    def merge_in_place(self, y):
        if not(y is None or isinstance(y, TreeLeaf)):
            raise Exception("TreeLeaf: merge_in_place: impossible merging")

    def merge(self, y):
        if y is None or isinstance(y, TreeLeaf):
            return self
        else:
            raise Exception("TreeLeaf: merge: impossible merging")

class TreeNode(TreeO):

    def __init__(self, l, r):
        self.l = l
        self.r = r
        self.__h = None
        pass

    def __eq__(self, other):
        if not isinstance(other,TreeNode):
            return False
        return self.l == other.l and self.r == other.r

    def __hash__(self):
        if self.__h is None:
            self.__h = hash(self.l) ^ 31 * hash(self.r)
        return self.__h

    def __repr__(self):
        return f"TreeNode({repr(self.l)},{repr(self.r)})"

    def merge_in_place(self, y):
        if y is None:
            return
        if isinstance(y, TreeNode):
            if self.l is None:
                self.l = y.l
            else:
                self.l.merge_in_place(y.l)
            if self.r is None:
                self.r = y.r
            else:
                self.r.merge_in_place(y.r)
        else:
            raise Exception("TreeNode: merge_in_place: impossible merging")

    def merge(self, y):
        if y is None:
            return self
        if isinstance(y, TreeNode):
            return TreeNode(
                y.l if self.l is None else self.l.merge(y.l),
                y.r if self.r is None else self.r.merge(y.r)
            )
        else:
            raise Exception("TreeNode: merge: impossible merging")




class TreeM():
    Left = 0
    Right = 1
    
    def __init__(self, s, t, p):
        assert TreeM.well_defined(p, s, t)
        self.s = s
        self.t = t
        self.p = p

    @staticmethod
    def follow(x, p):
        for mv in p:
            if isinstance(x, TreeNode):
                x = x.l if mv == TreeM.Left else x.r
            else:
                raise Exception("TreeM: follow: impossible path")
        return x

    @staticmethod
    def well_defined(p, x, y):
        try:
            y = TreeM.follow(y, p)
            return TreeM.well_defined_aux(x, y)
        except:
            return False

    @staticmethod
    def well_defined_aux(x, y):
        if x is None:
            return True
        if isinstance(x, TreeLeaf) and isinstance(y, TreeLeaf):
            return True
        if isinstance(x, TreeNode) and isinstance(y, TreeNode):
            return TreeM.well_defined_aux(x.l, y.l) and TreeM.well_defined_aux(x.r, y.r)
        return False

    def compose(self,h):
        assert self.t == h.s
        return TreeM(self.s,h.t,h.p + self.p)

    @staticmethod
    def merge_along(x, y, p):
        if len(p) == 0:
            if x is None:
                return y
            else:
                return x.merge(y)
        if not isinstance(x, TreeNode):
            raise Exception("TreeM: merge_along: illegal merge")
        if p[0] == TreeM.Left:
            return TreeNode(TreeM.merge_along(x.l, y, p[1:]), x.r)
        else:
            return TreeNode(x.l, TreeM.merge_along(x.r, y, p[1:]))
    
    @staticmethod
    def merge_along_in_place(x, y, p):
        if len(p) == 0:
            if x is None:
                if y is not None:
                    raise Exception("TreeM: merge_along_in_place: cannot do untrivial merge on None")
            else:
                x.merge_in_place(y)
        else:
            x = TreeM.follow(x, p[:-1])
            if isinstance(x, TreeNode):
                x.merge_in_place(TreeNode(y, None) if p[-1] == TreeM.Left else TreeNode(None, y))
            else:
                raise Exception("TreeM: merge_along_in_place: illegal merge")


    @staticmethod
    def merge_along_in_place_aux(x, y):
        if x is None:
            return y
        if y is None:
            return x
        if x is TreeLeaf() and y is TreeLeaf(): 
            return TreeLeaf()
        if isinstance(x, TreeNode) and isinstance(y, TreeNode):
            TreeNode(TreeM.merge_along_aux(x.l, y.l), TreeM.merge_along_aux(x.r, y.r))
        assert False


    def __eq__(self, other):
        if not isinstance(other,TreeM):
            return False
        return self.s == other.s and self.t == other.t and self.p == other.p

    def __hash__(self):
        r = hash(self.s) ^ 31 * hash(self.t)
        for lr in self.p:
            r ^= hash(lr) * 31 * r
        return r

    def __repr__(self):
        return f"TreeM({self.s},{self.t},{self.p})"

    @property
    def dom(self):
        return self.s

    @property
    def cod(self):
        return self.t

    def clean(self):
        self.p = self.p.copy()


class Tree(DataStructure):

    @staticmethod
    def TO():
        return TreeO

    @staticmethod
    def TM():
        return TreeM

    @staticmethod
    def pattern_match_object(p, X, s, m):
        if TreeM.well_defined_aux(p, s):
            yield TreeM(p, X, m.copy())
        if isinstance(s, TreeNode):
            m.append(TreeM.Left)
            yield from Tree.pattern_match_object(p, X, s.l, m.copy())
            m[-1] = TreeM.Right
            yield from Tree.pattern_match_object(p, X, s.r, m.copy())
            del m[-1]

    @staticmethod
    def pattern_match(p, X):
        if p is None or isinstance(p,TreeO):
            yield from Tree.pattern_match_object(p, X, X, [])
        else:
            # print(f'pattern match: {p} in {X}')
            if len(X.p) >= len(p.p):
                if X.p[len(X.p)-len(p.p):] == p.p:
                    m = X.p[0:len(X.p)-len(p.p)]
                    if TreeM.well_defined(m, p.cod, X.cod):
                        ins = TreeM(p.cod, X.cod, m.copy())
                        yield ins

    @staticmethod
    def multi_merge(m1s, m2s):
        if len(m1s[0].p) < len(m2s[0].p):
            (a,b,c) = Tree.multi_merge(m2s, m1s)
            return (a,c,b)
        q = m1s[0].p[0:len(m1s[0].p)-len(m2s[0].p)]
        for m1, m2 in zip(m1s, m2s):
            assert(m1.p == q + m2.p)
        t1 = m1s[0].t
        t2 = m2s[0].t
        r = TreeM.merge_along(t1,t2,q)
        # print(f'multi_merge: {m1s} {m2s}')
        # print(f'             {q}')
        # print(f'             {r}')
        return (r, TreeM(t1,r,[]), TreeM(t2,r,q))

    @staticmethod
    def multi_merge_2_in_1(m1s, m2s):
        if len(m1s[0].p) < len(m2s[0].p):
            raise Exception("Tree: multi_merge_2_in_1: the required merge cannot be done in place")
        q = m1s[0].p[0:len(m1s[0].p)-len(m2s[0].p)]
        for m1, m2 in zip(m1s, m2s):
            assert(m1.p == q + m2.p)
        t1 = m1s[0].t
        t2 = m2s[0].t
        TreeM.merge_along_in_place(t1,t2,q)
        return (t1, TreeM(t2,t1,q))

    
