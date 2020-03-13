from DataStructure import DataStructure

class Array2D():

    def __init__(self, row, col, f):
        assert row >= 0 and col >= 0
        self.row = row
        self.col = col
        if callable(f):
            self.data = [ f(n // col, n % col) for n in range(0, row * col) ]
        else:
            print(len(f), f, row, col)
            assert len(f) == row * col
            self.data = f

    def __repr__(self):
        r = "["
        for i in range(0,self.row):
            r += " ["
            for j in range(0,self.col):
                r += ' ' + repr(self[i,j])
            r += ' ]'
        r += ' ]'
        return r

    def __getitem__(self, c):
        i,j = c
        return self.data[i * self.col + j]

    def __setitem__(self, c, v):
        i,j = c
        self.data[i * self.col + j] = v

    def get_row(self, i):
        return [ self[i,j] for j in range(0, self.col) ]

    def get_col(self, j):
        return [ self[i,j] for i in range(0, self.row) ]

    def __copy__(self):
        return Array2D(self.row, self.col, lambda i, j: self[i,j])

    def subminor(self, i, j):
        def fill_subminor(mm,xi,xj):
            ii = 0
            jj = 0
            for i in range(0, self.row):
                if i != xi:
                    jj = 0
                    for j in range(0,self.col):
                        if j != xj:
                            mm[ii,jj] = self[i,j]
                            jj += 1
                    ii += 1

        mm = Array2D(self.row-1, self.col-1, lambda i,j: None)
        fill_subminor(mm,i,j)
        return mm

    def swap_row(self, i, j):
        for k in range(0, self.col):
            tmp = self[i,k]
            self[i,k] = self[j,k]
            self[j,k] = tmp

    def swap_col(self, i, j):
        for k in range(0, self.row):
            tmp = self[k,i]
            self[k,i] = self[k,j]
            self[k,j] = tmp

    def sub(self, starti, startj, leni, lenj):
        return Array2D(leni, lenj, lambda i, j: self[starti+i, startj+j]);

    def transpose(self):
        return Array2D(self.col, self.row, lambda i, j: self[j,i])

    @staticmethod
    def append(a):
        col = a[0].col
        row = 0
        data = []
        for m in a:
            row += m.row
            data += m.data
        return Array2D(row,col,data)

    def concat(self):
        # sz = Array2D(self.row, self.col, [ (m_ij.row, m_ij.col) for m_ij in self.data ])
        return Array2D.append([ Array2D.append(
            [ self[i,j] for i in range(0,self.row) ]
        ).transpose() for j in range(0,self.col) ]).transpose()

# let append a =
#   { row = Array.fold_right (fun m acc -> acc + (row m)) a 0;
#     col = (col a.(0));
#     data = Array.concat (Array.to_list (Array.map data a));
#   }






class Presentation():

    def __init__(self, d, relators):
        assert all(len(r) == d for r in relators)

        nb_rel = len(relators)

        m = Array2D(d, nb_rel, lambda i, j: relators[j][i])

        def smith(b):
            l    = Array2D(b.row, b.row, lambda i, j: 1 if i == j else 0)
            r    = Array2D(b.col, b.col, lambda i, j: 1 if i == j else 0)
            linv = Array2D(b.row, b.row, lambda i, j: 1 if i == j else 0)
            rinv = Array2D(b.col, b.col, lambda i, j: 1 if i == j else 0)
            a    = copy(b)
            mmm  = min(b.row, b.col)

            def add_alpha_row(m, alpha, i, j):
                for k in range(0, m.col):
                    m[j,k] += alpha * m[i,k]

            def add_alpha_col(m, alpha, i, j):
                for k in range(0, m.row):
                    m[k,j] += alpha * m[k,i]

            def step1(t):
                # Step 1: find pivot / stop if no non null ij
                piv = None
                x = t
                y = t
                allzero = True
                def ltpiv(saij):
                    if piv is None:
                        return True
                    else:
                        return saij < piv
                for i in range(t, a.row):
                    for j in range(t, a.col):
                        aij = a[i,j]
                        if aij != 0:
                            allzero = False
                            saij = abs(aij)
                            if ltpiv(saij):
                                piv = saij
                                x = i
                                y = j
                if allzero:
                    raise Exception()
                if x != t:
                    a.swap_row(x,t)
                    l.swap_row(x,t)
                    linv.swap_col(t,x)
                else:
                    a.swap_col(y,t)
                    r.swap_col(y,t)
                    rinv.swap_row(t,y)

            def step2(t,i):
                # Step 2: Annulation of the tth column
                if i < a.row:
                    att = a[t,t]
                    ait = a[i,t]
                    quo = ait // att
                    rem = ait % att
                    add_alpha_row(a, -quo, t, i)
                    add_alpha_row(l, -quo, t, i)
                    add_alpha_col(linv, quo, i, t)
                    if rem != 0:
                        step2(t,i+1)
                    else:
                        a.swap_row(t, i)
                        l.swap_row(t, i)
                        linv.swap_col(t, i)
                        step2(t,i)
                else:
                    step3(t,t+1)

            def step3(t,j):
                # Step 3: Annulation of the tth row
                if j < a.col:
                    att = a[t,t]
                    atj = a[t,j]
                    quo = atj // att
                    rem = atj % att
                    add_alpha_col(a, -quo, t, j)
                    add_alpha_col(r, -quo, t, j)
                    add_alpha_row(rinv, quo, j, t)
                    if rem != 0:
                        step3(t,j+1)
                    else:
                        a.swap_col(t, j)
                        r.swap_col(t, j)
                        rinv.swap_row(t, j)
                        step2(t,t+1)

            def step4(t):
                # Step 4: aij multiple of att
                c = t
                att = a[t,t]
                try:
                    for i in range(t+1,a.row):
                        for j in range(t+1,a.col):
                            aij = a[i,j]
                            if (aij % att) == 0:
                                c = j
                                raise Exception()
                    return True
                except:
                    add_alpha_col(a,1,c,t)
                    add_alpha_col(r,1,c,t)
                    add_alpha_row(rinv,-1,t,c)
                    return False

            big_cpt = 0

            def big_step(t):
                if t < mmm:
                    step1(t)
                    step2(t,t+1)
                    step3(t,t+1)
                    s4 = step4(t)
                    big_cpt += 1
                    if s4:
                        big_step(t+1)
                    else:
                        big_step(t)

            try:
                big_step(0)
            except:
                pass
            return (linv, l, a, r, rinv)

        (linv, l, a, rinv, r) = smith(m)
        signature = [ a[i,i] if (i < nb_rel) else 0 for i in range(0,d) ]

        d_trivial = 0
        l_cyclic = []
        d_free = 0
        for p in signature:
            if abs(p) == 1:
                d_trivial += 1
            elif p == 0:
                d_free += 1
            else:
                l_cyclic.append(p)

        d_cyclic = len(l_cyclic)
        torsions = l_cyclic

        if d_free > 0:
            order = 0
        else:
            order = 1
            for p in torsions:
                order *= p

        rank = d_cyclic + d_free + 1

        of_graph = Array2D(2,2,lambda i, j:
            l.sub(d_trivial,0,rank-1,d) if i==0 and j==0 else
            Array2D(rank-1,1,lambda a, b: 0) if i==0 and j==1 else
            Array2D(1,d,lambda a, b: 0) if i==1 and j==0 else
            Array2D(1,1,lambda a, b: 1)
        ).concat()

        to_graph = Array2D(2,2,lambda i, j:
            linv.sub(0,d_trivial,d,rank-1) if i==0 and j==0 else
            Array2D(d,1,lambda a, b: 0) if i==0 and j==1 else
            Array2D(1,rank-1,lambda a, b: 0) if i==1 and j==0 else
            Array2D(1,1,lambda a, b: 1)
        ).concat()

        def bezout(a,b):
            r = a
            r1 = b
            u = 1
            u1 = 0
            v = 0
            v1 = 1
            while(r1 != 0):
                q = r // r1
                rs = r
                us = u
                vs = v
                r = r1
                u = u1
                v = v1
                r1 = rs - q * r1
                u1 = us - q * u1
                v1 = vs - q * v1
            return (r,u,v)

        def gcd(a,b):
            (d,_,_) = bezout(a,b)
            return d

        def lcm(a,b):
            if b != 0:
                return (a * b) // gcd(a,b)
            else:
                return 0

        def gcd_array(a):
            l = len(a)
            res = a[0]
            for i in range(1,l):
                res = gcd(res,a[i])
            return res

        def lcm_array(a):
            l = len(a)
            res = a[0]
            for i in range(1,l):
                res = lcm(res,a[i])
            return res

        def internal_order(tor,c):
            l = len(tor)
            return lcm_array([ 1 if p == 0 else abs(tor[i] // gcd(p,tor[i])) if i < l else 0 for (i,p) in enumerate(c) ])

        def internal_normalize(tor,c):
          for (i,m) in enumerate(tor):
              c[i] = c[i] % m
          return c

        basis = [ internal_normalize(torsions,of_graph.get_col(gen_index)) for gen_index in range(0,d+1) ]

        orders = [ internal_order(torsions,b) for b in basis ][0:d]

        # print(m)
        # print(linv)
        # print(l)
        # print(a)
        # print(rinv)
        # print(r)
        # print(signature)
        # print(d_trivial)
        # print(rank)
        # print(d)
        # print(l_cyclic)
        # print(d_free)
        # print(d_cyclic)
        # print(torsions)
        # print(order)
        # print(of_graph)
        # print(to_graph)
        # print(basis)
        # print(orders)

        self.rank = rank
        self.torsions = torsions
        self.degree = d
        self.order = order
        self.orders = orders
        self.of_graph = of_graph
        self.to_graph = to_graph
        self.basis = basis

    class Position():
        def __init__(self, pres, smith):
            self.pres = self.pres
            self.smith = smith  # TODO: smith(c)
            self.__hash = self.__computeHash()

        def __computeHash():
            h = hash(self.pres)
            for c in self.smith:
                h = 31 * h + c
            return h

        def __hash__(self):
            return self.__hash

        def __eq__(self,other):
            if not isinstance(other,Position):
                return False
            return self.pres is other.pres and self.smith == other.smith

        def __repr__(self):
            res = '|'
            for d in c:
                res += ' ' + repr(d)
            res += ' >'
            return res

        def __add__(self,other):
            if not (isinstance(other,Position) and self.pres is other.pres):
                return None
            # TODO: DO IT
            return __init__(self, self.pres, self.smith)



class GbfO():
    def __init__(self, pres, map):
        self.pres = pres
        self.map = map















# [0, 1, 0,
#  1, 1, 0,
#  0, 0, 1]
# [-1, 1, 0,
#   1, 0, 0,
#   0, 0, 1]
# [0, 1, -1]
# [1]
# [1]


# [ [ [ [ -1 1 0 ]
#       [  1 0 0 ]
#       [  0 0 1 ] ] [ [ ] [ ] [ ] ] ] [ [ [ 0 0 0 ] ] [ [ 1 ] ] ] ]
#
from copy import copy


M = Array2D(3, 5, lambda i, j: 100 * i + j)

MM = copy(M)

print(M.data)
M[2,3] = 666
print(M[2,3])
print(M.data)
print(MM.data)
MM.swap_col(0,2);
print(MM.data)

print(MM.subminor(1,1).data)


G = Presentation(3,[[1,1,-1],[10,0,0]])


##
