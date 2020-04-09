import math
import networkx as nx
from DataStructure import DataStructure
import matplotlib.pyplot as plt
from itertools import chain
import time

show = False

# def draw_pat(g, pats, text):
#     plt.subplot(121)
#     options = {
#         'node_size': 10,
#         'width': 1,
#     }
#     color_map = []
#     for node in g:
#         color_map.append('gray')
#     for m in pats:
#         for node in m.s.g:
#             color_map[m.l[node]] = 'black'
#
#     reverse_map = {}
#     e_color_map = []
#     i = 0
#     for (u,v,d) in g.edges(keys = True):
#         e_color_map.append('gray')
#         reverse_map[(u,v,d)] = i
#         i += 1
#
#     for m in pats:
#         for (u,v,d) in m.s.g.edges(keys = True):
#             e_color_map[reverse_map[m.l[(u,v,d)]]] = 'black'
#
#     nx.draw_kamada_kawai(g, node_color = color_map, edge_color = e_color_map, **options)
#     figManager = plt.get_current_fig_manager()
#     figManager.window.showMaximized()
#     plt.title(text)
#     plt.show()

def draw(m1s, m2s, text):
    fig, axes = plt.subplots(nrows=1, ncols=2)

    m1t = m1s[0].t
    m2t = m2s[0].t
    ax = axes.flatten()
    options = {
        'node_size': 20,
        'width': 1,
    }
    color_map = []
    for node in m1t.g:
        color_map.append('black')
    for m1 in m1s:
        for node in m1.s.g:
            color_map[m1.l[node]] = 'red'

    reverse_map = {}
    e_color_map = []
    i = 0
    for (u,v,d) in m1t.g.edges(keys = True):
        e_color_map.append('black')
        reverse_map[(u,v,d)] = i
        i += 1

    for m1 in m1s:
        for (u,v,d) in m1.s.g.edges(keys = True):
            e_color_map[reverse_map[m1.l[(u,v,d)]]] = 'red'

    nx.draw_kamada_kawai(m1.t.g, node_color = color_map, edge_color = e_color_map, ax=ax[0], **options)

    options = {
        'node_size': 20,
        'width': 1,
    }
    color_map = []
    for node in m2t.g:
        color_map.append('black')
    for m2 in m2s:
        for node in m2.s.g:
            color_map[m2.l[node]] = 'red'

    reverse_map = {}
    e_color_map = []
    i = 0
    for (u,v,d) in m2t.g.edges(keys = True):
        e_color_map.append('black')
        reverse_map[(u,v,d)] = i
        i += 1

    for m2 in m2s:
        for (u,v,d) in m2.s.g.edges(keys = True):
            e_color_map[reverse_map[m2.l[(u,v,d)]]] = 'red'

    nx.draw_kamada_kawai(m2.t.g, node_color = color_map, edge_color = e_color_map, ax=ax[1], **options)
    figManager = plt.get_current_fig_manager()
    # figManager.window.showMaximized()
    plt.title(text)
    plt.show()

def kth_injection(p,q,k):
    if (p,q) not in kth_injection.mem: kth_injection.mem[(p,q)] = [ None ] * (math.factorial(q) // math.factorial(q-p))

    l = kth_injection.mem[(p,q)][k]

    if (l != None): return l

    r = []
    for i in range(q-p+1,q+1):
        l = k % i
        for x, v in enumerate(r): r[x] = (v + l + 1)%i
        r.append(l)

    r.reverse()
    kth_injection.mem[(p,q)][k] = r
    return r
kth_injection.mem = {}

def injections(p,q):
    for k in range(math.factorial(q) // math.factorial(q-p)):
        kth_injection(p,q,k)
    return kth_injection.mem[(p,q)]

class EndPattern():
    def match(self, ctx):
        yield ctx.l

    def __repr__(self):
        return 'STOP'

class ContPattern():
    def __init__(self):
        self.next = None

    def then(self, next):
        if self.next == None:
            self.next = next
        else:
            self.next.then(next)
        return self

    def __repr__(self):
        return " => " + str(self.next)

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

    def pr(self):
        return 'HN(' + str(self.i) + ')'

class HalfPairPattern(ContPattern):
    def __init__(self, i, j, nij):
        ContPattern.__init__(self)
        self.i = i
        self.j = j
        self.nij = nij
        pass

class CheckHalfPairPattern(HalfPairPattern):
    def __init__(self, i, j, nij):
        HalfPairPattern.__init__(self,i,j,nij)

    def match(self, ctx):
        i = ctx.l[self.i]
        j = ctx.l[self.j]
        if ctx.g.g.number_of_edges(i,j) < self.nij:
            return
        for l in self.next.match(ctx): yield l

    def pr(self):
        return 'CHP(' + str(self.i) + ' => ' + str(self.j) + ' - ' + str(self.nij) + ')'

class HeadHalfPairPattern(HalfPairPattern):
    def __init__(self, i, j, nij):
        HalfPairPattern.__init__(self,i,j,nij)
        self.__loop = (i == j)

    def match(self, ctx):
        if self.__loop:
            for i in ctx.g.nodes:
                if ctx.is_cursed(i): continue
                if ctx.g.g.number_of_edges(i,i) < self.nij:
                    continue
                ctx.curse(i)
                ctx.l[self.i] = i
                for l in self.next.match(ctx): yield l
                ctx.uncurse(i)
        else:
            for i in ctx.g.nodes:
                if ctx.is_cursed(i): continue
                ctx.curse(i)
                for j in ctx.g.nodes:
                    if ctx.is_cursed(j): continue
                    if ctx.g.g.number_of_edges(i,j) < self.nij:
                        continue
                    ctx.curse(j)
                    ctx.l[self.i] = i
                    ctx.l[self.j] = j
                    for l in self.next.match(ctx): yield l
                    ctx.uncurse(j)
                ctx.uncurse(i)

    def pr(self):
        return 'HHP(' + str(self.i) + ' => ' + str(self.j) + ' - ' + str(self.nij) + ')'

class OutgoingHalfPairPattern(HalfPairPattern):
    def __init__(self, i, j, nij):
        HalfPairPattern.__init__(self,i,j,nij)

    def match(self, ctx):
        i = ctx.l[self.i]
        for j in ctx.g.g.successors(i):
            if ctx.is_cursed(j): continue
            if ctx.g.g.number_of_edges(i,j) < self.nij:
                continue
            ctx.curse(j)
            ctx.l[self.j] = j
            for l in self.next.match(ctx): yield l
            ctx.uncurse(j)

    def pr(self):
        return 'OHP(' + str(self.i) + ' -> ' + str(self.j) + ' - ' + str(self.nij) + ')'

class IncomingHalfPairPattern(HalfPairPattern):
    def __init__(self, i, j, nij):
        HalfPairPattern.__init__(self,i,j,nij)

    def match(self, ctx):
        j = ctx.l[self.j]
        for i in ctx.g.g.predecessors(j):
            if ctx.is_cursed(i): continue
            if ctx.g.g.number_of_edges(i,j) < self.nij:
                continue
            ctx.curse(i)
            ctx.l[self.i] = i
            for l in self.next.match(ctx): yield l
            ctx.uncurse(i)

    def pr(self):
        return 'IHP(' + str(self.i) + ' -> ' + str(self.j) + ' - ' + str(self.nij) + ')'

class EdgePattern(ContPattern):
    def __init__(self, i, j, nij):
        ContPattern.__init__(self)
        self.i = i
        self.j = j
        self.nij = nij
        pass

    def match(self, ctx):
        i = ctx.l[self.i]
        j = ctx.l[self.j]
        nij = ctx.g.g.number_of_edges(i,j)
        for l in injections(self.nij,nij):
            for e in range(self.nij):
                ctx.l[(self.i,self.j,e)] = (i,j,l[e])
            for ll in self.next.match(ctx): yield ll

    def pr(self):
        return 'E(' + str(self.i) + ' => ' + str(self.j) + ')'

class PartialEdgePattern(ContPattern):
    def __init__(self, i, j, nij, keij):
        ContPattern.__init__(self)
        self.i = i
        self.j = j
        self.nij = nij
        self.kij = len(keij)
        self.keij = keij
        self.ueij = [ e for e in range(nij) if e not in keij ]
        pass

    def match(self, ctx):
        i = ctx.l[self.i]
        j = ctx.l[self.j]
        nij = ctx.g.g.number_of_edges(i,j)
        bound_ij = map(lambda e: ctx.l[(self.i,self.j,e)][2], self.keij)
        free_ij = [ e for e in range(nij) if e not in bound_ij ]
        for l in injections(self.nij-self.kij,nij-self.kij):
            for e in range(self.nij-self.kij):
                ctx.l[(self.i,self.j,self.ueij[e])] = (i,j,free_ij[l[e]])
            for ll in self.next.match(ctx): yield ll

    def pr(self):
        return 'PE(' + str(self.i) + ' => ' + str(self.j) + ' - ' + str(self.keij) +' in [0,' + str(self.nij-1) + '])'

class GraphO():
    def __init__(self, g = None):
        if g == None:
            self.g = nx.MultiDiGraph()
        else:
            self.g = g
        self.__pattern = None

    def restrict(self, h):
        if isinstance(h, GraphM):
            return h
        else:
            raise Exception("PROUT")

    def __eq__(self, other):
        if not isinstance(other, GraphO):
            return False
        return self.g == other.g

    def __hash__(self):
        return hash(self.g)

    def add_node(self):
        n = self.g.number_of_nodes()
        self.g.add_node(n)
        return n

    def add_edge(self,i,j):
        e = self.g.add_edge(i,j)
        return (i,j,e)

    def copy(self):
        cp = GraphO(self.g.copy())
        return cp

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

    def pattern(self):
        if self.__pattern == None:
            self.__pattern = self.pat()
        return self.__pattern

    def pat(self, known_nodes = set(), known_edges = {}):

        dep = nx.DiGraph()

        dep.add_node('r00t')

        for i in self.nodes:
            dep.add_node(i)
            dep.add_edge('r00t',i, weight = 0. if i in known_nodes else (1. + self.g.size()))

        for i in self.nodes:
            for j in self.nodes:
                if i == j:
                    kii = len(known_edges[i,i]) if (i,i) in known_edges else 0
                    nii = self.g.number_of_edges(i,i) - kii
                    if nii > 0:
                        dep.add_node((i,i))
                        dep.add_edge('r00t',(i,i), weight = 1.+1./nii)
                        dep.add_edge((i,i),i, weight = 0.)
                        dep.add_edge(i,(i,i), weight = 1.)
                    pass
                elif i < j:
                    kij = len(known_edges[i,j]) if (i,j) in known_edges else 0
                    kji = len(known_edges[j,i]) if (j,i) in known_edges else 0
                    nij = self.g.number_of_edges(i,j) - kij
                    nji = self.g.number_of_edges(j,i) - kji
                    if nij > 0:
                        dep.add_node((i,j))
                        dep.add_edge((i,j),i, weight = 0.)
                        dep.add_edge((i,j),j, weight = 0.)
                        dep.add_edge(i,(i,j), weight = 1.)
                        dep.add_edge(j,(i,j), weight = 1.)
                        dep.add_edge('r00t',(i,j), weight = 1.+1./(nij+nji))
                    if nji > 0:
                        dep.add_node((j,i))
                        dep.add_edge((j,i),i, weight = 0.)
                        dep.add_edge((j,i),j, weight = 0.)
                        dep.add_edge(i,(j,i), weight = 1.)
                        dep.add_edge(j,(j,i), weight = 1.)
                        if nij == 0:
                            dep.add_edge('r00t',(j,i), weight = 1.+1./(nij+nji))
                        else: # nij > 0 and nji > 0
                            dep.add_edge((i,j),(j,i), weight = 0.)
                            dep.add_edge((j,i),(i,j), weight = 0.)
                    pass

        ed = nx.algorithms.tree.branchings.Edmonds(dep)
        B = ed.find_optimum('weight', 1, kind='min', style='arborescence')
        C = nx.algorithms.dag.topological_sort(B)

        startpat = ContPattern()
        endpat = EndPattern()

        l = known_nodes.copy()
        for i in C:
            if i == 'r00t':
                continue

            pat = None
            if type(i) == int:
                if i in l:
                    continue
                else:
                    pat = HeadNodePattern(i)
                    l.add(i)
            else:
                (i,j) = i
                nij = self.g.number_of_edges(i,j)
                if i in l:
                    if j in l:
                        pat = CheckHalfPairPattern(i,j,nij)
                    else:
                        pat = OutgoingHalfPairPattern(i,j,nij)
                        l.add(j)
                else:
                    if j in l:
                        pat = IncomingHalfPairPattern(i,j,nij)
                        l.add(i)
                    else:
                        pat = HeadHalfPairPattern(i,j,nij)
                        l.add(i)
                        l.add(j)
                if (i,j) in known_edges:
                    endpat = PartialEdgePattern(i,j,nij,known_edges[i,j]).then(endpat)
                else:
                    endpat = EdgePattern(i,j,nij).then(endpat)
            startpat = startpat.then(pat)

        return startpat.then(endpat).next

class GraphM:
    def __init__(self, s, t, l):
        self.s = s
        self.t = t
        self.l = l
        self.__pattern = None
        hash(self)

    def compose(self,h):
        assert self.t == h.s
        # print(self.l, "\n|", h.l)
        l = { k: h.l[v] for k, v in self.l.items() }
        return GraphM(self.s,h.t,l)

    def __eq__(self, other):
        if not isinstance(other,GraphM):
            #print("~ instance not ok")
            return False
        return self.s == other.s and self.t == other.t and self.l == other.l

    def __hash__(self):
        r = hash(self.s) ^ hash(self.t)
        for k, v in self.l.items():
            r ^= 31 * hash(k)
            r ^= 31 * hash(v)
        return r

    def apply(self, e):
        return self.l[e]

    def __repr__(self):
        return "[ " + str(self.s) + " -> " + str(self.t) + ": " + str(self.l) + " ]"

    @property
    def dom(self):
        return self.s

    @property
    def cod(self):
        return self.t

    def pattern(self):
        if self.__pattern == None:
            known_nodes = { self.l[i] for i in self.s.nodes }
            known_edges = {}
            for (i,j,e) in self.s.edges:
                (ii,jj,ee) = self.l[(i,j,e)]
                known_edges.setdefault((ii,jj),set()).add(ee)
            self.__pattern = self.t.pat(known_nodes = known_nodes, known_edges = known_edges)
        return self.__pattern

    def clean(self):
        self.l = self.l.copy()

draw_pats = []

class Graph(DataStructure):

    @staticmethod
    def TO():
        return GraphO

    @staticmethod
    def TM():
        return GraphM

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

    @staticmethod
    def pattern_match(p, g):
        if isinstance(p,GraphO):
            pat = p.pattern()
            ctx = Graph.Ctx(g)
            for l in pat.match(ctx):
                m = GraphM(p,g,l)
                yield m
        else:
            pat = p.pattern()
            ctx = Graph.Ctx(g.cod)
            for i_eij, ii_eeij in g.l.items():
                if type(i_eij) == int:
                    ctx.curse(ii_eeij)
                ctx.l[p.l[i_eij]] = ii_eeij
            for l in pat.match(ctx):
                m = GraphM(p.cod,g.cod,l)
                yield m

    @staticmethod
    def multi_merge(m1s, m2s):
        global show
        if show:
            draw(m1s, m2s, "multi_merge")
        t1 = m1s[0].t
        t2 = m2s[0].t
        r = t1.copy()
        lr1 = { k:k for k in chain(iter(t1.nodes), iter(t1.edges)) } #identity
        lr2 = {}
        for m1, m2 in zip(m1s, m2s):
            assert m1.s == m2.s and m1.t == t1 and m2.t == t2
            s = m1.s
            for n in s.nodes:
                if lr2.get(m2.l[n]) != None:
                    if lr2[m2.l[n]] != m1.l[n]:
                        # conflict
                        raise Exception("multi_merge collapse")
                lr2[m2.l[n]] = m1.l[n] #lr1 is identity
            for e in s.edges:
                if lr2.get(m2.l[e]) != None:
                    if lr2[m2.l[e]] != m1.l[e]:
                        # conflict
                        raise Exception("multi_merge collapse")
                lr2[m2.l[e]] = m1.l[e] #lr1 is identity
        for n in t2.nodes:
            if n not in lr2:
                lr2[n] = r.add_node()
        for (i, j, e) in t2.edges:
            if (i, j, e) not in lr2:
                lr2[(i, j, e)] = r.add_edge(lr2[i], lr2[j])
        return r, GraphM(t1, r, lr1), GraphM(t2, r, lr2)

    @staticmethod
    def multi_merge_2_in_1(m1s, m2s):
        global show
        if show:
            draw(m1s, m2s, "multi_merge")
        t1 = m1s[0].t
        t2 = m2s[0].t
        r = t1
        lr2 = {}
        for m1, m2 in zip(m1s, m2s):
            assert m1.s == m2.s and m1.t == t1 and m2.t == t2
            s = m1.s
            for n in s.nodes:
                if lr2.get(m2.l[n]) != None:
                    if lr2[m2.l[n]] != m1.l[n]:
                        # conflict
                        raise Exception("multi_merge collapse")
                lr2[m2.l[n]] = m1.l[n] #lr1 is identity
            for e in s.edges:
                if lr2.get(m2.l[e]) != None:
                    if lr2[m2.l[e]] != m1.l[e]:
                        # conflict
                        raise Exception("multi_merge collapse")
                lr2[m2.l[e]] = m1.l[e] #lr1 is identity
        for n in t2.nodes:
            if n not in lr2:
                lr2[n] = r.add_node()
        for (i, j, e) in t2.edges:
            if (i, j, e) not in lr2:
                lr2[(i, j, e)] = r.add_edge(lr2[i], lr2[j])
        return r, GraphM(t2, r, lr2)

def test_multi_merge():
    g1 = GraphO()
    n1_1 = g1.add_node()
    n1_2 = g1.add_node()
    e1_12 = g1.add_edge(n1_1, n1_2)

    g2 = GraphO()
    n2_1 = g2.add_node()
    n2_2 = g2.add_node()
    n2_3 = g2.add_node()
    e2_12 = g2.add_edge(n2_1, n2_2)
    e2_23 = g2.add_edge(n2_2, n2_3)
    e2_31 = g2.add_edge(n2_3, n2_1)

    #span a
    ma121 = GraphM(g1, g2, {
        n1_1: n2_2,
        n1_2: n2_3,
        e1_12: e2_23
    })

    ma122 = GraphM(g1, g2, {
        n1_1: n2_3,
        n1_2: n2_1,
        e1_12: e2_31
    })

    # span b
    mb121 = GraphM(g1, g2, {
        n1_1: n2_3,
        n1_2: n2_1,
        e1_12: e2_31
    })

    mb122 = GraphM(g1, g2, {
        n1_1: n2_1,
        n1_2: n2_2,
        e1_12: e2_12
    })

    print(Graph.multi_merge([ma121, mb121], [ma122, mb122]))
    print()

    g1 = GraphO()
    n1_1 = g1.add_node()
    n1_2 = g1.add_node()
    e1_12 = g1.add_edge(n1_1, n1_2)

    g2 = GraphO()
    n2_1 = g2.add_node()
    n2_2 = g2.add_node()
    n2_3 = g2.add_node()
    e2_12 = g2.add_edge(n2_1, n2_2)
    e2_23 = g2.add_edge(n2_2, n2_3)
    e2_31 = g2.add_edge(n2_3, n2_1)

    g3 = g2.copy()

    ma121 = GraphM(g1, g2, {
        n1_1: n2_2,
        n1_2: n2_3,
        e1_12: e2_23
    })

    ma132 = GraphM(g1, g3, {
        n1_1: n2_3,
        n1_2: n2_1,
        e1_12: e2_31
    })

    mb121 = GraphM(g1, g2, {
        n1_1: n2_3,
        n1_2: n2_1,
        e1_12: e2_31
    })

    mb132 = GraphM(g1, g3, {
        n1_1: n2_1,
        n1_2: n2_2,
        e1_12: e2_12
    })

    print(Graph.multi_merge_2_in_1([ma121, mb121], [ma132, mb132]))


def test_merge():
    g1 = GraphO()
    n1 = g1.add_node()
    n2 = g1.add_node()
    n3 = g1.add_node()
    e1 = g1.add_edge(n1,n2)

    g2 = GraphO()
    n4 = g2.add_node()
    n5 = g2.add_node()
    n6 = g2.add_node()
    n7 = g2.add_node()
    e2 = g2.add_edge(n5,n6)
    e3 = g2.add_edge(n4,n7)

    h = GraphM(g1,g2,{
        n1: n5,
        n2: n6,
        n3: n4,
        e1: e2
    })
    print(h)
    print(Graph.merge(h,h))

def test_pmatching():
    g = GraphO()
    n1 = g.add_node()
    n2 = g.add_node()
    n3 = g.add_node()
    n4 = g.add_node()
    n5 = g.add_node()
    n6 = g.add_node()
    e1 = g.add_edge(n1, n2)
    e1 = g.add_edge(n1, n2)
    e1 = g.add_edge(n2, n1)
    e1 = g.add_edge(n2, n1)
    e2 = g.add_edge(n3, n5)
    e3 = g.add_edge(n6, n6)

    print(g.pat())

    for l in Graph.pattern_match(g,g):
        print(str(l))

def test_pmatching2():
    g1 = GraphO()
    n1 = g1.add_node()
    n2 = g1.add_node()
    n3 = g1.add_node()
    e1 = g1.add_edge(n1,n2)

    g2 = GraphO()
    n4 = g2.add_node()
    n5 = g2.add_node()
    n6 = g2.add_node()
    n7 = g2.add_node()
    n8 = g2.add_node()
    n9 = g2.add_node()
    e2 = g2.add_edge(n5,n6)
    e2 = g2.add_edge(n5,n6)
    e2 = g2.add_edge(n5,n6)
    e3 = g2.add_edge(n4,n7)

    h = GraphM(g1,g2,{
        n1: n5,
        n2: n6,
        n3: n4,
        e1: e2
    })

    print(h.pattern())

    for l in Graph.pattern_match(h,h):
        print(str(l))

def test_pmatching3():
    p1 = GraphO()
    p1n1 = p1.add_node()
    p1n2 = p1.add_node()
    p1e12 = p1.add_edge(p1n1,p1n2)

    p2 = GraphO()
    p2n1 = p2.add_node()
    p2n2 = p2.add_node()
    p2n3 = p2.add_node()
    p2e12 = p2.add_edge(p2n1,p2n2)
    p2e23 = p2.add_edge(p2n2,p2n3)
    p2e31 = p2.add_edge(p2n3,p2n1)

    g = GraphO()
    g.add_node()
    g.add_node()
    g.add_node()
    g.add_node()
    g.add_node()
    g.add_node()
    g.add_node()
    g.add_node()
    g.add_node()
    g.add_node()
    gn1 = g.add_node()
    gn2 = g.add_node()
    gn3 = g.add_node()
    ge12 = g.add_edge(gn1,gn2)
    ge23 = g.add_edge(gn2,gn3)
    ge31 = g.add_edge(gn3,gn1)

    print(g)

    i = GraphM(p1,p2,{
        p1n1: p2n1,
        p1n2: p2n2,
        p1e12: p2e12
    })

    print(i)

    b1 = GraphM(p1,g,{
        p1n1: gn1,
        p1n2: gn2,
        p1e12: ge12
    })

    b2 = GraphM(p1,g,{
        p1n1: gn2,
        p1n2: gn3,
        p1e12: ge23
    })

    print(b1)
    print(b2)

    for m in list(Graph.pattern_match(i,b1)):
        print(m)

    for m in list(Graph.pattern_match(i,b2)):
        print(m)

if __name__ == "__main__":
    # test_merge()
    # test_pmatching()
    # test_pmatching2()
    test_multi_merge()
