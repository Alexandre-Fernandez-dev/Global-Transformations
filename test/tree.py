import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from src.libgt.data.Sequence import Sequence, SequenceO, SequenceM
from src.libgt.data.Tree import Tree, TreeLeaf, TreeNode, TreeM
from src.libgt.engine.PFunctor import FlatPFunctor
from src.libgt.engine.GT import GT

def identity():
    pfTm = FlatPFunctor.Maker(Tree, Tree)

    l0 = None
    r0 = None

    g0 = pfTm.add_rule(l0,r0)

    l1 = TreeLeaf()
    r1 = TreeLeaf()

    g1 = pfTm.add_rule(l1,r1)

    l2 = TreeNode(None, None)
    r2 = TreeNode(None, None)

    g2 = pfTm.add_rule(l2,r2)

    incl01 = TreeM(l0, l1, [])
    incr01 = TreeM(r0, r1, [])

    inc01 = pfTm.add_inclusion(g0,g1,incl01,incr01)


    incl02a = TreeM(l0, l2, [])
    incr02a = TreeM(r0, r2, [])

    inc02a = pfTm.add_inclusion(g0,g2,incl02a,incr02a)

    incl02b = TreeM(l0, l2, [TreeM.Left])
    incr02b = TreeM(r0, r2, [TreeM.Left])

    inc02b = pfTm.add_inclusion(g0,g2,incl02b,incr02b)

    incl02c = TreeM(l0, l2, [TreeM.Right])
    incr02c = TreeM(r0, r2, [TreeM.Right])

    inc02c = pfTm.add_inclusion(g0,g2,incl02c,incr02c)

    s = TreeNode(TreeLeaf(),TreeNode(None, TreeLeaf()))
    pfT = pfTm.get()
    T = GT(pfT)
    s = T.extend(s)
    print(s)


def mirror():

    pfTm = FlatPFunctor.Maker(Tree, Tree)

    l0 = None
    r0 = None

    g0 = pfTm.add_rule(l0,r0)

    l1 = TreeLeaf()
    r1 = TreeLeaf()

    g1 = pfTm.add_rule(l1,r1)

    l2 = TreeNode(None, None)
    r2 = TreeNode(None, None)

    g2 = pfTm.add_rule(l2,r2)

    incl01 = TreeM(l0, l1, [])
    incr01 = TreeM(r0, r1, [])

    inc01 = pfTm.add_inclusion(g0,g1,incl01,incr01)


    incl02a = TreeM(l0, l2, [])
    incr02a = TreeM(r0, r2, [])

    inc02a = pfTm.add_inclusion(g0,g2,incl02a,incr02a)

    incl02b = TreeM(l0, l2, [TreeM.Left])
    incr02b = TreeM(r0, r2, [TreeM.Right])

    inc02b = pfTm.add_inclusion(g0,g2,incl02b,incr02b)

    incl02c = TreeM(l0, l2, [TreeM.Right])
    incr02c = TreeM(r0, r2, [TreeM.Left])

    inc02c = pfTm.add_inclusion(g0,g2,incl02c,incr02c)

    s = TreeNode(TreeLeaf(),TreeNode(None, TreeLeaf()))
    pfT = pfTm.get()
    T = GT(pfT)
    s = T.extend(s)
    print(s)

def height_as_a_word():
    pfTm = FlatPFunctor.Maker(Tree, Sequence())

    l0 = None
    r0 = SequenceO([1])

    g0 = pfTm.add_rule(l0,r0)

    l1 = TreeLeaf()
    r1 = SequenceO([1])

    g1 = pfTm.add_rule(l1,r1)

    l2 = TreeNode(None, None)
    r2 = SequenceO([1,1])

    g2 = pfTm.add_rule(l2,r2)

    incl01 = TreeM(l0, l1, [])
    incr01 = SequenceM(r0, r1, 0)

    inc01 = pfTm.add_inclusion(g0,g1,incl01,incr01)


    incl02a = TreeM(l0, l2, [])
    incr02a = SequenceM(r0, r2, 0)

    inc02a = pfTm.add_inclusion(g0,g2,incl02a,incr02a)

    incl02b = TreeM(l0, l2, [TreeM.Left])
    incr02b = SequenceM(r0, r2, 1)

    inc02b = pfTm.add_inclusion(g0,g2,incl02b,incr02b)

    incl02c = TreeM(l0, l2, [TreeM.Right])
    incr02c = SequenceM(r0, r2, 1)

    inc02c = pfTm.add_inclusion(g0,g2,incl02c,incr02c)

    s = TreeNode(TreeLeaf(),TreeNode(TreeNode(None, None), TreeLeaf()))
    pfT = pfTm.get()
    T = GT(pfT)
    s = T.extend(s)
    print(s)

def height_as_a_tree():
    pfTm = FlatPFunctor.Maker(Tree, Tree)

    l0 = None
    r0 = TreeNode(TreeLeaf(), None)

    g0 = pfTm.add_rule(l0,r0)

    l1 = TreeLeaf()
    r1 = TreeNode(TreeLeaf(), None)

    g1 = pfTm.add_rule(l1,r1)

    l2 = TreeNode(None, None)
    r2 = TreeNode(TreeLeaf(), TreeNode(TreeLeaf(), None))

    g2 = pfTm.add_rule(l2,r2)

    incl01 = TreeM(l0, l1, [])
    incr01 = TreeM(r0, r1, [])

    inc01 = pfTm.add_inclusion(g0,g1,incl01,incr01)


    incl02a = TreeM(l0, l2, [])
    incr02a = TreeM(r0, r2, [])

    inc02a = pfTm.add_inclusion(g0,g2,incl02a,incr02a)

    incl02b = TreeM(l0, l2, [TreeM.Left])
    incr02b = TreeM(r0, r2, [TreeM.Right])

    inc02b = pfTm.add_inclusion(g0,g2,incl02b,incr02b)

    incl02c = TreeM(l0, l2, [TreeM.Right])
    incr02c = TreeM(r0, r2, [TreeM.Right])

    inc02c = pfTm.add_inclusion(g0,g2,incl02c,incr02c)

    s = TreeNode(TreeLeaf(),TreeNode(None, None))
    s = TreeNode(TreeLeaf(),TreeNode(TreeNode(None, None), TreeLeaf()))
    pfT = pfTm.get()
    T = GT(pfT)
    s = T.extend(s)
    print(s)




if __name__ == "__main__":
    identity()
    mirror()
    height_as_a_tree()
    height_as_a_word()


