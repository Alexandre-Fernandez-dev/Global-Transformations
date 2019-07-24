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
nr1ab = r1.add_node()
nr1b = r1.add_node()
er1aab = r1.add_edge(nr1a,nr1ab)
er1abb = r1.add_edge(nr1ab,nr1b)

g1 = T.add_rule(l1,r1)

l2 = GraphO()
nl2a = l2.add_node()
nl2b = l2.add_node()
nl2c = l2.add_node()
el2ab = l2.add_edge(nl2a,nl2b)
el2bc = l2.add_edge(nl2b,nl2c)
el2ca = l2.add_edge(nl2c,nl2a)
r2 = GraphO()
nr2a = r2.add_node()
nr2ab = r2.add_node()
nr2b = r2.add_node()
nr2bc = r2.add_node()
nr2c = r2.add_node()
nr2ca = r2.add_node()
er2aab = r2.add_edge(nr2a,nr2ab)
er2abb = r2.add_edge(nr2ab,nr2b)
er2bbc = r2.add_edge(nr2b,nr2bc)
er2bcc = r2.add_edge(nr2bc,nr2c)
er2cca = r2.add_edge(nr2c,nr2ca)
er2caa = r2.add_edge(nr2ca,nr2a)
er2abca = r2.add_edge(nr2ab,nr2ca)
er2cabc = r2.add_edge(nr2ca,nr2bc)
er2bcab = r2.add_edge(nr2bc,nr2ab)

g2 = T.add_rule(l2,r2)


incl01a = GraphM(l0,l1,{
    nl0: nl1a
})
incr01a = GraphM(r0,r1,{
    nr0: nr1a
})

inc01a = T.add_inclusion(g0,g1,incl01a,incr01a)


incl01b = GraphM(l0,l1,{
    nl0: nl1b
})
incr01b = GraphM(r0,r1,{
    nr0: nr1b
})

inc01b = T.add_inclusion(g0,g1,incl01b,incr01b)

incl22a = GraphM(l2,l2,{
    nl2a: nl2b,
    nl2b: nl2c,
    nl2c: nl2a,
    el2ab: el2bc,
    el2bc: el2ca,
    el2ca: el2ab,
})
incr22a = GraphM(r2,r2,{
    nr2a:nr2b,
    nr2ab:nr2bc,
    nr2b:nr2c,
    nr2bc:nr2ca,
    nr2c:nr2a,
    nr2ca:nr2ab,
    er2aab:er2bbc,
    er2abb:er2bcc,
    er2bbc:er2cca,
    er2bcc:er2caa,
    er2cca:er2aab,
    er2caa:er2abb,
    er2abca:er2bcab,
    er2cabc:er2abca,
    er2bcab:er2cabc
})

inc22a = T.add_inclusion(g2,g2,incl22a,incr22a)
inc22b = T.add_inclusion(g2,g2,incl22a.compose(incl22a),incr22a.compose(incr22a))

print(incr22a.compose(incr22a).compose(incr22a))
print()

incl12a = GraphM(l1,l2,{
    nl1a: nl2a,
    nl1b: nl2b,
    el1ab: el2ab
})
incr12a = GraphM(r1,r2,{
    nr1a: nr2a,
    nr1ab: nr2ab,
    nr1b: nr2b,
    er1aab: er2aab,
    er1abb: er2abb
})

inc12a = T.add_inclusion(g1,g2,incl12a,incr12a)
inc12b = T.add_inclusion(g1,g2,incl12a.compose(incl22a),incr12a.compose(incr22a))
inc12b = T.add_inclusion(g1,g2,incl12a.compose(incl22a).compose(incl22a),incr12a.compose(incr22a).compose(incr22a))

print(T.G.nodes())
print(T.G.edges(keys=True))

print()

g = GraphO()
n1 = g.add_node()
n2 = g.add_node()
n3 = g.add_node()
e12 = g.add_edge(n1,n2)
e23 = g.add_edge(n2,n3)
e31 = g.add_edge(n3,n1)

T.apply(g)

import sys
sys.exit(0)

inc01b = T.add_inclusion(g0,g1,incl01b,incr01b)




















#
