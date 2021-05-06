class DataStructure:
    """
    Represents a Data type / structure

    Methods
    -------
    TO() : Type
        returns the type of the objects

    TM() : Type
        returns the type of the inclusions / morphisms
    
    pattern_match(p, g) : Iterator[TM()]
        returns an Iterator over the inclusions of the pattern p in g
    
    multi_merge(m1, m2) : TO(), TM(), TM()
        a span is two inclusions m1, m2 from the same object as follows:
        
        m1.dom --m2--> m2.cod
        |
        m1
        |
        v
        m1.cod

        the pushout computes the object r and the two inclusions m1p, p2p such that
        the following diagram commutes

        m1.dom --m2--> m2.cod
        |              |
        m1            m1p
        |              |
        v              v
        m1.cod --m2p-> r

        and is optimal (ie. is a pushout)

        this functions computes the same kind of operation for a list of n such spans,
            from n source objects to 2 destination objects

        see generalizedPushout in article(ref) for more details

    multi_merge2_in_1(m1, m2)
        do the multi_merge operation in place into the desination object of the m1's

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
