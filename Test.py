from Graph import *
from GT import *

T = GT(Graph)

l0 = GraphO()
nl0 = l0.add_node()
r0 = l0
nr0 = nl0

g0 = T.add_rule(l0,r0)

l1 = GraphO()
nl1a = l1.add_node()
nl1b = l1.add_node()
el1ab = l1.add_edge(nl1a,nl1b)
r1 = GraphO()
nr1a = r1.add_node()
nr1b = r1.add_node()
nr1c = r1.add_node()
er1ab = r1.add_edge(nr1a,nr1b)
er1bc = r1.add_edge(nr1b,nr1c)

g1 = T.add_rule(l1,r1)

incl01a = GraphM(l0,l1,{})
incl01a.l[nl0] = nl1a
incr01a = GraphM(r0,r1,{})
incr01a.l[nr0] = nr1a

incl01b = GraphM(l0,l1,{})
incl01b.l[nl0] = nl1b
incr01b = GraphM(r0,r1,{})
incr01b.l[nr0] = nr1c

inc01a = T.add_inclusion(g0,g1,incl01a,incr01a)
inc01b = T.add_inclusion(g0,g1,incl01b,incr01b)

print(T.G.nodes(data=True))
print(T.G.edges(data=True))

g = GraphO()
n1 = g.add_node()
n2 = g.add_node()
n3 = g.add_node()
e12 = g.add_edge(n1,n2)
e21 = g.add_edge(n2,n1)
e23 = g.add_edge(n2,n3)
e31 = g.add_edge(n3,n1)

T.apply(g)

import sys
sys.exit(0)

inc01b = T.add_inclusion(g0,g1,incl01b,incr01b)
