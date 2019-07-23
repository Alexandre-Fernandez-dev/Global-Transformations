import math
import networkx as nx

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
        return self.pr() + " => " + str(self.next)

class HeadNodePattern(ContPattern):
    def __init__(self, i):
        ContPattern.__init__(self)
        self.i = i

    def match(self, ctx):
        for i in ctx.g.nodes:
            if ctx.is_cursed(i): continue
            ctx.curse(i)
            ctx.l[self.i] = i
            # self.next.match(ctx)
            for l in self.next.match(ctx): yield l
            ctx.uncurse(i)

    def pr(self):
        return 'HN(' + str(self.i) + ')'


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
        # self.next.match(ctx)
        for l in self.next.match(ctx): yield l

    def pr(self):
        return 'CL(' + str(self.i) + ' - ' + str(self.nii) + ')'

class HeadLoopPattern(LoopPattern):
    def __init__(self, i, nii):
        LoopPattern.__init__(self,i,nii)

    def match(self, ctx):
        for i in ctx.g.nodes:
            if ctx.is_cursed(i): continue
            nii = ctx.g.g.number_of_edges(i,i)
            if nii < self.nii:
                continue
            ctx.curse(i)
            ctx.l[self.i] = i
            # self.next.match(ctx)
            for l in self.next.match(ctx): yield l
            ctx.uncurse(i)

    def pr(self):
        return 'HL(' + str(self.i) + ' - ' + str(self.nii) + ')'

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
                nij = ctx.g.g.number_of_edges(i,j)
                nji = ctx.g.g.number_of_edges(j,i)
                if nij < self.nij or nji < self.nji:
                    continue
                ctx.curse(j)
                ctx.l[self.i] = i
                ctx.l[self.j] = j
                # self.next.match(ctx)
                for l in self.next.match(ctx): yield l
                ctx.uncurse(j)
            ctx.uncurse(i)

    def pr(self):
        return 'HP(' + str(self.i) + ' -> ' + str(self.j) + ', ' + str(self.nij) + ' / ' + str(self.nji) + ')'

class OutgoingPairPattern(PairPattern):
    def __init__(self, i, j, nij, nji):
        PairPattern.__init__(self,i,j,nij,nji)

    def match(self, ctx):
        i = ctx.l[self.i]
        for j in ctx.g.g.successors(i) if self.nij > 0 else ctx.g.g.predecessors(i):
            if ctx.is_cursed(j): continue
            if ctx.g.g.number_of_edges(i,j) < self.nij or ctx.g.g.number_of_edges(j,i) < self.nji:
                continue
            ctx.curse(j)
            ctx.l[self.j] = j
            # self.next.match(ctx)
            for l in self.next.match(ctx): yield l
            ctx.uncurse(j)

    def pr(self):
        return 'OP(' + str(self.i) + ' -> ' + str(self.j) + ', ' + str(self.nij) + ' / ' + str(self.nji) + ')'


class IncomingPairPattern(PairPattern):
    def __init__(self, i, j, nij, nji):
        PairPattern.__init__(self,i,j,nij,nji)

    def match(self, ctx):
        j = ctx.l[self.j]
        for i in ctx.g.g.predecessors(j) if self.nij > 0 else ctx.g.g.successors(j):
            if ctx.is_cursed(i): continue
            if ctx.g.g.number_of_edges(i,j) < self.nij or ctx.g.g.number_of_edges(j,i) < self.nji:
                continue
            ctx.curse(i)
            ctx.l[self.i] = i
            # self.next.match(ctx)
            for l in self.next.match(ctx): yield l
            ctx.uncurse(i)

    def pr(self):
        return 'IP(' + str(self.i) + ' -> ' + str(self.j) + ', ' + str(self.nij) + ' / ' + str(self.nji) + ')'

class CheckPairPattern(PairPattern):
    def __init__(self, i, j, nij, nji):
        PairPattern.__init__(self,i,j,nij,nji)

    def match(self, ctx):
        i = ctx.l[self.i]
        j = ctx.l[self.j]
        if ctx.g.g.number_of_edges(i,j) < self.nij or ctx.g.g.number_of_edges(j,i) < self.nji:
            raise StopIteration
        # self.next.match(ctx)
        for l in self.next.match(ctx): yield l

    def pr(self):
        return 'CP(' + str(self.i) + ' -> ' + str(self.j) + ', ' + str(self.nij) + ' / ' + str(self.nji) + ')'

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
            # self.next.match(ctx)
            for ll in self.next.match(ctx): yield ll

    def pr(self):
        return 'E(' + str(self.i) + ' => ' + str(self.j) + ')'

class GraphO():
    def __init__(self, g = None):
        if g == None:
            self.g = nx.MultiDiGraph()
        else:
            self.g = g
        self.pattern = None

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
        if self.pattern != None:
            return self.pattern

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

        #print(str(dep.nodes))
        #print(str(dep.edges(data=True)))

        ed = nx.algorithms.tree.branchings.Edmonds(dep)
        B = ed.find_optimum('weight', 1, kind='min', style='arborescence')
        #B = nx.algorithms.tree.branchings.greedy_branching(dep)
        #print(nx.algorithms.tree.branchings.branching_weight(B))
        #print(B.nodes)
        #print(B.edges)
        C = nx.algorithms.dag.topological_sort(B)

        startpat = ContPattern()
        endpat = EndPattern()

        def unique_pred(B,i):
            for j in B.predecessors(i):
                return j

        l = set()
        for i in C:
            #print(str(i))
            if i == 'r00t': continue
            p = unique_pred(B,i)

            pat = ContPattern()
            if p == 'r00t':
                if type(i) == int:
                    #print("Head Node")
                    pat = HeadNodePattern(i)
                    l.add(i)
                elif i[0] == i[1]:
                    #print("Head Loop")
                    pat = HeadLoopPattern(i[0],i[2])
                    endpat = EdgePattern(i[0],i[0],i[2]).then(endpat)
                    l.add(i[0])
                else:
                    #print("Head Pair")
                    pat = HeadPairPattern(i[0],i[1],i[2][0],i[2][1])
                    endpat = EdgePattern(i[0],i[1],i[2][0]).then(endpat)
                    endpat = EdgePattern(i[1],i[0],i[2][1]).then(endpat)
                    l.add(i[0])
                    l.add(i[1])
            elif type(i) == int:
                continue
            else:
                (i,j,s) = i
                if i == j:
                    #print("Check Loop")
                    pat = CheckLoopPattern(i,s)
                    endpat = EdgePattern(i,i,s).then(endpat)
                else:
                    if i in l:
                        if j in l:
                            #print("Check Pair")
                            pat = CheckPairPattern(i,j,s[0],s[1])
                        else:
                            #print("Outgoing Pair")
                            pat = OutgoingPairPattern(i,j,s[0],s[1])
                            l.add(j)
                    else:
                        if j in l:
                            #print("Incoming Pair")
                            pat = IncomingPairPattern(i,j,s[0],s[1])
                            l.add(i)
                        else:
                            #print("WTF")
                            continue
                    endpat = EdgePattern(i,j,s[0]).then(endpat)
                    endpat = EdgePattern(j,i,s[1]).then(endpat)
            startpat = startpat.then(pat)

        self.pattern = startpat.then(endpat).next
        return self.pattern


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
        pat = p.pat()
        ctx = Graph.Ctx(g)
        for l in pat.match(ctx):
            yield l

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


g = GraphO()
n1 = g.add_node()
n2 = g.add_node()
n3 = g.add_node()
n4 = g.add_node()
e1 = g.add_edge(n1, n2)
e1 = g.add_edge(n1, n2)
e1 = g.add_edge(n2, n1)
e1 = g.add_edge(n2, n1)
#e1 = g.add_edge(n3, n1)
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


for l in Graph.pattern_match(g,g):
    print(str(l))

import sys
sys.exit(0)
