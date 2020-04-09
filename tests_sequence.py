from Sequence import Sequence, SequenceO, SequenceM, NkSeqO, NkSeqM

def test():
    # test = ['b', 'o', 'n', 'j', 'o', 'n', 'r']
    # pat =  ['o', 'n']
    # for i in Sequence.pattern_match(SequenceO(pat), SequenceO(test)):
    #     print(i.i)
    #     r1 = i

    # patdest = ['n', 'j', 'o', 'n', 'r']
    # for i in Sequence.pattern_match(SequenceO(pat), SequenceO(patdest)):
    #     print(i.i)
    #     r2 = i

    # for i in Sequence.pattern_match(r2, r1):
    #     print(i.i)

    # merge1 = ['e', 'y', 'l', 'e'] #, 'a', 'l', 'e', 'x']
    # merge2 = ['h', 'e', 'y', 'l', 'e', 'a']
    # mergeon = ['l', 'e']
    # m1 = SequenceM(SequenceO(mergeon), SequenceO(merge1), 2)
    # m2 = SequenceM(SequenceO(mergeon), SequenceO(merge2), 3)

    # t = Sequence.merge(m2, m1)
    # print(t)

    # print(merge1)
    # print(merge2)
    # print(mergeon)
    # t = Sequence.merge_2_in_1(m2, m1)
    # print(t)

    # for i in Sequence.pattern_match_fam((2, 4, 2), m2):
    #     print(i)

    # for i in Sequence.pattern_match_fam(0, SequenceO(test)):
    #     print(i)

    import PFunctor
    import GT

    pfm = PFunctor.FamPFunctor.Maker(Sequence, Sequence)

    l0 = NkSeqO(0)
    r0 = lambda x : x

    g0 = pfm.add_fam_rule(l0, r0)

    l1 = NkSeqO(1)
    r1 = lambda x : SequenceO(['a', 'b']) if x.s == ['a'] else SequenceO(['a'])

    g1 = pfm.add_fam_rule(l1, r1)

    def rhs0(lps, lpo, rs, ro):
        return SequenceM(rs, ro, 0)

    def rhs1(lps, lpo, rs, ro):
        if ro.s == ['a', 'b']:
            return SequenceM(rs, ro, 2)
        elif ro.s == ['a']:
            return SequenceM(rs, ro, 1)

    _, _, inc1 = pfm.add_fam_inclusion(g0, g1, NkSeqM(NkSeqO(0), NkSeqO(1), 0), rhs0)
    # print(">>> inc1 lhs", inc1.lhs)
    pfm.add_fam_inclusion(g0, g1, NkSeqM(NkSeqO(0), NkSeqO(1), 1), rhs1)

    pf = pfm.get()

    T = GT.GT(pf)

    g = SequenceO(['a'])
    # print(g)
    for i in range(0, 2):
        gr = T.extend(g)
        assert len(gr) == 1
        g = list(gr)[0].object
        print(g)

    pfm = PFunctor.FamPFunctor.Maker(Sequence, Sequence)

    l1 = NkSeqO(1)
    r1 = lambda x : x

    g1 = pfm.add_fam_rule(l1, r1)

    l2 = NkSeqO(2)
    r2 = lambda x : SequenceO([x.s[0], (x.s[0] + x.s[1])/2, x.s[1]])

    g2 = pfm.add_fam_rule(l2, r2)

    def rhs120(lps, lpo, rs, ro):
        return SequenceM(rs, ro, 0)

    def rhs122(lps, lpo, rs, ro):
        return SequenceM(rs, ro, 2)

    pfm.add_fam_inclusion(g1, g2, NkSeqM(NkSeqO(1), NkSeqO(2), 0), rhs120)
    pfm.add_fam_inclusion(g1, g2, NkSeqM(NkSeqO(1), NkSeqO(2), 1), rhs122)

    pf = pfm.get()

    T = GT.GT(pf)

    g = SequenceO([0, 5, 0, 5])
    print(g)
    for i in range(0, 3):
        gr = T.extend(g)
        assert len(gr) == 1
        g = list(gr)[0].object
        print(g)



from random import random

def test2():
    from DataStructure import Lazy
    LSequence = Lazy(Sequence)
    def s1exp():
        return (SequenceO(['a','a']), []) if random() <= 0.5  else (SequenceO(['a']), [])
    s1 = LSequence.TO()(s1exp)

    def s2exp():
        return (SequenceO(['b','b']), []) if random() <= 0.5  else (SequenceO(['b']), [])
    s2 = LSequence.TO()(s2exp)

    def s3exp(s1,s2):
        ret = SequenceO(s1.s + s2.s)
        return (ret, [ SequenceM(s1,ret,0) , SequenceM(s2,ret,len(s1.s)) ])
    s3 = LSequence.TO()(s3exp)
    h13 = s3.setSubobject(0,s1)
    h23 = s3.setSubobject(1,s2)

    def s4exp(s3):
        ret = SequenceO(['c'] + s3.s + ['c'])
        return (ret, [ SequenceM(s3,ret,1) ])
    s4 = LSequence.TO()(s4exp)
    h34 = s4.setSubobject(0,s3)

    h = h13.compose(h34)

    print(h.force())


def test3():
    from PFunctor import ExpPFunctor
    from GT import GT
    from DataStructure import Lazy
    LSequence = Lazy(Sequence)

    epf = ExpPFunctor.Maker(Sequence, LSequence)

    l_a = SequenceO(['a'])
    def er_a():
        return (SequenceO(['a','a']), []) if random() <= 0.5  else (SequenceO(['a']), [])
    g_a = epf.add_exp_rule(l_a, er_a)

    l_aa = SequenceO(['a','a'])
    def er_aa(s1,s2):
        ret = SequenceO(s1.s + s2.s)
        return (ret, [ SequenceM(s1,ret,0) , SequenceM(s2,ret,len(s1.s)) ])
    g_aa = epf.add_exp_rule(l_aa, er_aa)

    l_a_aa_0 = SequenceM(l_a,l_aa,0)
    ir_a_aa_0 = 0
    g_a_aa_0 = epf.add_exp_inclusion(g_a, g_aa, l_a_aa_0, ir_a_aa_0)

    l_a_aa_1 = SequenceM(l_a,l_aa,1)
    ir_a_aa_1 = 1
    g_a_aa_1 = epf.add_exp_inclusion(g_a, g_aa, l_a_aa_1, ir_a_aa_1)

    epf = epf.get()

    T = GT(epf)

    sz = {}
    for i in range(0,100):
        s = len(tuple(T.extend(SequenceO(['a','a','a'])))[0].object)
        sz[s] = sz.setdefault(s,0) + 1
    print({s: 8*n/100 for (s,n) in sz.items() })
    print((tuple(T.extend(SequenceO(['a','a','a'])))[0].object))

def test4():
    from PFunctor import FamExpPFunctor
    from GT import GT
    from DataStructure import Lazy
    LSequence = Lazy(Sequence)

    epf = FamExpPFunctor.Maker(Sequence, LSequence)

    l_a = SequenceO(['a'])
    def er_a(lp):
        def er_a_exp():
            return (SequenceO(['a','a']), [], []) if random() <= 0.5  else (SequenceO(['a']), [], [])
        return er_a_exp
    g_a = epf.add_fam_exp_rule(l_a, er_a, 0)

    l_aa = SequenceO(['a','a'])
    def er_aa(lp):
        def er_aa_exp(s1,s2):
            ret = SequenceO(s1.s + s2.s)
            return (ret, [ SequenceM(s1,ret,0) , SequenceM(s2,ret,len(s1.s))], [SequenceM(ret, ret, 0)])
        return er_aa_exp
    g_aa = epf.add_fam_exp_rule(l_aa, er_aa, 1)

    l_a_aa_0 = SequenceM(l_a,l_aa,0)
    ir_a_aa_0 = 0
    g_a_aa_0 = epf.add_fam_exp_inclusion(g_a, g_aa, l_a_aa_0, ir_a_aa_0)

    l_a_aa_1 = SequenceM(l_a,l_aa,1)
    ir_a_aa_1 = 1
    g_a_aa_1 = epf.add_fam_exp_inclusion(g_a, g_aa, l_a_aa_1, ir_a_aa_1)

    l_aa_aa = SequenceM(l_aa, l_aa, 0)
    ir_aa_aa = 0
    g_aa_aa = epf.add_fam_exp_inclusion(g_aa, g_aa, l_aa_aa, ir_aa_aa)

    epf = epf.get()

    T = GT(epf)

    sz = {}
    for i in range(0,100):
        s = len(tuple(T.extend(SequenceO(['a','a','a'])))[0].object)
        sz[s] = sz.setdefault(s,0) + 1
    print({s: 8*n/100 for (s,n) in sz.items() })
    print((tuple(T.extend(SequenceO(['a','a','a'])))[0].object))

if __name__ == "__main__":
    test()
    # test3()
    print("-------------------------------------------------------------END1")
    # test4()

# g1 = ExprRule(['a'], lambda self: ['a', 'a'] if random() > 0.5 else ['a'])
# 
# g2 = ExprRule(['a', 'a'], lambda self : self.inc[i].dom.obj + self.inc[j].dom.obj)
# 
# g2.inc[i] = ExprInclusion(g1, g2, 0, lambda self : 0)
# g2.inc[j] = ExprInclusion(g1, g2, 1, lambda self : len(self.cod.inc[i].dom.obj))

#
# let g1 =
#   a => a if random() else aa
#
# let g2 = 
#   aa => i * j
#
# and i: g1 -> g2 = 
#   (0: g1 -> g2) => (0: g1 -> g2)
#
# and j: g1 -> g2 = 
#   (1: a -> aa) => (len(i.dom): g1 -> g2)
# 
# 
# let g1 = a => b
# 
# and g2 = b => ab
# 
# and g3 = . => .
#
# and _: g3 -> g1 = 0 => 0
# 
# 