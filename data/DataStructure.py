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
    
    @staticmethod
    def TM():
        """
        returns the type of the inclusions / morphisms
        
        Returns
        -------
        Type
            the type of the inclusions / morphisms
        """

    @staticmethod
    def pattern_match(p, X):
        """
        returns a Generator to iterate on the inclusions of the pattern p in X

        Parameters
        ----------
        p : self.TO()
            the pattern
        
        X : self.TO()
            the object in which to search for X

        Returns
        -------
        generator
            A generator that iterates on inclusions from p to X
        """

    @staticmethod
    def multi_merge(m1s, m2s):
        """
        TODO
        """

    @staticmethod
    def multi_merge_2_in_1(m1s, m2s):
        """
        TODO
        """
