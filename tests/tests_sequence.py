import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from src.data.Sequence import Sequence, SequenceO, SequenceM, NkSeqO, NkSeqM

def D0L():
    from src.engine.PFunctor import FlatPFunctor
    from src.engine.GT import GT
    from src.data.Sequence import Sequence, SequenceM, SequenceO
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
    T = GT(pfT)
    for i in range(0, 3):
        s = T.extend(s).object
        print(s)

if __name__ == "__main__":
    D0L()

# Here I keep old tests that needs to be adapted
def old():
    def test():
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
