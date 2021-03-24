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


def valid_parens(num=3):
    parens_list = [("(", 1, 0)]
    for level in range(num * 2 - 1):
        level_list = []
        for p in parens_list:
            if p[1] < num:
                level_list.append([p[0] + "(", p[1] + 1, p[2]])
            if p[2] < num and p[1] > p[2]:
                level_list.append([p[0] + ")", p[1], p[2] + 1])
        parens_list = level_list

    return [p[0] for p in parens_list]


# TODO: Research recursive approach using permutations of partitions

# $ https://code.activestate.com/recipes/218332-generator-for-integer-partitions/
def partitions_tuple(n):
    # tuple version
    if n == 0:
        yield ()
        return

    for p in partitions_tuple(n - 1):
        yield (1,) + p
        if p and (len(p) < 2 or p[1] > p[0]):
            yield (p[0] + 1,) + p[1:]


# this doesn't work - misses {'(())(())'} for n = 4, for example
def add_pair(parens=set([""])):
    new_parens = set()
    for p in parens:
        new_parens.add(f"({p})")
        new_parens.add(f"{p}()")
        new_parens.add(f"(){p}")

    return new_parens


def get_parens(n=4):
    parens = set([""])
    for _ in range(n):
        parens = add_pair(parens)

    return parens


def call_valid_parens():
    n = 4

    parens_list = valid_parens(n)
    print(f"{len(parens_list)} total combinations of valid parens.")

    if True:
        for paren in parens_list:
            print(paren)


if __name__ == "__main__":
    call_valid_parens()
    print(get_parens())
    print(set(valid_parens(4)).difference(get_parens(4)))
