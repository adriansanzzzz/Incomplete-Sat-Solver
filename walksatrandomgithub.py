import random
import sys


def parse(filename):
    clauses = []
    count = 0
    for line in open(filename):
        if line[0] == 'c':
            continue
        if line[0] == 'p':
            n_vars = int(line.split()[2])
            lit_clause = [[] for _ in range(n_vars * 2 + 1)]
            continue

        clause = []
        for literal in line[:-2].split():
            literal = int(literal)
            clause.append(literal)
            lit_clause[literal].append(count)
        clauses.append(clause)
        count += 1
    return clauses, n_vars, lit_clause


# make parse function to make the same as the original code but more fast
def get_random_interpretation(n_vars):
    return [i if random.random() < 0.5 else -i for i in xrange(n_vars + 1)]


# difference between xrange and range
# the range function returns a list, while the xrange function returns an iterator that can be used in a for loop.

def xrange(n):
    return iter(range(n))


def get_true_sat_lit(clauses, interpretation):
    true_sat_lit = [0 for _ in clauses]
    for index, clause in enumerate(clauses):
        for lit in clause:
            if interpretation[abs(lit)] == lit:
                true_sat_lit[index] += 1
    return true_sat_lit


def update_tsl(literal_to_flip, true_sat_lit, lit_clause):
    for clause_index in lit_clause[literal_to_flip]:
        true_sat_lit[clause_index] += 1
    for clause_index in lit_clause[-literal_to_flip]:
        true_sat_lit[clause_index] -= 1


def compute_broken(clause, true_sat_lit, lit_clause, omega=0.4):
    break_min = sys.maxint
    best_literals = []
    for literal in clause:

        break_score = 0

        for clause_index in lit_clause[-literal]:
            if true_sat_lit[clause_index] == 1:
                break_score += 1

        if break_score < break_min:
            break_min = break_score
            best_literals = [literal]
        elif break_score == break_min:
            best_literals.append(literal)

    if break_min == 0:
        return random.choice(clause)
    else:
        return random.choice(best_literals)


def run_sat(clauses, n_vars, lit_clause, max_flips_proportion=4):
    max_flips = n_vars * max_flips_proportion
    while 1:
        interpretation = get_random_interpretation(n_vars)
        true_sat_lit = get_true_sat_lit(clauses, interpretation)
        for _ in xrange(max_flips):

            unsatisfied_clauses_index = [index for index, true_lit in enumerate(true_sat_lit) if
                                         not true_lit]

            if not unsatisfied_clauses_index:
                return interpretation

            clause_index = random.choice(unsatisfied_clauses_index)
            unsatisfied_clause = clauses[clause_index]

            lit_to_flip = compute_broken(unsatisfied_clause, true_sat_lit, lit_clause)

            update_tsl(lit_to_flip, true_sat_lit, lit_clause)

            interpretation[abs(lit_to_flip)] *= -1


if __name__ == '__main__':
    filename = sys.argv[1]
    clauses, n_vars, lit_clause = parse(filename)

    # solve the problem
    run_sat(clauses, n_vars, lit_clause)

    # and return the solution in the format: v SATISFIABLE if the problem is satisfiable, v UNSATISFIABLE otherwise
    if run_sat(clauses, n_vars, lit_clause) is None:
        print("v UNSATISFIABLE")
    else:
        print("v SATISFIABLE")
        print("v", run_sat(clauses, n_vars, lit_clause))
