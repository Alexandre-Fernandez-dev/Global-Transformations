import sys
from pathlib import Path

current_dir = Path(__file__).parent.absolute()
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir)) 

from src.libgt.data.Integer import Integer, IntegerM
from src.libgt.engine.PFunctor import FlatPFunctor
from src.libgt.engine.GT import GT

def pattern_match():

    for m in Integer.pattern_match(1342, 3456):
        print(m)

    for m in Integer.pattern_match(1342, 346):
        print(m)


    # pfTm = FlatPFunctor.Maker(Sequence, Sequence)

    # l0 = SequenceO([])
    # r0 = l0

    # g0 = pfTm.add_rule(l0,r0)

    # l1 = SequenceO(['a'])
    # r1 = SequenceO(['a', 'b'])

    # g1 = pfTm.add_rule(l1,r1)

    # l2 = SequenceO(['b'])
    # r2 = SequenceO(['a'])

    # g2 = pfTm.add_rule(l2,r2)

    # incl01a = SequenceM(l0, l1, 0)
    # incr01a = SequenceM(r0, r1, 0)

    # inc01a = pfTm.add_inclusion(g0,g1,incl01a,incr01a)


    # incl01b = SequenceM(l0, l1, 1)
    # incr01b = SequenceM(r0, r1, 2)

    # inc01b = pfTm.add_inclusion(g0,g1,incl01b,incr01b)

    # incl02a = SequenceM(l0, l2, 0)
    # incr02a = SequenceM(r0, r2, 0)

    # inc02a = pfTm.add_inclusion(g0,g2,incl02a,incr02a)


    # incl02b = SequenceM(l0, l2, 1)
    # incr02b = SequenceM(r0, r2, 1)

    # inc02b = pfTm.add_inclusion(g0,g2,incl02b,incr02b)

    # s = SequenceO('a')
    # pfT = pfTm.get()
    # T = GT(pfT)
    # for i in range(0, 3):
    #     s = T.extend(s)
    #     print("i =", i+1)
    #     print(s)

if __name__ == "__main__":
    pattern_match()
