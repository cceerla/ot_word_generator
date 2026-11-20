import sys
from pysat.examples.rc2 import RC2
from pysat.formula import CNF
from pysat.solvers import Solver

# re-implementing hw2.6 in python because its pretty different from spreadsheets
# and i wanna wrestle w sudoku again

# format:
# src: https://pysathq.github.io/docs/pysat.pdf (page 47)
# p wcnf a      b         c
#        ^#vars ^#clauses ^biggest weight

# var: 81 * row + 9 * col + num means "num is on at row,col"
def var(row, col, num):
    # offset of 1 because 0 is reserved. lmao
    return 9*9*row + 9*col + num + 1

def decode(var):
    var = var - 1
    n = var % 9
    var = var // 9
    c = var % 9
    var  = var // 9
    r = var
    return (r,c,n)

form = CNF()
# sudoku: #vars is 9*9*9 (9 nums, 9 rows, 9 columns)
# clauses: (might just hard code from the actual generated clauses)
# max weight: 1 (since i'm encoding unweighted as wcnf, lmao.)
for r in range(9):
    for c in range(9):
        # at least 1 num per spot
        allPresent = []
        for n in range(9):
            allPresent.append(var(r,c,n))
        form.append(allPresent)
        # only 1 num per spot
        for n in range(8):
            for n2 in range(n+1,9):
                # thank you adrian brasoveanu for teaching me python prints
                form.append([-var(r,c,n), -var(r,c,n2)])
# 1 n per row
for r in range(9):
    for n in range(9):
        for c in range(9):
            for c2 in range(c+1,9):
                # thank you adrian brasoveanu for teaching me python prints
                form.append([-var(r,c,n), -var(r,c2,n)])
# 1 n per col
for c in range(9):
    for n in range(9):
        for r in range(1,8):
            for r2 in range(r+1,9):
                # thank you adrian brasoveanu for teaching me python prints
                form.append([-var(r,c,n), -var(r2,c,n)])
# 1 n per 3x3
for tri_r in range(3):
    for tri_c in range(3):
        for r in range(3):
            for c in range(3):
                for r2 in range(r+1,3):
                    for c2 in range(c+1,3):
                        form.append([-var(r,c,n), -var(r2,c2,n)])
preset = [
    [8,0,0, 0,0,0, 0,0,0],
    [0,0,3, 6,0,0, 0,0,0],
    [0,7,0, 0,9,0, 2,0,0],

    [0,5,0, 0,0,7, 0,0,0],
    [0,0,0, 0,4,5, 7,0,0],
    [0,0,0, 1,0,0, 0,3,0],

    [0,0,1, 0,0,0, 0,6,8],
    [0,0,8, 5,0,0, 0,1,0],
    [0,9,0, 0,0,0, 4,0,0],
    ]
for r in range(9):
    for c in range(9):
        if preset[r][c] != 0:
            # note: internally, nums are 0-8, but the input is 1-9
            # we adjust here
            form.append([var(r,c,(preset[r][c]-1))])


output = [
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    [0,0,0, 0,0,0, 0,0,0],
    ]

#cnf = CNF(from_file='sudoku.cnf')
with Solver(bootstrap_with=form) as solver:
    solver.solve()
    for var in solver.get_model():
        if var > 0:
            guess = decode(var)
            # guess[2] + 1 because the nums are 0-8 internally
            # and 1-9 is expected in the output
            output[guess[0]][guess[1]] = guess[2] + 1
    for r in range(9):
        for c in range(9):
            print(output[r][c], end=' ')
        print('')
