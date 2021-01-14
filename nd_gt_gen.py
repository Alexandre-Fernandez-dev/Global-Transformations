from Graph import Graph, GraphM, GraphO

class Small_Cat:
    class Generator:
        class Hs_inc:
            def __init__(self, o_a, o_b, inc):
                self.o_a = o_a
                self.o_b = o_b
                self.inc = inc
            
            def name(self):
                return self.inc.name
            
            def set_name(self, name):
                self.inc.name = name
            
            def compose(self, other):
                return Small_Cat.Generator.Hs_inc(self.o_a, other.o_b, self.inc.compose(other.inc))

            def __repr__(self):
                return str(self.o_a) + " => " + str(self.o_b) + " : " + str(self.inc)
            
            def __hash__(self):
                return hash(self.inc)
            
            def __eq__(self, other):
                return self.o_a == other.o_a and self.o_b == other.o_b and self.inc == other.inc

        def __init__(self, CS, CD):
            # self.gl_gen = GraphO()
            # self.gl_free = None
            # self.m_l_gen_free = None
            # self.level_r = { }
            # self.max_level = 0
            # self.r_nl = { } # rule -> node in gl
            # self.i_el = { } # lhs_inc -> edge in gl
            # # should be stocked in the graph structure \/
            # self.nl_r = { } # node in gl -> rule
            # self.el_i = { } # edge in gl -> lhs_inc
            # #
            # self.CS = CS
            # self.CD = CD
            self.g_gen = GraphO()
            self.g_free = None
            self.inc_gen_free = None
            self.level_r = { }
        
        def add_generator_rule(self, lhs, rhs, level):
            r = RuleSet.Rule(lhs, rhs)
            nl = self.gl_gen.add_node()
            nr = self.gr.add_node()
            self.r_nl[r] = nl
            self.r_nr[r] = nr
            self.nl_r[nl] = r
            self.nr_r[nr] = r
            l_list = self.level_r.setdefault(level, [])
            if level > self.max_level:
                self.max_level = level
            l_list.append(r)
            return r
        
        def add_lhs_inc(self, g_a, g_b, lhs):
            i = self.Hs_inc(g_a, g_b, lhs)
            el = self.gl_gen.add_edge(self.r_nl[g_a], self.r_nl[g_b])
            self.i_el[i] = el
            self.el_i[el] = i
        
        def add_rhs_inc(self, g_a, g_b, rhs):
            i = self.Hs_inc(g_a, g_b, rhs)
            er = self.gr.add_edge(self.r_nr[g_a], self.r_nr[g_b])
            self.i_er[i] = er
            self.er_i[er] = i
        