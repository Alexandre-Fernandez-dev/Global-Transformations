import copy

class GraphO:
    def __init__(self):
        self.n = 0
        self.e = {}

    def add_node(self):
        self.n+=1
        return self.n-1

    def add_edge(self, i, j):
        if max(i, j) >= self.n or min(i, j) < 0:
           raise Exception("Dangling edge")
        if i <= j:
            n_e = (i, j)
        else:
            n_e = (j, i)
        id = -len(self.e)-1
        self.e[id] = n_e
        return id

    def __repr__(self):
        return "{ " + str(self.n) + ", " + str(self.e) + " }";


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
    def __init__(self):
        self.generators = [GraphO(), GraphO()]
        self.generators[0].add_node()
        self.generators[1].add_node()
        self.generators[1].add_node()
        self.generators[1].add_edge(0, 1)

    def pattern_match(self, p, t):
        pass

    def merge(self, m1, m2):
        if m1.s != m2.s:
            raise Exception("Not same source")
        r = copy.deepcopy(m1.s)
        l1 = {}
        l2 = {}

        for i in range(0, r.n):
            l1[m1.l[i]] = i
            l2[m2.l[i]] = i

        for i in range(-1, -len(r.e)-1, -1):
            l1[m1.l[i]] = i
            l2[m2.l[i]] = i

        for i in range(-len(m1.t.e), m1.t.n):
            if i not in l1:
                if i >=0:
                    j = r.add_node()
                    l1[i] = j
                else:
                    i_from, i_to = m1.t.e[i]
                    if i_from not in l1:
                        j_from = r.add_node()
                        l1[i_from] = j_from
                    else:
                        j_from = l1[i_from]

                    if i_to not in l1:
                        j_to = r.add_node()
                        l1[i_to] = j_to
                    else:
                        j_to = l1[i_to]

                    l1[i] = r.add_edge(j_from, j_to)

        for i in range(-len(m2.t.e), m2.t.n):
            if i not in l2:
                if i >=0:
                    j = r.add_node()
                    l2[i] = j
                else:
                    i_from, i_to = m2.t.e[i]
                    if i_from not in l2:
                        j_from = r.add_node()
                        l2[i_from] = j_from
                    else:
                        j_from = l2[i_from]

                    if i_to not in l2:
                        j_to = r.add_node()
                        l2[i_to] = j_to
                    else:
                        j_to = l2[i_to]

                    l2[i] = r.add_edge(j_from, j_to)
        return r, GraphM(m1.t, r, l1), GraphM(m2.t, r, l2)

cat = Graph()

g = GraphO()
n1 = g.add_node()
n2 = g.add_node()
n3 = g.add_node()
e1 = g.add_edge(n1, n2)

print(g)

gl = GraphO()
o1 = gl.add_node()
o2 = gl.add_node()
o3 = gl.add_node()
o4 = gl.add_node()
f1 = gl.add_edge(o2, o3)
f2 = gl.add_edge(o1, o4)

print(gl)

m = GraphM(g, gl, {})
m.l[n1] = o2
m.l[n2] = o3
m.l[n3] = o1
m.l[e1] = f1

print(m)

print(cat.merge(m, m))

