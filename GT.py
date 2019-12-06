import networkx as nx

depth = 0

class Rule:
    """
    A rule of a global transformation.

    Attributes
    ----------
    lhs : ??.Object
        the left hand side of the rule
    rhs : ??.Object
        the right hand side of the rule
    self_inclusions : Inclusion
        inclusions of the rule in itself (automorphisms)
    """

    def __init__(self, lhs, rhs):
        """
        Parameters
        ----------
        lhs : ??.Object
            the left hand side of the rule
        rhs : ??.Object
            the right hand side of the rule
        """

        self.lhs = lhs
        self.rhs = rhs
        self.self_inclusions = set()

    def __eq__(self, other):
        """
        Parameters
        ----------
        other : Rule
            an other rule
        """

        if not isinstance(other,Rule):
            return False
        return self.lhs == other.lhs

    def __hash__(self):
        return hash(self.lhs)

    def __repr__(self):
        return str(self.lhs) + " => " + str(self.rhs)


class Inclusion():
    """
    A rule inclusion

    Attributes
    ----------
    g_a : Rule
        source rule
    g_b : Rule
        destination rule
    lhs : ??.Morphism
        a morphism that includes g_a.lhs in g_b.lhs
    rhs : ??.Morphism
        a morphism that includes g_a.rhs in g_b.rhs
    
    Methods
    -------
    compose(other)
        composes the inclusion with the other inclusions if domain and codomains matches (TODO self . other or other . self)
    """

    def __init__(self, g_a, g_b, lhs, rhs):
        self.g_a = g_a
        self.g_b = g_b
        self.lhs = lhs
        self.rhs = rhs

    def __eq__(self, other):
        if not isinstance(other,Inclusion):
            return False
        return self.lhs == other.lhs

    def __hash__(self):
        return hash(self.lhs)

    def __repr__(self):
        return str(self.lhs) + ' => ...' #+ str(self.rhs)

    def compose(self, other):
        """
        composes the inclusion with the other inclusions if domain and codomains matches (TODO self . other or other . self)

        Parameters
        ----------
        other : Inclusion
            an other inclusion with matching domain (TODO ?)

        Returns
        -------
        Inclusion
            the composition
        
        """
        return Inclusion(self.g_a, other.g_b, self.lhs.compose(other.lhs), self.rhs.compose(other.rhs))


class GT:
    """
    A global transformation T from the category CS to the category CD

    Attributes
    ----------
    CS : DataStructure (TODO use Datatype/DataStructure as category)
        the source Datatype
    
    CD : DataStructure
        the destination Datatype
    
    G : nx.MultiDiGraph
        the MultiDiGraph of the rules and rules inclusions of the GT
    
    smalls : Set
        the set of bottom rules
    
    small_pred : nx.MultiDiGraph (TODO hide ?)
        the graph associating to each rule the bottom rules under it
    
    Methods
    -------
    add_rule(l, r)
        add a new rule with lhs l and rhs r in G and returns it

    add_inclusion(g_a, g_b, l, r)
        add a new rule inclusion from g_a to g_b with l the inclusion of lhs and r the inclusion of rhs
    
    compute_small_rules(g) (TODO hide ?)
        initialize small_pred for the given rule g
    
    apply(X)
        compute T(X)

    """

    def __init__(self, CS, CD):
        self.CS = CS
        self.CD = CD
        self.G = nx.MultiDiGraph()
        self.smalls = None
        self.small_pred = None

    def add_rule(self, l, r):
        """
        creates and add a new rule with lhs l and rhs r in G and returns it

        Parameters
        ----------
        l : CS.O
            the left hand side of the rule

        r : CD.O
            the right hand side of the rule
        
        Returns
        -------
        Rule
            the new rule
        """
        self.smalls = None
        self.small_pred = None
        rule = Rule(l, r)
        self.G.add_node(rule)
        return rule

    def add_inclusion(self, g_a, g_b, l, r):
        """
        creates and add a new inclusion of rules from g_a to g_b and returns it

        Parameters
        ----------
        g_a : Rule
            the source rule

        g_b : Rule
            the destination rule

        l : CS.M
            the inclusions of the left hand sides g_a.lhs -> g_b.lhs

        r : CD.M
            the inclusions of the right hand sides g_a.rhs -> g_b.rhs
        
        Returns
        -------
        Inclusion
            the new inclusion
        """
        assert g_a.lhs == l.dom
        assert g_b.lhs == l.cod
        assert g_a.rhs == r.dom
        assert g_b.rhs == r.cod
        self.smalls = None
        self.small_pred = None
        inc = Inclusion(g_a, g_b, l, r)
        if g_a == g_b:
            g_a.self_inclusions.add(inc)
        else:
            self.G.add_edge(g_a, g_b, key = inc)
        return (g_a, g_b, inc)

    # TODO no need to compute morphisms
    def compute_small_rules(self, g):
        """ (TODO remove doc ?)
        initialize small_pred for the given rule g

        Parameters
        ----------
        g : Rule
            a rule of G
        
        Returns
        -------
        List
            the list of small rules under g
        """
        if g in self.small_pred.nodes():
            return [ r for _, _, r in self.small_pred.in_edges(g, keys = True) ]
        self.small_pred.add_node(g)
        l = []
        for s, _, inc in self.G.in_edges(g, keys = True):
            r = self.compute_small_rules(s)
            if r == []:
                l.append(inc)
            else:
                l = l + [ incp.compose(inc) for incp in r ]
        if l == []:
            self.smalls.add(g)
            # self.small_pred.add_edge(g, g, None)
        for inc in l:
            self.small_pred.add_edge(inc.g_a, g, inc)
        return l

    def apply(self, X):
        """
        compute T(X)

        Parameters
        ----------
        X : CS.O
            the input object
        
        Returns
        -------
        CD.O
            the result
        """
        if self.smalls == None:
            self.smalls = set()
            self.small_pred = nx.MultiDiGraph()
            for g in self.G.nodes:
                self.compute_small_rules(g)

        class Instance():
            def __init__(self_, rule, ins, black, green):
                # print("test", ins.dom, rule.lhs)
                assert isinstance(rule, Rule)
                assert ins.dom == rule.lhs
                assert ins.cod == X
                self_.black = black
                self_.green = green
                self_.rule = rule
                self_.nb_dep = len(self.small_pred.in_edges(rule))
                self_.ins = ins          # C[rule.lhs, X]
                self_.result = None      # Result or None
                self_.subresult = None   # C[rule.rhs, self.result.object] or None
                self_.uppercone = []
                for small_rule, _, inc in self.small_pred.in_edges(rule, keys = True):
                    small_match = inc.lhs.compose(ins)
                    if small_match not in matches:
                        small_ins = add_instance(small_rule, small_match, False, False)
                        fifo.insert(0, small_ins)
                    else:
                        small_ins = matches[small_match]
                    small_ins.uppercone.append(self_)

            def observe(self, res, m):
                assert m == None or (m.dom == self.rule.rhs and m.cod == res.object)
                assert self not in res.obs_by
                self.result = res
                self.subresult = m
                res.obs_by.append(self)

            def decrNbDep(self):
                self.nb_dep -= 1
                if self.nb_dep == 0:
                    self.result.obs_by.remove(self)
                    if len(self.result.obs_by) == 0:
                        self.result = None
                        self.subresult = None
                        results.remove(self.result)
                    del matches[self.ins]

            def __repr__(self):
                return "Instance : [" + " rule : " + str(self.rule) + " | match : " + str(self.ins) + " | result : " + str(self.result) + " | subresult : " + str(self.subresult) + "]"

        class Result():
            def __init__(self,obj,isrhs):
                self.object = obj     # C.Object
                self.is_rhs = isrhs
                self.obs_by = []      # List of ins:Instance with  ins/result = self
            
            @staticmethod
            def triv_merge(res, h, u_res, u_h):
                assert u_h == None
                assert h.dom == u_res.object
                on_u = h
                for ins in u_res.obs_by:
                    ins.observe(res, on_u if ins.subresult == None else ins.subresult.compose(on_u))
                u_res.obs_by = None
                u_res.object = None
                results.remove(u_res)
        
        def multi_merge(l_merges):
            res_old, res_new = None, None
            mult_merge_arg1 = []
            mult_merge_arg2 = []
            # print("multi merge", len(l_merges))
            # for res_old_i, h_old, res_new_i, h_new in l_merges:
                # print("arg :")
                # print(res_old_i)
                # print(h_old)
                # print(res_new_i)
                # print(h_new)
            for res_old_i, h_old, res_new_i, h_new in l_merges:
                if res_new == None:
                    res_new = res_new_i
                else:
                    assert(res_new == res_new_i)
                if res_old == None:
                    res_old = res_old_i
                else:
                    assert(res_old == res_old_i)
                mult_merge_arg1.append(h_old)
                mult_merge_arg2.append(h_new)
            # print("old res", res_old)
            # print("new res", res_new)
            if res_old != None and res_new != None:
                if res_old.is_rhs:
                    obj, on_old, on_new = self.CD.multi_merge(mult_merge_arg1, mult_merge_arg2)
                    res = Result(obj, False)
                    results.add(res)
                    for ins in res_old.obs_by:
                        ins.observe(res, on_old if ins.subresult == None else
                                    ins.subresult.compose(on_old))
                    res_old.obs_by = None
                    res_old.object = None
                    results.remove(res_old)
                    # print(type(res_old), type(res_new), type(res_new.obs_by))
                    for ins in res_new.obs_by:
                        ins.observe(res, on_new if ins.subresult == None else
                                    ins.subresult.compose(on_new))
                    res_new.obs_by = None
                    res_new.object = None
                    results.remove(res_new)
                else:
                    obj, on_new = self.CD.multi_merge_2_in_1(mult_merge_arg1, mult_merge_arg2)
                    for ins in res_new.obs_by:
                        ins.observe(res_old, on_new if ins.subresult == None else
                                    ins.subresult.compose(on_new))
                    res_new.obs_by = None
                    res_new.object = None
                    results.remove(res_new)

        #     @staticmethod
        #     def merge(res_a, h_a, res_b, h_b):
        #         # print("\ntry merge")
        #         # print("h_a", h_a)
        #         # print("res_a", res_a)
        #         # print("h_b", h_b)
        #         # print("res_b", res_b)
        #         if h_a == None:
        #             raise ValueError("First argument cannot be None")
        #         elif h_b == None:
        #             assert h_a.dom == res_b.object
        #             on_b = h_a
        #             res = res_a
        #             for ins in res_b.obs_by:
        #                 ins.observe(res, on_b if ins.subresult == None else ins.subresult.compose(on_b))
        #             res_b.obs_by = None
        #             res_b.object = None
        #             results.remove(res_b)
        #         elif res_a is res_b:
        #             if h_a != h_b:
        #                 raise Exception("Try to fold an object (quotient needed)")
        #             #     (obj,lift) = self.CD.quotient(h_a, h_b)
        #             #     res_a.object = obj
        #             #     for ins in res_a.obs_by:
        #             #         assert ins.subresult != None
        #             #         ins.subresult = lift(ins.subresult)
        #         else:
        #             assert h_a.dom == h_b.dom
        #             if res_a.is_rhs and res_b.is_rhs:
        #                 (obj, on_a, on_b) = self.CD.merge(h_a, h_b)
        #                 res = Result(obj, False)
        #                 results.add(res)
        #                 for ins in res_a.obs_by:
        #                     ins.observe(res, on_a if ins.subresult == None else ins.subresult.compose(on_a))
        #                 res_a.obs_by = None
        #                 res_a.object = None
        #                 results.remove(res_a)
        #                 for ins in res_b.obs_by:
        #                     ins.observe(res, on_b if ins.subresult == None else ins.subresult.compose(on_b))
        #                 res_b.obs_by = None
        #                 res_b.object = None
        #                 results.remove(res_b)
        #             else:
        #                 # TODO clean
        #                 if not res_a.is_rhs and not res_b.is_rhs:
        #                     (obj, on_bl) = self.CD.merge_2_in_1(h_a, h_b)
        #                 elif not res_a.is_rhs and res_b.is_rhs:
        #                     (obj, on_bl) = self.CD.merge_2_in_1(h_a, h_b)
        #                 elif res_a.is_rhs and not res_b.is_rhs:
        #                     temp = h_a
        #                     h_a = h_b
        #                     h_b = temp
        #                     temp = res_a
        #                     res_a = res_b
        #                     res_b = temp
        #                     (obj, on_bl) = self.CD.merge_2_in_1(h_a, h_b)
        #                 res = res_a
        #                 for ins in res_b.obs_by:
        #                     ins.observe(res, on_bl if ins.subresult == None else
        #                                 ins.subresult.compose(on_bl))
        #                 res_b.obs_by = None
        #                 res_b.object = None
        #                 results.remove(res_b)
        #         # print()

            def __repr__(self):
                return str(self.object) + ", observed by " + str(-1 if self.obs_by == None else len(self.obs_by)) + " instance(s)"

        matches = {}
        results = set()
        fifo = []
        depth = 0

        def add_instance(rule, match, black, green):
            # print("add i rule.l : " + str(rule.lhs) + " | " + str(match))
            res = Result(rule.rhs, True)
            results.add(res)
            ins = Instance(rule, match, black, green)
            ins.observe(res, None)
            matches[match] = ins
            for auto in rule.self_inclusions:
                match_ = auto.lhs.compose(match)
                ins_ = Instance(rule, match_, black, green)
                ins_.observe(res,auto.rhs)
                matches[match_] = ins_
            return ins

        def close(cins):
            global depth
            # print(">>>>>>>>>>>")
            cfifo = [cins]
            l_merges = []
            while len(cfifo) > 0:
                ins = cfifo.pop()
                # print("wclose", ins)
                for under_rule, _, inc in self.G.in_edges(ins.rule, keys = True):
                    # print("inc", inc)
                    under_match = inc.lhs.compose(ins.ins)
                    if under_match not in matches:
                        under_match.clean()
                        under_ins = add_instance(under_rule, under_match, False, False)
                        # print("create")
                    else:
                        under_ins = matches[under_match]
                        # print("found")
                    # print("under", under_ins)
                    new_subresult = inc.rhs if ins.subresult == None else inc.rhs.compose(ins.subresult)
                    if not under_ins.green:
                        # print("not green")
                        if ins.result != under_ins.result:
                            # new result, easy merge (replace by simpler function)
                            assert(under_ins.subresult == None)
                            Result.triv_merge(ins.result, new_subresult, under_ins.result, under_ins.subresult)
                        # else not green so actual wave so subresults are equals no need to merge
                        cfifo.insert(0, under_ins)
                    else:
                        # print("green")
                        if ins.result != under_ins.result:
                            l_merges.append((under_ins.result, under_ins.subresult, ins.result, new_subresult)) # more consistent with old before new
                ins.green = True
            multi_merge(l_merges)
            # print("<<<<<<<<<<")

        def star(ins):
            global depth
            # print("\n", "  "*depth, "STAR", ins)
            top = True
            for _, over_rule, inc in self.G.out_edges(ins.rule, keys = True):
                for over_match in self.CS.pattern_match(inc.lhs, ins.ins):
                    # print("", "  "*depth, "-match", over_rule)
                    top = False
                    if over_match in matches:
                        # print("", "  "*depth, "X")
                        over_ins = matches[over_match]
                    else:
                        # print("", "  "*depth, "O")
                        over_match.clean()
                        over_ins = add_instance(over_rule, over_match, False, False)
                    if not over_ins.black:
                        depth += 1
                        star(over_ins)
                        depth -= 1
            ins.black = True
            if top:
                assert not ins.green
                close(ins)

        def next_small():
            for small_rule in self.smalls:
                for small_match in self.CS.pattern_match(small_rule.lhs, X):
                    small_match.clean()
                    yield add_instance(small_rule, small_match, False, False)

        for i in next_small():
            fifo.insert(0, i)
            break

        while len(fifo) > 0:
            depth = 0
            small_ins = fifo.pop()
            # print("\nPOOOOOOOOOOOOOOOOOOP", small_ins.rule)
            assert not small_ins.black
            star(small_ins)
            for dep_ins in small_ins.uppercone:
                dep_ins.decrNbDep()
            small_ins.result.obs_by.remove(small_ins)
            del matches[small_ins.ins]

        print(len(results), len(matches))
        return results
