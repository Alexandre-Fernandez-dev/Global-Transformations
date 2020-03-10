class DataStructure:
    """
    Represents a Data type / structure

    Methods
    -------
    TO()
        returns the type of the objects

    TM()
        returns the type of the inclusions / morphisms
    
    pattern_match(p, g)
        returns a Generator to iterate on the inclusions of the pattern p in g
    
    quotient(m1, m2)
        given two inclusions m1, m2 between the same objects dom and cod
        compute an object r and a morphism cod--lift--> r such that
        r is a the quotient of cod along the equivalence relation m1 ~ m2
            --m1-->
        dom         cod
            --m2-->
        
        compute the object r and the morphism lift (might not be an inclusion)
        cod --lift--> r
        such that lift . m1 = lift . m2
        
        and is optimal (ie. is a coequalizer)
    
    merge(m1, m2)
        given two inclusions m1, m2 from the same object as follows:
        
        m1.dom --m2--> m2.cod
        |
        m1
        |
        v
        m1.cod

        compute the object r and the two inclusions m1p, p2p such that
        the following diagram commutes

        m1.dom --m2--> m2generator.cod
        |              |
        m1            m1p
        |              |
        v              v
        m1.cod --m2p-> r

        and is optimal (ie. is a pushout)

    merge2_in_1(m1, m2)
        do the merge operation in place in m1

    """

    @staticmethod
    def TO():
        """
        returns the type of the objects
        
        Returns
        -------
        Type
            the type of the objects
        """
        pass
    
    @staticmethod
    def TM():
        """
        returns the type of the inclusions / morphisms
        
        Returns
        -------
        Type
            the type of the inclusions / morphisms
        """
        pass

    @staticmethod
    def pattern_match(p, g):
        """
        returns a Generator to iterate on the inclusions of the pattern p in g

        Parameters
        ----------
        p : self.TO()
            the pattern
        
        g : self.TO()
            the object in which to search for p

        Returns
        -------
        generator
            A generator that iterates on inclusions from p to g
        """
        pass

    # REMOVED
    # @staticmethod
    # def quotient(m1, m2):
    #    """
    #    given two inclusions m1, m2 between the same objects dom and cod
    #    compute an object r and a morphism cod--lift--> r such that
    #    r is a the quotient of cod along the equivalence relation m1 ~ m2
    #        --m1-->
    #    dom         cod
    #        --m2-->
    #    
    #    compute the object r and the morphism lift (might not be an inclusion)
    #    cod --lift--> r
    #    such that lift . m1 = lift . m2
    #    
    #    and is optimal (ie. is a coequalizer)

    #    Parameters
    #    ----------
    #    m1 : self.TM()
    #        the first inclusion
    #    
    #    m2 : self.TM()
    #        the second inclusion
    #    
    #    Returns
    #    -------
    #    r, lift : tuple
    #        the quotient object and lift morphism specified above
    #    """
    #    pass

    @staticmethod
    def multi_merge(m1s, m2s):
        return None

    @staticmethod
    def multi_merge_2_in_1(m1s, m2s):
        return None

    # @staticmethod
    # def merge_2_in_1(m1, m2):
    #     """
    #     do the merge operation in place in m1

    #     Parameters
    #     ----------
    #     m1 : self.TM()
    #         the inclusion that will be mutated (FIXME hash problem ?)
    #     m2 : self.TM()
    #         the second inclusion
    #     
    #     Returns
    #     -------
    #     r, m2p : tuple
    #         the merge object and the arrow m2.cod --m2p--> r
    #     """
    #     pass

    # @staticmethod
    # def merge(m1, m2):
    #     """
    #     given two inclusions m1, m2 from the same object as follows:
    #     
    #     m1.dom --m2--> m2.cod
    #     |
    #     m1
    #     |
    #     v
    #     m1.cod

    #     compute the object r and the two inclusions m1p, p2p such that
    #     the following diagram commutes

    #     m1.dom --m2--> m2.cod
    #     |              |
    #     m1            m1p
    #     |              |
    #     v              v
    #     m1.cod --m2p-> r

    #     and is optimal (ie. is a pushout)

    #     Parameters
    #     ----------
    #     m1 : self.TM()
    #         the first inclusion
    #     m2 : self.TM()
    #         the second inclusion
    #     
    #     Returns
    #     -------
    #     r, m1p, m2p : tuple
    #         the merge object and the arrows m1.cod --m1.cod--> r,
    #         m2.cod --m2p--> r as defined above
    #     """
    #     pass

from inspect import signature

def Lazy(C):
    """
    A lazy object is the data of an expression to be evaluated in order to get an concrete object.
    The expression is given as a Python function waiting for a list of subobjects (lazy as well).
    The subobjects are not necessarily known at the construction; they are passed with the method setSubobject.
    The evaluation can be forced at any time if all the subobjects have been passed and if they are all evaluable; otherwise an exception is raised.
    The function evaluates into the expected concrete object and the list of concrete inclusions relating each subobject to that object.
    The objects are called lazy in the sense that they can be built and handle as any object of the underlying category, even if they are not yet evaluable.
    """
    
    def init_o(self, expr):
        self.obj = None
        self.expr = expr
        self.finalCountDown = len(signature(expr).parameters)
        self.subobjects = self.finalCountDown * [ None ]

    def eq_o(self, other):
        raise Exception("LazyO : illegal operation")
    
    def hash_o(self):
        raise Exception("LazyO : illegal operation")

    def setSubobject_o(self, i, sub):
        assert self.subobjects[i] == None
        self.subobjects[i] = MBaseClass(sub,self)
        self.finalCountDown -= 1
        return self.subobjects[i]

    def forceable_o(self):
        return self.finalCountDown == 0

    def force_o(self):
        if self.obj != None:
            return self.obj
        if self.forceable():
            self.obj, loulou = self.expr(*[h.s.force() if isinstance(h.s,OClass) else h.s for h in self.subobjects])
            for i, h in enumerate(self.subobjects):
                h.set(loulou[i])
            return self.obj
        raise Exception("LazyO: Force: some subobjects are missing")

    def repr_o(self):
        if self.obj == None:
            return '<NotYetConstructed>'
        else:
            return "Lazy: " + str(self.obj)
    
    OClass = type('Lazy' + C.__name__ + 'O', (), {
        '__init__'     : init_o,
        '__eq__'       : eq_o,
        '__hash__'     : hash_o,
        'setSubobject' : setSubobject_o,
        'forceable'    : forceable_o,
        'force'        : force_o,
        '__repr__'     : repr_o,
    })

    def init_m(self, s, t):
        self.s = s
        self.t = t
        self.h = None

    def eq_m(self, other):
        raise Exception("LazyM: illegal operation on lazy object")
        # if not isinstance(other, LazySequenceM):
        #     return False
        # return self.force() == other.force()

    def hash_m(self):
        raise Exception("LazyM: illegal operation on lazy object")
        # return hash(self.force())

    @property
    def dom_m(self):
        raise Exception("LazyM: illegal operation on lazy object")

    @property
    def cod_m(self):
        raise Exception("LazyM: illegal operation on lazy object")

    def compose_m(self, h):
        if isinstance(h,C.TM()):
            assert self.h != None
            return self.h.compose(h)
        if self.h != None and h.h != None:
            return self.h.compose(h.h)
        return MComposeClass(self, h)

    def repr_m(self):
        if self.h == None:
            return '<NotYetConstructed>'
        else:
            return str(self.h)
    
    MClass = type('Lazy' + C.__name__ + 'M', (), {
        '__init__'     : init_m,
        '__eq__'       : eq_m,
        '__hash__'     : hash_m,
        'dom'          : dom_m,
        'cod'          : cod_m,
        'compose'      : compose_m,
        '__repr__'     : repr_m,
    })

    def init_m_base(self, s, t):
        assert isinstance(t, OClass)
        MClass.__init__(self, s, t)

    def set_m_base(self,h):
        self.h = h
        self.s = h.dom
        self.t = h.cod

    def force_m_base(self):
        if self.h == None:
            self.t.force()
            if self.h == None:
                raise Exception("LazyMBase: Force: not yet set")
        return self.h
    
    MBaseClass = type('Lazy' + C.__name__ + 'MBase', (MClass,), {
        '__init__'  : init_m_base,
        'set'       : set_m_base,
        'force'     : force_m_base
    })

    def init_m_compose(self, h1, h2):
        MClass.__init__(self, h1.s, h2.t)
        self.h1 = h1
        self.h2 = h2

    def force_m_compose(self):
        if self.h == None:
            self.h = self.h1.force().compose(self.h2.force())
            self.s = self.h.dom
            self.t = self.h.cod
        return self.h

    MComposeClass = type('Lazy' + C.__name__ + 'MCompose', (MClass,), {
        '__init__'  : init_m_compose,
        'force'     : force_m_compose
    })

    def TO_C():
        return OClass

    def TM_C():
        return MClass

    def pattern_match_C(p, s):
        raise Exception("LazySequenceM: illegal operation on lazy object")

    def multi_merge_2_in_1_C(m1s, m2s):
        m1s = [ h.force() if isinstance(h,MClass) else h for h in m1s ]
        m2s = [ h.force() if isinstance(h,MClass) else h for h in m2s ]
        return C.multi_merge_2_in_1(m1s, m2s)

    def multi_merge_C(m1s, m2s):
        m1s = [ h.force() if isinstance(h,MClass) else h for h in m1s ]
        m2s = [ h.force() if isinstance(h,MClass) else h for h in m2s ]
        return C.multi_merge(m1s, m2s)
    
    
    DataClass = type('Lazy' + C.__name__, (DataStructure,), {
        'TO'                    : staticmethod(TO_C),
        'TM'                    : staticmethod(TM_C),
        'pattern_match'         : staticmethod(pattern_match_C),
        'multi_merge_2_in_1'    : staticmethod(multi_merge_2_in_1_C),
        'multi_merge'           : staticmethod(multi_merge_C),
    })

    return DataClass