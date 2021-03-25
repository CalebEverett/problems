# Given n pairs of parentheses, write a function to generate all combinations of
# well-formed parentheses.

# For example, given n = 3, a solution set is:

# generate_solutions(n=3)
# ((()))
# (()())
# (())()
# ()(())
# ()()()
# =============================================================================
from itertools import product, permutations
from timeit import timeit


def parens_from_strings(num=3):
    parens_list = [("(", 1, 0)]
    for _ in range(num * 2 - 1):
        level_list = []
        for p in parens_list:
            if p[1] < num:
                level_list.append([p[0] + "(", p[1] + 1, p[2]])
            if p[2] < num and p[1] > p[2]:
                level_list.append([p[0] + ")", p[1], p[2] + 1])
        parens_list = level_list

    return set([p[0] for p in parens_list])


def all_partitions(num):
    partitions = {i: [] for i in range(1, num + 1)}

    def partitions_tuple(n):

        # tuple version
        if n == 0:
            yield ()
            return

        for p in partitions_tuple(n - 1):
            part = (1,) + p
            partitions[n].append(part)
            yield part
            if p and (len(p) < 2 or p[1] > p[0]):
                part = (p[0] + 1,) + p[1:]
                partitions[n].append(part)
                yield part

    _ = list(partitions_tuple(num))

    return partitions


def add_pair(parens=set([""])):
    new_parens = set()
    for p in parens:
        new_parens.add(f"({p})")

    return new_parens


def parens_from_partitions(n=4):
    """This approach builds the valid combinations of parens starting with the partitions
    (ways to sum to a given number) and then using the permutations of the the partitions
    to construct the valid parens from previously constructed valid combinations. Not
    very efficient clearly with three nested loops - perhaps could be improved by getting
    permutations in calc of partitions, but bailing on this since string method is fast.
    """
    partitions = all_partitions(n)
    parens_sets = {0: set([""])}

    for m in range(1, n + 1):
        parens_sets[m] = add_pair(parens_sets[m - 1])
        for k in partitions[m]:
            for p in set(permutations(k)):
                parens_sets[m] = parens_sets[m].union(
                    set(map(("").join, product(*(parens_sets[o] for o in p))))
                )

    return parens_sets[n]


def call_valid_parens(func, n=4):

    parens_list = func(n)
    print(f"{len(parens_list)} total combinations of valid parens.")

    if True:
        for paren in parens_list:
            print(paren)


def evaluate(func, n_parens, n=10):
    t = timeit(
        lambda: func(n_parens),
        number=n,
    )
    print(f"{func.__name__}: average of {(t/n)*1e3:0.0f}ms.")


if __name__ == "__main__":
    for func in [parens_from_strings, parens_from_partitions]:
        evaluate(func, 10)
