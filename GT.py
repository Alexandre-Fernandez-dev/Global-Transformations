import networkx as nx

depth = 0

class Rule:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.self_inclusions = set()

    def __eq__(self, other):
        if not isinstance(other,Rule):
            return False
        return self.lhs == other.lhs

    def __hash__(self):
        return hash(self.lhs)

    def __repr__(self):
        return str(self.lhs) + " => " + str(self.rhs)


class Inclusion():
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
        return Inclusion(self.g_a, other.g_b, self.lhs.compose(other.lhs), self.rhs.compose(other.rhs))


class GT:
    def __init__(self, CS, CD):
        self.CS = CS
        self.CD = CD
        self.G = nx.MultiDiGraph()
        self.smalls = None
        self.small_pred = None

    def add_rule(self, l, r):
        self.smalls = None
        self.small_pred = None
        rule = Rule(l, r)
        self.G.add_node(rule)
        return rule

    def add_inclusion(self, g_a, g_b, l, r):
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
            e = self.G.add_edge(g_a, g_b, key = inc)
        return (g_a, g_b, inc)

    # TODO no need to compute morphisms
    def compute_small_rules(self, g):
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
            def merge(res_a, h_a, res_b, h_b):
                if h_a == None:
                    raise ValueError("First argument cannot be None")
                elif h_b == None:
                    assert h_a.dom == res_b.object
                    on_b = h_a
                    res = res_a
                    for ins in res_b.obs_by:
                        ins.observe(res, on_b if ins.subresult == None else ins.subresult.compose(on_b))
                    res_b.obs_by = None
                    res_b.object = None
                    results.remove(res_b)
                elif res_a is res_b:
                    if h_a != h_b:
                        (obj,lift) = self.CD.quotient(h_a, h_b)
                        res_a.object = obj
                        for ins in res_a.obs_by:
                            assert ins.subresult != None
                            ins.subresult = lift(ins.subresult)
                else:
                    assert h_a.dom == h_b.dom
                    if res_a.is_rhs and res_b.is_rhs:
                        (obj, on_a, on_b) = self.CD.merge(h_a, h_b)
                        res = Result(obj, False)
                        results.add(res)
                        for ins in res_a.obs_by:
                            ins.observe(res, on_a if ins.subresult == None else ins.subresult.compose(on_a))
                        res_a.obs_by = None
                        res_a.object = None
                        results.remove(res_a)
                        for ins in res_b.obs_by:
                            ins.observe(res, on_b if ins.subresult == None else ins.subresult.compose(on_b))
                        res_b.obs_by = None
                        res_b.object = None
                        results.remove(res_b)
                    else:
                        # TODO clean
                        if not res_a.is_rhs and not res_b.is_rhs:
                            (obj, on_bl) = self.CD.merge_2_in_1(h_a, h_b)
                        elif not res_a.is_rhs and res_b.is_rhs:
                            (obj, on_bl) = self.CD.merge_2_in_1(h_a, h_b)
                        elif res_a.is_rhs and not res_b.is_rhs:
                            temp = h_a
                            h_a = h_b
                            h_b = temp
                            temp = res_a
                            res_a = res_b
                            res_b = temp
                            (obj, on_bl) = self.CD.merge_2_in_1(h_a, h_b)
                        res = res_a
                        for ins in res_b.obs_by:
                            ins.observe(res, on_bl if ins.subresult == None else
                                        ins.subresult.compose(on_bl))
                        res_b.obs_by = None
                        res_b.object = None
                        results.remove(res_b)

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

        def close(ins):
            global depth
            small = True
            for under_rule, _, inc in self.G.in_edges(ins.rule, keys = True):
                under_match = inc.lhs.compose(ins.ins)
                small = False
                if under_match not in matches:
                    under_match.clean()
                    under_ins = add_instance(under_rule, under_match, False, False)
                else:
                    under_ins = matches[under_match]
                subresult = inc.rhs if ins.subresult == None else inc.rhs.compose(ins.subresult)
                Result.merge(ins.result, subresult, under_ins.result, under_ins.subresult)
                if not under_ins.green:
                    depth -= 1
                    close(under_ins)
                    depth += 1
            ins.green = True

        def star(ins):
            global depth
            top = True
            for _, over_rule, inc in self.G.out_edges(ins.rule, keys = True):
                for over_match in self.CS.pattern_match(inc.lhs, ins.ins):
                    top = False
                    if over_match in matches:
                        over_ins = matches[over_match]
                    else:
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
            # print("POOOOOOOOOOOOOOOOOOP")
            # small_ins.black = True
            assert not small_ins.black
            star(small_ins)
            for dep_ins in small_ins.uppercone:
                dep_ins.decrNbDep()
            small_ins.result.obs_by.remove(small_ins)
            del matches[small_ins.ins]

        print(len(results), len(matches))
        return results
