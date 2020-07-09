import networkx as nx

class Instance():
    def __init__(self, rule, nb_dep, occ): # privé à GT
        self.black = False
        self.rule = rule
        self.nb_dep = nb_dep
        self.occ = occ          # C[rule.lhs, X]
        self.result = None      # Result or None
        self.alt_result = None
        self.subresult = None   # C[rule.rhs, self.result.object] or None
        self.alt_subresult = None
        self.uppercone = []
    
    def rhs(self):
        return self.rule.get_rhs()
    
    def observe(self, res, m): # privé à GT ?
        #if self in res.obs_by:
        #    return
        # assert not self in res.obs_by # removed because of alt_result / result, instance associated to two result
        assert m == None or m.cod == res.object
        self.result = res
        self.subresult = m
        res.obs_by.append(self)

    def decrNbDep(self): # privé à GT ?
        self.nb_dep -= 1
        if self.nb_dep == 0:
            # self.result.obs_by.remove(self)
            return True # should remove ins
        return False

    def __repr__(self):
        return "Instance : [" + " occ : " + str(self.occ) + " | result : " + str(self.result) + " | subresult : " + str(self.subresult) + "]"

class InstanceInc():
    def __init__(self, rule_inc, s, t):
        self.rule_inc = rule_inc
        self.s = s
        self.t = t
    
    def rhs(self):
        return self.rule_inc.get_rhs()
    
    def __repr__(self):
        return "InsInc : [" + " lhs : " + str(self.rule_inc.lhs) + " ]"

class Result():
    def __init__(self, obj, is_rhs):
        self.object = obj
        self.is_rhs = is_rhs
        self.obs_by = []
    
    @staticmethod
    def triv_merge(res, h, u_res):
        for ins in u_res.obs_by:
            ins.observe(res, h if ins.subresult == None else ins.subresult.compose(h))
        for i in res.obs_by:
            assert i.subresult == None or i.subresult.cod == res.object
        u_res.obs_by = None
        u_res.object = None
        return u_res # to remove of results
    
    @staticmethod
    def multi_merge_2(lm, CD, m):
        l_new = []
        l_old = []
        res_old = None
        res_new = None
        for ins in lm:
            # print(ins.alt_subresult)
            # print(ins.alt_result)
            # print(ins.subresult)
            # print(ins.result)
            l_old.append(ins.alt_subresult)
            l_new.append(ins.subresult)
            if res_old == None:
                res_old = ins.alt_result
                res_new = ins.result
            # else:
            #     print(res_new)
            #     print(ins.alt_result)
            #     assert res_new == ins.alt_result
            #     assert res_old == ins.result
        return Result.multi_merge(l_old, l_new, res_old, res_new, CD, m)
    
    @staticmethod
    def multi_merge(l_old, l_new, res_old, res_new, CD, m):
        # print("MULTI MERGE", len(l_old), len(l_new))
        # print("res", res_old, res_new)
        # all l_old must refer to an instance with result res_old, same for res_new
        # for i in m:
        #     print(m[i].result)
        if len(l_old) == 0:
            return [], []
        if res_old.is_rhs:
            assert res_new.is_rhs
            obj, on_old, on_new = CD.multi_merge(l_old, l_new)
            res = Result(obj, False)
            print("----")
            print(on_old)
            print([i.subresult for i in res_old.obs_by])
            print("----")
            for ins in res_old.obs_by:
                if ins.result == res_old:
                    ins.observe(res, on_old if ins.subresult is None else ins.subresult.compose(on_old))
                elif ins.alt_result == res_old:
                    ins.observe(res, on_old if ins.alt_subresult is None else ins.alt_subresult.compose(on_old))
                else:
                    assert False
            res_old.obs_by = None
            res_old.object = None
            for ins in res_new.obs_by:
                if ins.result != res: # already set ?
                    if ins.result == res_new:
                        ins.observe(res, on_new if ins.subresult is None else ins.subresult.compose(on_new))
                    elif ins.alt_result == res_new:
                        assert False
                        ins.observe(res, on_new if ins.alt_subresult is None else ins.alt_subresult.compose(on_new))
                    else:
                        assert False
            for i in res.obs_by:
                i.alt_result = None
                i.alt_subresult = None
            res_new.obs_by = None
            res_new.object = None
            # print()
            # for i in m:
            #     print(m[i].result)
            return [res], [res_old, res_new]
        else:
            obj, on_new = CD.multi_merge_2_in_1(l_old, l_new)
            for ins in res_new.obs_by:
                if ins.result != res_old:
                    if ins.result == res_new:
                        ins.observe(res_old, on_new if ins.subresult is None else ins.subresult.compose(on_new))
                    elif ins.alt_result == res_new:
                        assert False
                        ins.observe(res_old, on_new if ins.alt_subresult is None else ins.alt_subresult.compose(on_new))
                    else:
                        assert False
            for i in res_old.obs_by:
                i.alt_result = None
                i.alt_subresult = None
            res_new.obs_by = None
            res_new.object = None
            return [], [res_new]


class FlatPFunctor:
    class Rule:
        def __init__(self, lhs, rhs):
            self.lhs = lhs
            self.rhs = rhs
            self.self_inclusions = set()
            # self.is_small
            # self.nb_smalls 
        
        def get_rhs(self):
            return self.rhs

        def __eq__(self, other):
            if not isinstance(other,FlatPFunctor.Rule):
                return False
            return self.lhs == other.lhs

        def __hash__(self):
            return hash(self.lhs)

        def __repr__(self):
            return str(self.lhs) + " => " + str(self.rhs)

        def iter_self_inclusions(self):
            for i in self.self_inclusions:
                yield i

    class Inclusion:
        def __init__(self, g_a, g_b, lhs, rhs):
            self.g_a = g_a
            self.g_b = g_b
            self.lhs = lhs
            self.rhs = rhs

        def get_rhs(self):
            return self.rhs

        def __eq__(self, other):
            if not isinstance(other, FlatPFunctor.Inclusion):
                return False
            return self.lhs == other.lhs

        def __hash__(self):
            return hash(self.lhs)

        def __repr__(self):
            return str(self.lhs) + ' => ...' #+ str(self.rhs)

    class Maker():
        def __init__(self, CS, CD):
            self.CS = CS
            self.CD = CD
            self.l_to_r = {}
            self.G = nx.MultiDiGraph()

        def add_rule(self, l, r):
            rule = FlatPFunctor.Rule(l, r)
            self.G.add_node(rule)
            self.l_to_r[l] = rule
            return rule

        def add_inclusion(self, g_a, g_b, l, r):
            inc = FlatPFunctor.Inclusion(g_a, g_b, l, r)
            if g_a == g_b:
                g_a.self_inclusions.add(inc)
            else:
                self.G.add_edge(g_a, g_b, key = inc)
            return (g_a, g_b, inc)

        def get(self):
            return FlatPFunctor(self.CS, self.CD, self.G, self.l_to_r)
        
    def __init__(self, CS, CD, G, l_to_r):
        self.CS = CS
        self.CD = CD
        self.G = G
        self.l_to_r = l_to_r
        self.smalls = set()
        self.small_pred = nx.MultiDiGraph()
        # replace by union find like datastructure or set ?
        def f(g): # TODO replace by smaller function that only computes nb_small
            if g in self.small_pred.nodes():
                return [ r for _, _, r in self.small_pred.in_edges(g, keys = True) ]
            self.small_pred.add_node(g)
            l = []
            for s, _, inc in self.G.in_edges(g, keys = True):
                r = f(s)
                if r == []:
                    l.append(s)
                else:
                    l = l + [ sp for sp in r ]
            if l == []:
                self.smalls.add(g)
            for s in l:
                self.small_pred.add_edge(s, g, None)
            return l
        for g in self.G.nodes:
            f(g)
    
    def is_small(self, ins): # could be a bool in ins
        return self.l_to_r[ins.rule.lhs] in self.smalls

    def nb_small(self, ins): # could be a bool in ins
        return len(self.small_pred.in_edges(self.l_to_r[ins.rule.lhs]))

    def next_small(self, X):
        for small_rule in self.smalls:
            for small_match in self.CS.pattern_match(small_rule.lhs, X):
                small_match.clean()
                get_s_ins = lambda : Instance(small_rule, len(self.small_pred.in_edges(small_rule)), small_match)
                yield get_s_ins
    
    def iter_under(self, ins, matches):
        for u_rule, _, u_inc in self.G.in_edges(self.l_to_r[ins.rule.lhs], keys = True):
            u_occ = u_inc.lhs.compose(ins.occ)
            get_u_ins = lambda : Instance(u_rule, len(self.small_pred.in_edges(u_rule)), u_occ)
            get_ins_inc = lambda u_ins : InstanceInc(u_inc, u_ins, ins)
            yield u_occ, get_u_ins, get_ins_inc
    
    def pmatch_up(self, ins, matches):
        for _, o_rule, o_inc in self.G.out_edges(self.l_to_r[ins.rule.lhs], keys = True):
            for o_occ in self.CS.pattern_match(o_inc.lhs, ins.occ):
                get_o_ins = lambda : Instance(o_rule, len(self.small_pred.in_edges(o_rule)), o_occ)
                get_ins_inc = lambda o_ins : InstanceInc(o_inc, ins, o_ins)
                yield o_occ, get_o_ins, get_ins_inc
    
    def iter_self_inclusions(self, ins, matches):
        rule = self.l_to_r[ins.rule.lhs]
        for inc in rule.iter_self_inclusions():
            s_occ = inc.lhs.compose(ins.occ)
            get_s_ins = lambda : Instance(rule, len(self.small_pred.in_edges(rule)), s_occ)
            get_ins_inc = lambda u_ins : InstanceInc(inc, u_ins, inc)
            yield s_occ, get_s_ins, get_ins_inc

class OPFunctor:
    class Choices:
        def __init__(self, lhs, results):
            self.results = results
            self.lhs = lhs # redundant may be removed keeped for the assert
            self.f_alpha_inv = {}
            self.f_beta = {}
            self.under = {}

        def add_under_choice(self, linc, uchoice, rincs):
            assert linc.dom == uchoice.lhs
            self.under[linc] = uchoice
            for rinc in rincs:
                if rinc == None:
                    continue
                assert rinc.cod in self.results
                self.f_beta[(linc, rinc.cod)] = rinc
                fiber = self.f_alpha_inv.setdefault(linc, {})
                rfiber = fiber.setdefault(rinc.dom, [])
                rfiber.append(rinc.cod)

    class ORule:
        def __init__(self, lhs, rhs_choice, rhs_run):
            self.lhs = lhs
            self.rhs_choice = rhs_choice
            self.rhs_run = rhs_run
            self.self_inclusions = set()
        
        def __eq__(self, other):
            if not isinstance(other,OPFunctor.ORule):
                return False
            return self.lhs == other.lhs

        def __hash__(self):
            return hash(self.lhs)

        def __repr__(self):
            return str(self.lhs) + " => " + str(self.rhs_choice)

        def iter_self_inclusions(self):
            yield from self.self_inclusions

    class OInclusion():
        def __init__(self, g_a, g_b, lhs):
            self.g_a = g_a
            self.g_b = g_b
            self.lhs = lhs

        def __eq__(self, other):
            if not isinstance(other, OPFunctor.OInclusion):
                return False
            return self.lhs == other.lhs

        def __hash__(self):
            return hash(self.lhs)

        def __repr__(self):
            return str(self.lhs) + ' => ...' #+ str(self.rhs)

    class Maker():
        def __init__(self, CS, LCD):
            self.CS = CS
            self.CD = LCD
            self.l_to_r = {}
            self.G = nx.MultiDiGraph()

        def add_o_rule(self, l, rc, rr):
            rule = OPFunctor.ORule(l, rc, rr)
            self.G.add_node(rule)
            self.l_to_r[l] = rule
            return rule

        def add_o_inclusion(self, g_a, g_b, l):
            inc = OPFunctor.OInclusion(g_a, g_b, l)
            if g_a == g_b:
                g_a.self_inclusions.add(inc)
            else:
                self.G.add_edge(g_a, g_b, key = inc)
            return (g_a, g_b, inc)

        def get(self):
            return OPFunctor(self.CS, self.CD, self.G, self.l_to_r)

    def __init__(self, CS, CD, G, l_to_r):
        self.CS = CS
        self.CD = CD
        self.G = G
        self.l_to_r = l_to_r
        self.smalls = set()
        self.small_pred = nx.MultiDiGraph()
        def f(g): # TODO replace by smaller function that only computes nb_small
            if g in self.small_pred.nodes():
                return [ r for _, _, r in self.small_pred.in_edges(g, keys = True) ]
            self.small_pred.add_node(g)
            l = []
            for s, _, inc in self.G.in_edges(g, keys = True):
                r = f(s)
                if r == []:
                    l.append(s)
                else:
                    l = l + [ sp for sp in r ]
            if l == []:
                self.smalls.add(g)
            for s in l:
                self.small_pred.add_edge(s, g, None)
            return l
        for g in self.G.nodes:
            f(g)

    class RuleInst:
        def __init__(self, o_rule, auto = None):
            self.o_rule = o_rule
            self.lhs = o_rule.lhs
            self.incs_in = { linc : None for linc in o_rule.rhs_choice.under if linc.dom != o_rule.lhs }
            self.r = None
            self.auto = auto

        def get_rhs(self):
            return self.rhs()
        
        def rhs(self):
            if self.r != None:
                return self.r
            else:
                if self.auto == None:
                    # print("incs_in", self.incs_in)
                    # print(self.o_rule.rhs_choice.under)
                    self.r = self.o_rule.rhs_run(self.o_rule.rhs_choice, self.incs_in)
                    # print(self.incs_in)
                    # print("got ", self.r)
                    # DEBUG CHECK !
                    # for i in self.incs_in.items():
                    #     print(i)
                    for linc, incinst in self.incs_in.items():
                        # print(linc, incinst)
                        # print(incinst.g_a.rhs())
                        # print(self.o_rule.rhs_choice.f_alpha_inv[incinst.g_a.rhs()])
                        # print("rkfjg", type(self.o_rule.rhs_choice.f_alpha_inv[incinst.lhs][incinst.g_a.rhs()]))
                        # print(self.r)
                        # print(self.o_rule.rhs_choice.f_alpha_inv[incinst.lhs][incinst.g_a.rhs()])
                        assert self.r in self.o_rule.rhs_choice.f_alpha_inv[incinst.lhs][incinst.g_a.rhs()]
                    return self.r
                else:
                    incl, over_rule = self.auto 
                    self.r = over_rule.rhs().restrict(over_rule.o_rule.rhs_choice.f_beta[(incl, over_rule.rhs())]).dom # SHOUD be a equal to the over rhs or this rhs must have been specified in the choices
                    return self.r

        def __eq__(self, other):
            if not isinstance(other,OPFunctor.RuleInst):
                return False
            return self.lhs == other.lhs and self.r == other.r

        def __hash__(self):
            return hash(self.lhs)

        def __repr__(self):
            return str(self.lhs)# + " => " + str(self.rhs)

    class InclusionInst():
        def __init__(self, o_inc, g_a, g_b, auto = False):
            self.o_inc = o_inc
            self.g_a = g_a
            self.g_b = g_b
            self.lhs = o_inc.lhs
            self.r = None
            if not auto:
                assert self.g_b.incs_in[self.lhs] == None
                self.g_b.incs_in[self.lhs] = self
        
        def get_rhs(self):
            return self.rhs()

        def rhs(self):
            # print("called")
            if self.r != None:
                return self.r
            else:
                # print(type(self.lhs), type(self.g_b.rhs))
                self.r = self.g_b.o_rule.rhs_choice.f_beta[(self.lhs, self.g_b.rhs())]
                return self.r

        def __repr__(self):
            return str(self.lhs)# + " => " + str(self.rhs)

    def is_small(self, ins):
        return self.l_to_r[ins.rule.lhs] in self.smalls

    def nb_small(self, ins):
        return len(self.small_pred.in_edges(self.l_to_r[ins.rule.lhs]))

    def next_small(self, X):
        for small_o_rule in self.smalls:
            for small_match in self.CS.pattern_match(small_o_rule.lhs, X):
                small_match.clean()
                small_rule = self.RuleInst(small_o_rule)
                get_s_ins = lambda : Instance(small_rule, len(self.small_pred.in_edges(small_o_rule)), small_match)
                yield get_s_ins

    def iter_under(self, ins, matches):
        for u_o_rule, _, u_o_inc in self.G.in_edges(self.l_to_r[ins.rule.lhs], keys = True):
            # u_rule = self.RuleInst(u_o_rule)
            # u_inc = self.InclusionInst(u_o_inc, u_rule, rule)
            u_occ = u_o_inc.lhs.compose(ins.occ)
            # if u_occ not in matches:
            def get_u_ins():
                u_rule = self.RuleInst(u_o_rule)
                return Instance(u_rule, len(self.small_pred.in_edges(u_o_rule)), u_occ)
            get_ins_inc = lambda u_ins : InstanceInc(self.InclusionInst(u_o_inc, u_ins.rule, ins.rule), u_ins, ins)
            yield u_occ, get_u_ins, get_ins_inc
            # else:
            #     # print("RECOVERED RULEINST under")
            #     u_ins = matches[u_occ]
            #     u_rule = u_ins.rule
            #     get_u_ins = lambda : u_ins
            #     get_ins_inc = lambda u_ins : InstanceInc(self.InclusionInst(u_o_inc, u_rule, ins.rule), u_ins, ins)
            #     yield u_occ, get_u_ins, get_ins_inc

    def pmatch_up(self, ins, matches):
        for _, over_o_rule, inc_o in self.G.out_edges(self.l_to_r[ins.rule.lhs], keys = True):
            for over_occ in self.CS.pattern_match(inc_o.lhs, ins.occ):
                # if over_occ in matches: # redundant check with GT_DU
                #     # print("RECOVERED RULEINST up")
                #     over_ins = matches[over_occ]
                #     over_rule = over_ins.rule
                #     get_o_ins = lambda : over_ins
                #     get_ins_inc = lambda o_ins : InstanceInc(self.InclusionInst(inc_o, ins.rule, over_rule), ins, o_ins)
                #     yield over_occ, get_o_ins, get_ins_inc
                # else:
                def get_o_ins():
                    over_rule = self.RuleInst(over_o_rule)
                    return Instance(over_rule, len(self.small_pred.in_edges(over_o_rule)), over_occ)
                get_ins_inc = lambda o_ins : InstanceInc(self.InclusionInst(inc_o, ins.rule, o_ins.rule), ins, o_ins)
                yield over_occ, get_o_ins, get_ins_inc

    def iter_self_inclusions(self, ins, matches):
        for inc_o in ins.rule.o_rule.iter_self_inclusions():
            s_occ = inc_o.lhs.compose(ins.occ)
            # if s_occ not in matches:
            def get_s_ins():
                self_rule = self.RuleInst(ins.rule.o_rule, (inc_o.lhs, ins.rule))
                return Instance(self_rule, len(self.small_pred.in_edges(self_rule.o_rule)), s_occ)
            get_ins_inc = lambda u_ins : InstanceInc(self.InclusionInst(inc_o, u_ins.rule, ins.rule, True), u_ins, ins)
            yield s_occ, get_s_ins, get_ins_inc
            # else:
            #     # print("RECOVERED RULEINST self")
            #     self_ins = matches[s_occ]
            #     self_rule = self_ins.rule
            #     get_s_ins = lambda : self_ins
            #     get_ins_inc = lambda u_ins : InstanceInc(self.InclusionInst(inc_o, self_rule, ins.rule, True), u_ins, ins)
            #     yield s_occ, get_s_ins, get_ins_inc

    
class GT_DU:
    def __init__(self, pfunctor):
        self.pfunctor = pfunctor

    def __call__(self, X):
        return self.extend(X)

    def extend(self, X):
        matches = {}
        bigresult = None
        fifo = []
        depth = 0
        cpt = 0

        def add_instance(ins):
            assert ins.occ not in matches
            matches[ins.occ] = ins
            ins.auto = False
            # for s_occ, get_s_ins, _ in self.pfunctor.iter_self_inclusions(ins):
            #     # if s_occ in matches:
            #     #     s_ins = matches[s_occ]
            #     # else:
            #     assert s_occ not in matches
            #     s_ins = get_s_ins()
            #     # ins_inc = get_ins_inc(s_ins)
            #     matches[s_occ] = s_ins

        def add_result(ins):
            res = Result(ins.rhs(), True)
            # results.add(res)
            res.c = cpt
            ins.observe(res, None)
            # for s_occ, get_s_ins, get_ins_inc in self.pfunctor.iter_self_inclusions(ins):
            #     if s_occ in matches:
            #         s_ins = matches[s_occ]
            #     else:
            #         s_ins = get_s_ins()
            #     ins_inc = get_ins_inc(s_ins)
            #     s_ins.observe(res, ins_inc.rhs)
        
        def close(ins):
            nonlocal depth, bigresult
            # print("  " * depth, "close ", ins)
            lm = []
            under = []
            for u_occ, get_u_ins, get_ins_inc in self.pfunctor.iter_under(ins, matches): # iter under
                if u_occ in matches: # instance already encountered
                    u_ins = matches[u_occ]
                    ins_inc = get_ins_inc(u_ins)
                else: # new instance
                    u_ins = get_u_ins()
                    ins_inc = get_ins_inc(u_ins)
                    add_instance(u_ins)
                    if self.pfunctor.is_small(u_ins):
                        fifo.insert(0, u_ins)
                if u_ins.result != None: # already visited by close
                    if u_ins.result.c != cpt: # other wave
                        lm += [u_ins]
                        u_ins.alt_subresult = u_ins.subresult
                        u_ins.alt_result = u_ins.result
                        add_result(u_ins)
                else:
                    depth -= 1
                    lm += close(u_ins)
                    depth += 1
                under += [(u_ins, ins_inc)]
            add_result(ins)
            for u_ins, ins_inc in under: # update subresults under
                # if u_ins.result.c != cpt: # store other result
                #     u_ins.alt_subresult = u_ins.subresult
                #     u_ins.alt_result = u_ins.result
                #     # u_ins.result.obs_by.remove(u_ins)
                #     add_result(u_ins) # work with this one
                #     # print(u_ins.alt_result.rhs, u_ins.result.rhs)
                #     # assert u_ins.alt_result.rhs == u_ins.result.rhs
                if u_ins.subresult == None:
                    new_subresult = ins_inc.rhs() if ins.subresult == None else ins_inc.rhs().compose(ins.subresult)
                    for u_u_ins in u_ins.result.obs_by:
                        if u_ins != u_u_ins:
                            assert u_u_ins.result == u_ins.result
                            u_u_ins.observe(ins.result, new_subresult if u_u_ins.subresult == None else u_u_ins.subresult.compose(new_subresult))
                    u_ins.observe(ins.result, new_subresult)
                    print(ins.result.obs_by)
                    for i in ins.result.obs_by:
                        assert i.subresult == None or i.subresult.cod == u_ins.result.object
            for s_occ, get_s_ins, get_ins_inc in self.pfunctor.iter_self_inclusions(ins, matches): # add siblings
                if s_occ not in matches:
                    s_ins = get_s_ins()
                    add_instance(s_ins)
                    s_ins.auto = True
            # print("  " * depth, "close ret ", lm)
            return lm
        
        def star(ins):
            nonlocal depth, bigresult
            top = True
            uppercone = []
            for o_occ, get_o_ins, _ in self.pfunctor.pmatch_up(ins, matches):
                top = False
                if o_occ in matches:
                    o_ins = matches[o_occ]
                else:
                    o_ins = get_o_ins()
                    add_instance(o_ins)
                uppercone.append(o_ins)
                if not o_ins.black:
                    depth += 1
                    uppercone += star(o_ins)
                    depth -= 1
                else:
                    uppercone += o_ins.uppercone
            ins.uppercone = uppercone
            ins.black = True
            if top and not ins.auto: # on oublie les automorphismes des tops
                lm = close(ins)
                if len(lm) > 0:
                    # print(lm)
                    r_new, _ = Result.multi_merge_2(lm, self.pfunctor.CD, matches)
                    if len(r_new) > 0:
                        bigresult = r_new[0]
                        r_new[0].c = cpt - 1
                elif bigresult == None:
                    bigresult = ins.result
            return uppercone

        for get_s_ins in self.pfunctor.next_small(X):
            s_ins = get_s_ins()
            add_instance(s_ins)
            fifo.insert(0, s_ins)
            break

        while len(fifo) > 0:
            small_ins = fifo.pop()
            # print()
            # print("FIFO POP")
            # print()
            star(small_ins)
            # for match in matches:
            #     print(matches[match])
            #     print(matches[match].result)
            # print()
            for dep_ins in small_ins.uppercone:
                if dep_ins.decrNbDep():
                    # if len(dep_ins.result.obs_by) == 0:
                    #     assert False # should remove result
                    del matches[dep_ins.occ]
            # small_ins.result.obs_by.remove(small_ins)
            del matches[small_ins.occ]
            cpt += 1
        
        return bigresult