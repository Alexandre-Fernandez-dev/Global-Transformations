import networkx as nx

# class GenPattern():
#     def __init__(self):
#         pass
#
# class EndPattern(GenPattern):
#     def __init__(self):
#         GenPattern.__init__(self)
#
#     def match(self,g,l):
#         yield l
#
# class ContPattern(GenPattern):
#     def __init__(self):
#         GenPattern.__init__(self)
#         self.next = None
#
#     def then(self, next):
#         if self.next == None:
#             self.next = next
#         else:
#             self.next.then(next)
#         return self
#
# class NodePattern(ContPattern):
#     def __init__(self, i):
#         ContPattern.__init__(self)
#         self.i = i
#
#     def match(self,g,l):
#         for i in self.iterator(g, l):
#             l[self.i] = i
#             for l in self.next.match(g, l): yield l
#
# class AHeadNodePattern(NodePattern):
#     def __init__(self, i):
#         NodePattern.__init__(self, i)
#
#     def iterator(self, g, l):
#         return list(g.nodes)
#
# class SourceNodePattern(NodePattern):
#     def __init__(self, edge_pat):
#         NodePattern.__init__(self, edge_pat.e[0])
#         self.edge_pat = edge_pat
#
#     def iterator(self, g, l):
#         yield l[self.edge_pat.e][0]
#
# class TargetNodePattern(NodePattern):
#     def __init__(self, edge_pat):
#         NodePattern.__init__(self, edge_pat.e[1])
#         self.edge_pat = edge_pat
#
#     def iterator(self, g, l):
#         yield l[self.edge_pat.e][1]
#
# class EdgePattern(ContPattern):
#     def __init__(self, e):
#         ContPattern.__init__(self)
#         self.e = e
#
#     def match(self,g,l):
#         for e in self.iterator(g, l):
#             l[self.e] = e
#             for l in self.next.match(g, l): yield l
#
# class AHeadEdgePattern(EdgePattern):
#     def __init__(self, e):
#         EdgePattern.__init__(self, e)
#
#     def iterator(self, g, l):
#         return list(g.edges)
#
# class OutgoingEdgePattern(EdgePattern):
#     def __init__(self, node_pat, e):
#         EdgePattern.__init__(self, e)
#         self.node_pat = node_pat
#
#     def iterator(self, g, l):
#         return list(g.out_edges(l[self.node_pat.i]))
#
# class IncomingEdgePattern(EdgePattern):
#     def __init__(self, node_pat, e):
#         EdgePattern.__init__(self, e)
#         self.node_pat = node_pat
#
#     def iterator(self, g, l):
#         return list(g.in_edges(l[self.node_pat.i]))


class EndPattern():
    def match(self, ctx):
        yield ctx.l

class ContPattern():
    def __init__(self):
        self.next = None

    def then(self, next):
        if self.next == None:
            self.next = next
        else:
            self.next.then(next)
        return self

class HeadNodePattern(ContPattern):
    def __init__(self, i):
        ContPattern.__init__(self)
        self.i = i

    def match(self, ctx):
        for i in ctx.g.nodes:
            if ctx.is_cursed(i): continue
            ctx.curse(i)
            ctx.l[self.i] = i
            for l in self.next.match(ctx): yield l
            ctx.uncurse(i)

class LoopPattern(ContPattern):
    def __init__(self, i, nii):
        ContPattern.__init__(self)
        self.i = i
        self.nii = nii
        pass

class CheckLoopPattern(LoopPattern):
    def __init__(self, i, nii):
        LoopPattern.__init__(self,i,nii)

    def match(self, ctx):
        i = ctx.l[self.i]
        if ctx.g.g.number_of_edges(i,i) < self.nii:
            return
        for l in self.next.match(ctx): yield l

class HeadLoopPattern(LoopPattern):
    def __init__(self, i, nii):
        LoopPattern.__init__(self,i,nii)

    def match(self, ctx):
        for i in ctx.g.nodes:
            if ctx.is_cursed(i): continue
            ctx.curse(i)
            nii = ctx.g.g.number_of_edges(i,i)
            if nii < self.nii:
                continue
            ctx.l[self.i] = i
            for l in self.next.match(ctx): yield l
            ctx.uncurse(i)

class PairPattern(ContPattern):
    def __init__(self, i, j, nij, nji):
        ContPattern.__init__(self)
        self.i = i
        self.j = j
        self.nij = nij
        self.nji = nji
        pass

class HeadPairPattern(PairPattern):
    def __init__(self, i, j, nij, nji):
        PairPattern.__init__(self,i,j,nij,nji)

    def match(self, ctx):
        for i in ctx.g.nodes:
            if ctx.is_cursed(i): continue
            ctx.curse(i)
            for j in ctx.g.nodes:
                if ctx.is_cursed(j): continue
                ctx.curse(j)
                nij = ctx.g.g.number_of_edges(i,j)
                nji = ctx.g.g.number_of_edges(j,i)
                if nij < self.nij or nji < self.nji:
                    continue
                ctx.l[self.i] = i
                ctx.l[self.j] = j
                for l in self.next.match(ctx): yield l
                ctx.uncurse(j)
            ctx.uncurse(i)

class OutgoingPairPattern(PairPattern):
    def __init__(self, i, j, nij, nji):
        PairPattern.__init__(self,i,j,nij,nji)

    def match(self, ctx):
        i = ctx.l[self.i]
        for j in ctx.g.g.successors(i) if self.nij > 0 else ctx.g.g.predecessors(i):
            if ctx.is_cursed(j): continue
            ctx.curse(j)
            if ctx.g.g.number_of_edges(i,j) < self.nij or ctx.g.g.number_of_edges(j,i) < self.nji:
                continue
            ctx.l[self.j] = j
            for l in self.next.match(ctx): yield l
            ctx.uncurse(j)

class IncomingPairPattern(PairPattern):
    def __init__(self, i, j, nij, nji):
        PairPattern.__init__(self,i,j,nij,nji)

    def match(self, ctx):
        j = ctx.l[self.j]
        for i in ctx.g.g.predecessors(j) if self.nij > 0 else ctx.g.g.successors(j):
            if ctx.is_cursed(i): continue
            ctx.curse(i)
            if ctx.g.g.number_of_edges(i,j) < self.nij or ctx.g.g.number_of_edges(j,i) < self.nji:
                continue
            ctx.l[self.i] = i
            for l in self.next.match(ctx): yield l
            ctx.uncurse(i)

class CheckPairPattern(PairPattern):
    def __init__(self, i, j, nij, nji):
        PairPattern.__init__(self,i,j,nij,nji)

    def match(self, ctx):
        i = ctx.l[self.i]
        j = ctx.l[self.j]
        if ctx.g.g.number_of_edges(i,j) < self.nij or ctx.g.g.number_of_edges(j,i) < self.nji:
            return
        for l in self.next.match(ctx): yield l


class GraphO():
    def __init__(self, g = None):
        if g == None:
            self.g = nx.MultiDiGraph()
        else:
            self.g = g

    def add_node(self):
        n = len(self.g)
        self.g.add_node(n)
        return n

    def add_edge(self,i,j):
        e = self.g.add_edge(i,j)
        return (i,j,e)

    def copy(self):
        return GraphO(self.g.copy())

    @property
    def nodes(self):
        return self.g.nodes

    @property
    def edges(self):
        return self.g.edges

    def out_edges(self, i):
        return self.g.out_edges(i, keys = True)

    def in_edges(self, i):
        return self.g.in_edges(i, keys = True)

    def __iter__(self):
        return self.g.iter()

    def __getitem__(self,n):
        return self.g[n]

    def __contains__(self,n):
        return self.g.__contains__(n)

    def __len__(self):
        return self.g.__len__()

    def __repr__(self):
        return "{ " + str(self.nodes) + ", " + str(self.edges) + " }";

    def pat(self):
        dep = nx.DiGraph()

        dep.add_node('r00t')

        for i in self.nodes:
            dep.add_node(i)
            dep.add_edge('r00t',i, weight = 1. + self.g.size())

        for i in self.nodes:
            for j in self.nodes:
                if i == j:
                    nii = self.g.number_of_edges(i,i)
                    if nii != 0:
                        dep.add_node((i,i,nii))
                        dep.add_edge('r00t',(i,i,nii), weight = 1.+1./nii)
                        dep.add_edge((i,i,nii),i, weight = 0.)
                        dep.add_edge(i,(i,i,nii), weight = 1.)
                    pass
                elif i < j:
                    nij = self.g.number_of_edges(i,j)
                    nji = self.g.number_of_edges(j,i)
                    if nij != 0 or nji != 0:
                        dep.add_node((i,j,(nij,nji)))
                        dep.add_edge('r00t',(i,j,(nij,nji)), weight = 1.+1./(nij+nji))
                        dep.add_edge((i,j,(nij,nji)),i, weight = 0.)
                        dep.add_edge((i,j,(nij,nji)),j, weight = 0.)
                        dep.add_edge(i,(i,j,(nij,nji)), weight = 1.)
                        dep.add_edge(j,(i,j,(nij,nji)), weight = 1.)
                    pass

        print(str(dep.nodes))
        print(str(dep.edges(data=True)))

        ed = nx.algorithms.tree.branchings.Edmonds(dep)
        B = ed.find_optimum('weight', 1, kind='min', style='arborescence')
        #B = nx.algorithms.tree.branchings.greedy_branching(dep)
        print(nx.algorithms.tree.branchings.branching_weight(B))
        print(B.nodes)
        print(B.edges)
        C = nx.algorithms.dag.topological_sort(B)

        startpat = ContPattern()
        endpat = EndPattern()

        def unique_pred(B,i):
            for j in B.predecessors(i):
                return j

        l = set()
        for i in C:
            print(str(i))
            if i == 'r00t': continue
            p = unique_pred(B,i)

            pat = ContPattern()
            if p == 'r00t':
                if type(i) == int:
                    print("Head Node")
                    pat = HeadNodePattern(i)
                    l.add(i)
                elif i[0] == i[1]:
                    print("Head Loop")
                    pat = HeadLoopPattern(i[0],i[2])
                    l.add(i[0])
                else:
                    print("Head Pair")
                    pat = HeadPairPattern(i[0],i[1],i[2][0],i[2][1])
                    l.add(i[0])
                    l.add(i[1])
            elif type(i) == int:
                continue
            else:
                (i,j,s) = i
                if i == j:
                    print("Check Loop")
                    pat = CheckLoopPattern(i,s)
                else:
                    if i in l:
                        if j in l:
                            print("Check Pair")
                            pat = CheckPairPattern(i,j,s[0],s[1])
                        else:
                            print("Outgoing")
                            pat = OutgoingPairPattern(i,j,s[0],s[1])
                            l.add(j)
                    else:
                        if j in l:
                            print("Incoming")
                            pat = IncomingPairPattern(i,j,s[0],s[1])
                            l.add(i)
                        else:
                            print("WTF")
                            continue
            startpat = startpat.then(pat)

        return startpat.then(endpat).next





# [('r00t', (0, 1, (2, 2)), {'weight': 1.25}),
# ('r00t', (0, 2, (1, 2)), {'weight': 1.3333333333333333}),
# ('r00t', (0, 3, (1, 0)), {'weight': 2.0}),
# ('r00t', (1, 1, 2), {'weight': 1.5}),
# ('r00t', (1, 2, (0, 1)), {'weight': 2.0}),
# (0, (0, 1, (2, 2)), {'weight': 1.0}),
# (0, (0, 2, (1, 2)), {'weight': 1.0}),
# (0, (0, 3, (1, 0)), {'weight': 1.0}),
# (1, (0, 1, (2, 2)), {'weight': 1.0}),
# (1, (1, 1, 2), {'weight': -10.0}),
# (2, (0, 2, (1, 2)), {'weight': 1.0}),
# (2, (1, 2, (0, 1)), {'weight': 1.0}),
# ((0, 1, (2, 2)), 0, {'weight': -10.0}),
# ((0, 1, (2, 2)), 1, {'weight': -10.0}),
# ((0, 2, (1, 2)), 0, {'weight': -10.0}),
# ((0, 2, (1, 2)), 2, {'weight': -10.0}),
# ((0, 3, (1, 0)), 0, {'weight': -10.0}),
# ((0, 3, (1, 0)), 3, {'weight': -10.0}),
# ((1, 1, 2), 1, {'weight': -10.0}),
# ((1, 2, (0, 1)), 1, {'weight': -10.0}),
# ((1, 2, (0, 1)), 2, {'weight': -10.0})]


#
# # [(, ),
#    (, (0, 2, (1, 2))),
#    (, (0, 3, (1, 0))),
#    (1, (1, 1, 2)),
#    (2, (1, 2, (0, 1))),
#    (, ),
#    ((0, 2, (1, 2)), 2),
#    ((0, 3, (1, 0)), 3),
#    ((1, 2, (0, 1)), 1)]
#
# 'r00t'
# (0, 1, (2, 2))
# 0

class GraphM:
    def __init__(self, s, t, l):
        self.s = s
        self.t = t
        self.l = l

    def __eq__(self, other):
        return self.s == other.s and self.t == other.t and self.l == other.l

    def apply(self, e):
        return self.l[e]

    def __repr__(self):
        return "[ " + str(self.l) + " ]"

class Graph:

    @staticmethod
    def merge(m1, m2):
        if m1.s != m2.s:
            raise Exception("Not same source")
        s = m1.s
        t1 = m1.t
        t2 = m2.t
        l1 = {}
        l2 = {}
        r = s.copy()

        for i in r.nodes:
            l1[m1.l[i]] = i
            l2[m2.l[i]] = i

        for e in r.edges:
            l1[m1.l[e]] = e
            l2[m2.l[e]] = e

        for i in t1.nodes:
            if i not in l1:
                l1[i] = r.add_node()

        for i in t2.nodes:
            if i not in l2:
                l2[i] = r.add_node()

        for (i,j,e) in t1.edges:
            if (i,j,e) not in l1:
                l1[(i,j,e)] = r.add_edge(l1[i],l1[j])

        for (i,j,e) in t2.edges:
            if (i,j,e) not in l2:
                l2[(i,j,e)] = r.add_edge(l2[i],l2[j])

        return r, GraphM(t1, r, l1), GraphM(t2, r, l2)

#
# g = GraphO()
# n1 = g.add_node()
# n2 = g.add_node()
# n3 = g.add_node()
# e1 = g.add_edge(n1, n2)
# e2 = g.add_edge(n1, n2)
#
# p1 = AHeadNodePattern(n2)
# p2 = IncomingEdgePattern(p1,e1)
# p3 = SourceNodePattern(p2)
# p4 = OutgoingEdgePattern(p3,e2)
#
# pat = p1.then(p2).then(p3).then(p4).then(EndPattern())

# for l in pat.match(g,{}):
#     print("=> " + str(l))
#
# print(str(g.g.in_edges(1)))

g = GraphO()
n1 = g.add_node()
n2 = g.add_node()
n3 = g.add_node()
n4 = g.add_node()
# e1 = g.add_edge(n1, n2)
# e1 = g.add_edge(n1, n2)
# e1 = g.add_edge(n2, n1)
# e1 = g.add_edge(n2, n1)
# e2 = g.add_edge(n3, n2)
# e1 = g.add_edge(n1, n3)
# e1 = g.add_edge(n3, n1)
# e1 = g.add_edge(n3, n1)
# e1 = g.add_edge(n1, n4)
# e1 = g.add_edge(n2, n2)
# e1 = g.add_edge(n2, n2)



class Ctx():
    def __init__(self,g):
        self.l = {}
        self.g = g
        self.c = set()

    def curse(self,i):
        self.c.add(i)

    def is_cursed(self,i):
        return i in self.c

    def uncurse(self,i):
        self.c.remove(i)

ctx = Ctx(g)

pat = g.pat()
print(pat)

for l in pat.match(ctx):
    print(str(l))

import sys
sys.exit(0)

# [, , , , , , , , , , ]
#
# (2, 3, 1)
# 3         by ((2, 3, 1), 3)
# (2, 3, 0) by (3, (2, 3, 0))
# 2         by ((2, 3, 1), 2)
# (2, 0, 0) by (2, (2, 0, 0))
# 0         by ((2, 0, 0), 0)
# (1, 0, 1) by (0, (1, 0, 1))
# 1         by ((1, 0, 1), 1)
# (1, 0, 0) by (1, (1, 0, 0))
# (0, 1, 1) by (1, (0, 1, 1))
# (0, 1, 0) by (0, (0, 1, 0))
# (1, 2, 0) by (2, (1, 2, 0))
#









print(str(g.nodes) + " " + str(g.edges))

gl = GraphO()
m1 = gl.add_node()
m2 = gl.add_node()
m3 = gl.add_node()
m4 = gl.add_node()
f1 = gl.add_edge(m2, m3)
f2 = gl.add_edge(m1, m4)

print(str(gl.nodes) + " " + str(gl.edges))

m = GraphM(g, gl, {})
m.l[n1] = m2
m.l[n2] = m3
m.l[n3] = m1
m.l[e1] = f1

print(m)

print(Graph.merge(m, m))

# import copy
#
# class GraphO:
#     def __init__(self):
#         self.n = 0
#         self.e = {}
#
#     def add_node(self):
#         self.n+=1
#         return self.n-1
#
#     def add_edge(self, i, j):
#         if max(i, j) >= self.n or min(i, j) < 0:
#            raise Exception("Dangling edge")
#         if i <= j:
#             n_e = (i, j)
#         else:
#             n_e = (j, i)
#         id = -len(self.e)-1
#         self.e[id] = n_e
#         return id
#
#     def __repr__(self):
#         return "{ " + str(self.n) + ", " + str(self.e) + " }";
#
#
# class GraphM:
#     def __init__(self, s, t, l):
#         self.s = s
#         self.t = t
#         self.l = l
#
#     def __eq__(self, other):
#         return self.s == other.s and self.t == other.t and self.l == other.l
#
#     def apply(self, e):
#         return self.l[e]
#
#     def __repr__(self):
#         return "[ " + str(self.l) + " ]"
#
#     def pattern_match(self, p, g):
#         l = { }
#         h = GraphM(p, g, l)
#
#         pass
#
#
#
