import networkx as nx


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

    def __init__(self,C):
        self.C = C
        self.G = nx.MultiDiGraph()
        self.smalls = set()
        pass

    def add_rule(self,l,r):
        rule = Rule(l,r)
        self.G.add_node(rule)
        return rule

    def add_inclusion(self,g_a,g_b,l,r):
        assert g_a.lhs == l.dom
        assert g_b.lhs == l.cod
        assert g_a.rhs == r.dom
        assert g_b.rhs == r.cod
        inc = Inclusion(g_a,g_b,l,r)
        if g_a == g_b:
            g_a.self_inclusions.add(inc)
        else:
            e = self.G.add_edge(g_a, g_b, key = inc)
        return (g_a,g_b,inc)

    def apply(self,X):
        self.small_pred = nx.MultiDiGraph()

        def toto(g):
            if g in self.small_pred.nodes():
                return [ r for _, _, r in self.small_pred.in_edges(g, keys = True) ]
            self.small_pred.add_node(g)
            l = []
            for s, _, inc in self.G.in_edges(g, keys = True):
                r = toto(s)
                if r == []:
                    l.append(inc)
                else:
                    l = l + [ incp.compose(inc) for incp in r ]
            if l == []:
                self.smalls.add(g)
                #self.small_pred.add_edge(g, g, None)
            for inc in l:
                self.small_pred.add_edge(inc.g_a, g, inc)
            return l


        for g in self.G.nodes:
            toto(g)

        # for u in self.small_pred.edges(keys = True):
        #     print(u)
        #
        # print()
        #
        # print(self.smalls)

        matches = {}
        results = set()

        def prdebug():
            print("Instances:")
            for _, ins_ in matches.items():
                print(str(ins_.ins.l) + " observes [" + str(ins_.result) + "] by " + str(ins_.subresult))
            print("Results:")
            for res_ in results:
                print(res_)


        class Instance():
            # def __eq__(self, other):
            #     if isinstance(other, Instance):
            #         return self.ins = other.ins
            #     elif isinstance(other, C.Morphism):
            #         return self.ins == other
            #     else:
            #         return False
            #
            # def __hash__(self):
            #     return hash(self.ins)

            def __init__(self, rule, ins):
                assert isinstance(rule, Rule)
                assert ins.dom == rule.lhs
                assert ins.cod == X
                #self.nb_dep = len(self.small_pred.in_edges(rule))
                self.rule = rule        # Rule
                self.ins = ins          # C[rule.lhs, X]
                self.result = None      # Result or None
                self.subresult = None   # C[rule.rhs, self.result.object] or None

            def observe(self, res, m):
                assert m == None or (m.dom == self.rule.rhs and m.cod == res.object)
                assert self not in res.obs_by
                self.result = res
                self.subresult = m
                res.obs_by.append(self)

        class Result():
            def __init__(self,obj):
                self.object = obj     # C.Object
                self.obs_by = []      # List of ins:Instance with ins/result = self

            @staticmethod
            def merge(res_a, h_a, res_b, h_b):
                # print("IN MERGE " + str(res_a is res_b))
                # prdebug()
                # print("#######################")
                if h_a == None:
                    raise ValueError("First argument should not be None")
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
                    assert h_a == h_b
                else:
                    assert h_a.dom == h_b.dom
                    (obj, on_a, on_b) = self.C.merge(h_a, h_b)
                    res = Result(obj)
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
                    # return res, h_a.compose(on_a)
                # prdebug()
                # print("OUT MERGE")

            def __repr__(self):
                return str(self.object) + ", observed by " + str(-1 if self.obs_by == None else len(self.obs_by)) + " instance(s)"

        def add_instance(rule, match):
            res = Result(rule.rhs)
            results.add(res)
            ins = Instance(rule, match)
            ins.observe(res,None)
            matches[match] = ins
            for auto in rule.self_inclusions:
                match_ = auto.lhs.compose(match)
                ins_ = Instance(rule, match_)
                ins_.observe(res,auto.rhs)
                matches[match_] = ins_
            return ins

        def process(rule, match):
            print("IN process: " + str(match))
            ins = add_instance(rule, match)
            is_top_ins = True
            for _, over_rule, inc in self.G.out_edges(ins.rule, keys = True):
                for over_match in self.C.pattern_match(inc.lhs, ins.ins):
                    print("OVER MATCH FOUND: " + str(over_match))
                    print("FOR INCLUSION: " + str(inc))
                    is_top_ins = False
                    if over_match not in matches:
                        over_match.clean()
                        process(over_rule, over_match)
                    over_ins = matches[over_match]
                    subresult = inc.rhs if over_ins.subresult == None else inc.rhs.compose(over_ins.subresult)
                    Result.merge(over_ins.result, subresult, ins.result, ins.subresult)
            print("OUT process: " + str(match))

        print()
        for small_rule in self.smalls:
            # print("small rule: " + str(small_rule))
            for small_match in self.C.pattern_match(small_rule.lhs, X):
                # print()
                if small_match not in matches:
                    small_match.clean()
                    process(small_rule, small_match)

        return results

def test():
        pass


if __name__ == "__main__":
    test()













#
