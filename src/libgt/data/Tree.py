

class SubTree():
    pass


class SubTreeLeaf(SubTree):
    _leaf = None
    def __new__(class_, *args, **kwargs):
        if class_._instance is None:
            class_._instance = SubTree.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__(self):
        pass

    def __eq__(self, other):
        return self is other

    def __hash__(self, other):
        return 0

    def __repr__(self):
        return f"SubTreeLeaf()"


class SubTreeNode(SubTree):

    def __init__(self, l, r):
        self.l = l
        self.r = r
        self.__h = None
        pass

    def __eq__(self, other):
        if not isinstance(other,SubTreeNode):
            return False
        return self.l == other.l and self.r == other.r

    def __hash__(self):
        if self.__h is None:
            self.__h = hash((self.l,self.r))
        return self.__h
        
    def __repr__(self):
        return f"SubTreeNode({repr(self.l)},{repr(self.r)})"
