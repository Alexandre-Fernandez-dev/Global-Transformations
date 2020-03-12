from DataStructure import DataStructure

class Array2D():

    def __init__(self, row, col, f):
        assert row > 0 and col > 0
        self.row = row
        self.col = col
        self.data = [ f(n // col, n % col) for n in range(0, row * col) ]

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

class Presentation():

    def __init__(self, d, relators):
        assert all( all(g < d for g in r) for r in relators)

        nb_rel = len(relators)

        m = Array2D(d, nb_rel, lambda i, j: relators[j][i])

        def smith(b):
            l    = Array2D(b.row, b.row, lambda i, j: 1 if i == j else 0)
            r    = Array2D(b.col, b.col, lambda i, j: 1 if i == j else 0)
            linv = Array2D(b.row, b.row, lambda i, j: 1 if i == j else 0)
            rinv = Array2D(b.col, b.col, lambda i, j: 1 if i == j else 0)
            a    = b.copy()
            m    = min(b.row, b.col)

            def add_alpha_row(m, alpha, i, j):
                for k in range(0, m.col):
                    m[j,k] += alpha * m[i,k]

            def add_alpha_col(m, alpha, i, j):
                for k in range(0, m.row):
                    m[k,j] += alpha * m[k,i]

            def step1(t) =
                # Step 1: find pivot / stop if no non null ij
                piv = None
                x = t
                y = t
                allzero = True
                def ltpiv(saij):
                    if piv is None:
                        return True
                    else
                        return saij < piv


from copy import copy

G = Presentation(3,[[1,1,-1]])


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



##
