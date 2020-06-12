import networkx as nx

class Instance():
    def __init__(self, lhs_rule, rhs_rule, nb_dep, occ): # privé à GT
        self.black = False
        self.lhs_rule = lhs_rule
        self.rhs_rule = rhs_rule
        self.nb_dep = nb_dep
        self.occ = occ          # C[rule.lhs, X]
        self.result = None      # Result or None
        self.subresult = None   # C[rule.rhs, self.result.object] or None
        self.uppercone = []
    
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
    def __init__(self, lhs, rhs, s, t):
        self.lhs = lhs
        self.rhs = rhs
        self.s = s
        self.t = t
    
    def __repr__(self):
        return "InsInc : [" + " lhs : " + str(self.lhs) + " ]"

class Result():
    def __init__(self, obj, is_rhs):
        self.object = obj
        self.is_rhs = is_rhs
        self.obs_by = []
    
    @staticmethod
    def triv_merge(res, h, u_res):
        for ins in u_res.obs_by:
            ins.observe(res, h if ins.subresult == None else ins.subresult.compose(h))
        u_res.obs_by = None
        u_res.object = None
        return u_res # to remove of results
    
    @staticmethod
    def multi_merge_2(lm, CD, matches):
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
        return Result.multi_merge(l_old, l_new, res_old, res_new, CD, matches)
    
    @staticmethod
    def multi_merge(l_old, l_new, res_old, res_new, CD, matches):
        # print("MULTI MERGE", len(l_old), len(l_new))
        # print("res", res_old, res_new)
        # all l_old must refer to an instance with result res_old, same for res_new
        for i in matches:
            print(matches[i].result)
        if len(l_old) == 0:
            return [], []
        if res_old.is_rhs:
            assert res_new.is_rhs
            obj, on_old, on_new = CD.multi_merge(l_old, l_new)
            res = Result(obj, False)
            for ins in res_old.obs_by:
                ins.observe(res, on_old if ins.subresult is None else ins.subresult.compose(on_old))
            res_old.obs_by = None
            res_old.object = None
            for ins in res_new.obs_by:
                if ins.result != res: # already set ?
                    ins.observe(res, on_new if ins.subresult is None else ins.subresult.compose(on_new))
            res_new.obs_by = None
            res_new.object = None
            print()
            for i in matches:
                print(matches[i].result)
            return [res], [res_old, res_new]
        else:
            obj, on_new = CD.multi_merge_2_in_1(l_old, l_new)
            for ins in res_new.obs_by:
                if ins.result != res_old:
                    ins.observe(res_old, on_new if ins.subresult is None else ins.subresult.compose(on_new))
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
        return self.l_to_r[ins.lhs_rule] in self.smalls

    def nb_small(self, ins): # could be a bool in ins
        return len(self.small_pred.in_edges(self.l_to_r[ins.lhs_rule]))

    def next_small(self, X):
        for small_rule in self.smalls:
            for small_match in self.CS.pattern_match(small_rule.lhs, X):
                small_match.clean()
                get_s_ins = lambda : Instance(small_rule.lhs, small_rule.rhs, len(self.small_pred.in_edges(small_rule)), small_match)
                yield get_s_ins
    
    def iter_under(self, ins):
        for u_rule, _, u_inc in self.G.in_edges(self.l_to_r[ins.lhs_rule], keys = True):
            u_occ = u_inc.lhs.compose(ins.occ)
            get_u_ins = lambda : Instance(u_rule.lhs, u_rule.rhs, len(self.small_pred.in_edges(u_rule)), u_occ)
            get_ins_inc = lambda u_ins : InstanceInc(u_inc.lhs, u_inc.rhs, u_ins, ins)
            yield u_occ, get_u_ins, get_ins_inc
    
    def pmatch_up(self, ins):
        for _, o_rule, o_inc in self.G.out_edges(self.l_to_r[ins.lhs_rule], keys = True):
            for o_occ in self.CS.pattern_match(o_inc.lhs, ins.occ):
                get_o_ins = lambda : Instance(o_rule.lhs, o_rule.rhs, len(self.small_pred.in_edges(o_rule)), o_occ)
                get_ins_inc = lambda o_ins : InstanceInc(o_inc.lhs, o_inc.rhs, ins, o_ins)
                yield o_occ, get_o_ins, get_ins_inc
    
    def iter_self_inclusions(self, ins):
        rule = self.l_to_r[ins.lhs_rule]
        for inc in rule.iter_self_inclusions():
            s_occ = inc.lhs.compose(ins.occ)
            get_s_ins = lambda : Instance(rule.lhs, rule.rhs, len(self.small_pred.in_edges(rule)), s_occ)
            get_ins_inc = lambda u_ins : InstanceInc(inc.lhs, inc.rhs, u_ins, inc)
            yield s_occ, get_s_ins, get_ins_inc
    
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
            res = Result(ins.rhs_rule, True)
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
            nonlocal depth
            print("  " * depth, "close ", ins)
            lm = []
            under = []
            for u_occ, get_u_ins, get_ins_inc in self.pfunctor.iter_under(ins): # iter under
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
                else:
                    depth -= 1
                    lm += close(u_ins)
                    depth += 1
                under += [(u_ins, ins_inc)]
            add_result(ins)
            for u_ins, ins_inc in under: # update subresults under
                if u_ins.result.c != cpt: # store other result
                    u_ins.alt_subresult = u_ins.subresult
                    u_ins.alt_result = u_ins.result
                    add_result(u_ins) # work with this one
                if u_ins.subresult == None:
                    new_subresult = ins_inc.rhs if ins.subresult == None else ins_inc.rhs.compose(ins.subresult)
                    for u_u_ins in u_ins.result.obs_by:
                        if u_ins != u_u_ins:
                            assert u_u_ins.result == u_ins.result
                            u_u_ins.observe(ins.result, new_subresult if u_u_ins.subresult == None else u_u_ins.subresult.compose(new_subresult))
                    u_ins.observe(ins.result, new_subresult)
            for s_occ, get_s_ins, get_ins_inc in self.pfunctor.iter_self_inclusions(ins): # add siblings
                if s_occ not in matches:
                    s_ins = get_s_ins()
                    add_instance(s_ins)
                    s_ins.auto = True
            print("  " * depth, "close ret ", lm)
            return lm
        
        def star(ins):
            nonlocal depth, bigresult
            top = True
            uppercone = []
            for o_occ, get_o_ins, _ in self.pfunctor.pmatch_up(ins):
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
                    print(lm)
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
            print()
            print("FIFO POP")
            print()
            star(small_ins)
            for match in matches:
                print(matches[match])
                print(matches[match].result)
            print()
            for dep_ins in small_ins.uppercone:
                if dep_ins.decrNbDep():
                    # if len(dep_ins.result.obs_by) == 0:
                    #     assert False # should remove result
                    del matches[dep_ins.occ]
            # small_ins.result.obs_by.remove(small_ins)
            del matches[small_ins.occ]
            cpt += 1
        
        return bigresult