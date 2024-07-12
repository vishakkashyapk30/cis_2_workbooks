from re import findall
import numpy as np
from sympy import *

def parse_formula(formula):
    elements = findall(r'([A-Z][a-z]*)(\d*)', formula)
    return {element: (int(count) if count else 1) for element, count in elements}

def balance_equation(lhs, rhs):
    lhs_compounds = lhs.split(' + ')
    rhs_compounds = rhs.split(' + ')

    lhs_elements = [parse_formula(compound) for compound in lhs_compounds]
    rhs_elements = [parse_formula(compound) for compound in rhs_compounds]
    elements = list(set().union(*[compound.keys() for compound in lhs_elements + rhs_elements]))

    A = []
    for compounds in [lhs_elements, rhs_elements]:
        matrix = []
        for element in elements:
            row = []
            for compound in compounds:
                row.append(compound.get(element, 0))
            matrix.append(row)
        A.append(matrix)

    for i in range(len(A)):
        for j in range(len(A[i])):
            while len(A[i][j]) < len(elements):
                A[i][j].append(0)

    A = [np.array(a).T for a in A]
    A = np.concatenate(A, axis=1)

    x = symbols(' '.join(['x{}'.format(i) for i in range(len(A[0]))]))
    system = [Eq(sum(row[:len(lhs_compounds)]), sum(row[len(lhs_compounds):])) for row in A]
    solution = solve(system, x)

    if isinstance(solution, dict):
        return [solution[symbol] for symbol in x]
    else:
        return solution

lhs = 'H2 + O2'
rhs = 'H2O'
print(balance_equation(lhs, rhs))