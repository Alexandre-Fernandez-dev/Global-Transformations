import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

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
    g_aa = epf.add_fam_exp_rule(l_aa, er_aa, 0)

    l_a_aa_0 = SequenceM(l_a,l_aa,0)
    ir_a_aa_0 = 0
    g_a_aa_0 = epf.add_fam_exp_inclusion(g_a, g_aa, l_a_aa_0, ir_a_aa_0)

    l_a_aa_1 = SequenceM(l_a,l_aa,1)
    ir_a_aa_1 = 1
    g_a_aa_1 = epf.add_fam_exp_inclusion(g_a, g_aa, l_a_aa_1, ir_a_aa_1)

    # l_aa_aa = SequenceM(l_aa, l_aa, 0)
    # ir_aa_aa = 0
    # g_aa_aa = epf.add_fam_exp_inclusion(g_aa, g_aa, l_aa_aa, ir_aa_aa)

    epf = epf.get()

    T = GT(epf)

    sz = {}
    for i in range(0,100):
        s = len(tuple(T.extend(SequenceO(['a','a','a'])))[0].object)
        sz[s] = sz.setdefault(s,0) + 1
    print({s: 8*n/100 for (s,n) in sz.items() })
    print((tuple(T.extend(SequenceO(['a','a','a'])))[0].object))

def test5():
    from GT_DU import GT_DU
    from PFunctor import OPFunctor

    fpfm = OPFunctor.Maker(Sequence, Sequence)
    Choices = OPFunctor.Choices
    
    l0 = SequenceO([])
    r0 = SequenceO([])

    r0C = Choices(l0, [r0])

    l1 = SequenceO(['a'])
    r1 = SequenceO(['a', 'b'])

    r1C = Choices(l1, [r1])

    il01a = SequenceM(l0, l1, 0)
    ir01a = SequenceM(r0, r1, 0)

    il01b = SequenceM(l0, l1, 1)
    ir01b = SequenceM(r0, r1, 2)

    r1C.add_under_choice(il01a, r0C, [ir01a])
    r1C.add_under_choice(il01b, r0C, [ir01b])
    
    l2 = SequenceO(['b'])
    r2 = SequenceO(['a'])

    r2C = Choices(l2, [r2])

    il02a = SequenceM(l0, l2, 0)
    ir02a = SequenceM(r0, r2, 0)

    il02b = SequenceM(l0, l2, 1)
    ir02b = SequenceM(r0, r2, 1)

    r2C.add_under_choice(il02a, r0C, [ir02a])
    r2C.add_under_choice(il02b, r0C, [ir02b])

    g0 = fpfm.add_o_rule(l0, r0C, lambda c, incs : r0)

    g1 = fpfm.add_o_rule(l1, r1C, lambda c, incs : r1)

    fpfm.add_o_inclusion(g0, g1, il01a)
    fpfm.add_o_inclusion(g0, g1, il01b)

    g2 = fpfm.add_o_rule(l2, r2C, lambda c, incs : r2)

    fpfm.add_o_inclusion(g0, g2, il02a)
    fpfm.add_o_inclusion(g0, g2, il02b)

    fpf = fpfm.get()

    T = GT_DU(fpf)
    
    s = SequenceO(['a'])
    
    for i in range(0, 3):
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        sp = T.extend(s)
        print(len(sp))
        s = tuple(sp)[0].object
        print(s)
        
def test6():
    from GT_DU import GT_DU
    from PFunctor import OPFunctor

    fpfm = OPFunctor.Maker(Sequence, Sequence)
    Choices = OPFunctor.Choices
    
    l0 = SequenceO([])
    r0 = SequenceO([])

    r0C = Choices(l0, [r0])

    l1 = SequenceO(['a'])
    r1a = SequenceO(['a', 'b'])
    r1b = SequenceO(['a'])

    r1C = Choices(l1, [r1a, r1b])

    il01_0 = SequenceM(l0, l1, 0)
    ir01_0a = SequenceM(r0, r1a, 0)
    ir01_0b = SequenceM(r0, r1b, 0)

    il01_1 = SequenceM(l0, l1, 1)
    ir01_1a = SequenceM(r0, r1a, 2)
    ir01_1b = SequenceM(r0, r1b, 1)

    r1C.add_under_choice(il01_0, r0C, [ir01_0a, ir01_0b])
    r1C.add_under_choice(il01_1, r0C, [ir01_1a, ir01_1b])
    
    l2 = SequenceO(['b'])
    r2 = SequenceO(['a'])

    r2C = Choices(l2, [r2])

    il02_0 = SequenceM(l0, l2, 0)
    ir02_0 = SequenceM(r0, r2, 0)

    il02_1 = SequenceM(l0, l2, 1)
    ir02_1 = SequenceM(r0, r2, 1)

    r2C.add_under_choice(il02_0, r0C, [ir02_0])
    r2C.add_under_choice(il02_1, r0C, [ir02_1])

    g0 = fpfm.add_o_rule(l0, r0C, lambda c, incs : r0)

    g1 = fpfm.add_o_rule(l1, r1C, lambda c, incs : r1a if random() > 0.5 else r1b)

    fpfm.add_o_inclusion(g0, g1, il01_0)
    fpfm.add_o_inclusion(g0, g1, il01_1)

    g2 = fpfm.add_o_rule(l2, r2C, lambda c, incs : r2)

    fpfm.add_o_inclusion(g0, g2, il02_0)
    fpfm.add_o_inclusion(g0, g2, il02_1)

    fpf = fpfm.get()

    T = GT_DU(fpf)
    
    s = SequenceO(['a'])
    
    for i in range(0, 10):
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        sp = T.extend(s)
        print(len(sp))
        s = tuple(sp)[0].object
        print(s)

def test7():
    from GT_DU_2 import FlatPFunctor, GT_DU
    pfTm = FlatPFunctor.Maker(Sequence, Sequence)

    l0 = SequenceO([])
    r0 = l0

    g0 = pfTm.add_rule(l0,r0)

    l1 = SequenceO(['a'])
    r1 = SequenceO(['a', 'b'])

    g1 = pfTm.add_rule(l1,r1)

    l2 = SequenceO(['b'])
    r2 = SequenceO(['a'])

    g2 = pfTm.add_rule(l2,r2)

    incl01a = SequenceM(l0, l1, 0)
    incr01a = SequenceM(r0, r1, 0)

    inc01a = pfTm.add_inclusion(g0,g1,incl01a,incr01a)


    incl01b = SequenceM(l0, l1, 1)
    incr01b = SequenceM(r0, r1, 2)

    inc01b = pfTm.add_inclusion(g0,g1,incl01b,incr01b)

    incl02a = SequenceM(l0, l2, 0)
    incr02a = SequenceM(r0, r2, 0)

    inc02a = pfTm.add_inclusion(g0,g2,incl02a,incr02a)


    incl02b = SequenceM(l0, l2, 1)
    incr02b = SequenceM(r0, r2, 1)

    inc02b = pfTm.add_inclusion(g0,g2,incl02b,incr02b)

    s = SequenceO('a')
    pfT = pfTm.get()
    T = GT_DU(pfT)
    for i in range(0, 3):
        s = tuple(T.extend(s))[0].object
        print(s)

if __name__ == "__main__":
    # test()
    # test3()
    print("-------------------------------------------------------------END1")
    test7()

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