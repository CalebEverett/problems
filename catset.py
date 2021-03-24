# Write a function that takes a list of pairs of cats who are living together,
# and two cat names X and Y, and returns a boolean indicating if X and Y are
# living together.

# Example,

# cat_pairs = [
#    ('Myu', 'Boxes'),
#    ('Bounces', 'Felix'),
#    ('Sam', 'Felix'),
#    ('Boxes', 'Jax'),
#    ('Quinn', 'Bounces'),
# ]

# cats_together(cat_pairs, 'Myu', 'Boxes') -> True
# cats_together(cat_pairs, 'Bounces', 'Sam') -> True
# cats_together(cat_pairs, 'Bounces', 'Boxes') -> False
# cats_together(cat_pairs, 'Cat Not In The List', 'Felix') -> False

# Q1. What is the time complexity of your function?
# =============================================================================


from collections import defaultdict
from functools import partial
from hashlib import new
from random import randint
from typing import List, Optional, Tuple
from timeit import timeit


def cats_together(
    cat_pairs: List[Tuple[str]], cat0: str, cat1: str, return_sets: bool = False
) -> bool:
    """Returns True if cat0 and cat1 are together."""

    query_pair = set((cat0, cat1))
    cat_sets = list(map(set, cat_pairs))
    flag = True
    while flag:
        flag = False
        for i, set0 in enumerate(cat_sets):
            for set1 in cat_sets[i + 1 :]:
                if set0.intersection(set1):
                    flag = True

                    # Update in place to avoid using additional memory
                    # for temporary list.
                    set0.update(set1)

                    # Once set has been added to earlier set, don't evaluate it
                    # again. It will be evaluated as part of merged set on next
                    # iteration of while loop
                    cat_sets.remove(set1)

    if return_sets:
        return any([query_pair.issubset(s) for s in cat_sets]), cat_sets
    else:
        return any([query_pair.issubset(s) for s in cat_sets])


# https://www.geeksforgeeks.org/generate-graph-using-dictionary-python/
# https://www.geeksforgeeks.org/difference-between-bfs-and-dfs/
def cats_together_graph(
    cat_pairs: List[Tuple[str, str]],
    cat0: str,
    cat1: str,
    graph: dict = None,
    return_graph: bool = False,
) -> bool:
    """Treats cat_pairs as edges in graph with cats as nodes. Searches recursively
    depth first for a path from cat0 to cat1 and returns True if successful
    and False otherwise. Depth first because of the way recursion works, suspending
    the frame in which find_path is called until it returns, resulting in the
    explortation of the first related node in each recursive call before evaluating
    subsequent related nodes.
    """

    if graph is None:
        graph = defaultdict(list)
        for pair in cat_pairs:
            graph[pair[0]].append(pair[1])
            graph[pair[1]].append(pair[0])

    def find_path(start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        for node in graph[start]:
            if node not in path:
                newpath = find_path(node, end, path)
                if newpath:
                    return newpath

    together = find_path(cat0, cat1) is not None

    if return_graph:
        return together, graph
    else:
        return together


def evaluate(func, cat_pairs, test_pairs, test_results, n=1000):
    t = timeit(
        lambda: [func(cat_pairs, *p) for p in test_pairs] == test_results,
        number=n,
    )
    print(
        f"{func.__name__}: average of {(t/n)*1e6:0.0f}\N{MICRO SIGN}s per {len(test_pairs)} test pairs."
    )


def generate_cat_pairs(max_cat=500, n_pairs=200):
    def randcat_pair():
        return str(randint(1, max_cat)), str(randint(1, max_cat))

    return [randcat_pair() for _ in range(n_pairs)]


if __name__ == "__main__":
    cat_pairs = [
        ("Myu", "Boxes"),
        ("Bounces", "Felix"),
        ("Sam", "Felix"),
        ("Boxes", "Jax"),
        ("Quinn", "Bounces"),
    ]

    test_pairs = [
        ("Myu", "Boxes"),
        ("Bounces", "Sam"),
        ("Bounces", "Boxes"),
        ("Cat Not In The List", "Felix"),
    ]
    test_results = [True, True, False, False]

    evaluate_small = partial(
        evaluate, cat_pairs=cat_pairs, test_pairs=test_pairs, test_results=test_results
    )

    eval_funcs = [cats_together, cats_together_graph]

    # Not really much of a difference in duration in absolute terms small number or pairs
    print("\nEvaluating small number of pairs...")
    for func in eval_funcs:
        evaluate_small(func)

    # Let's see what happens with larger number of pairs
    new_cat_pairs = generate_cat_pairs()
    new_test_pairs = generate_cat_pairs(n_pairs=4)

    evaluate_bigger = partial(
        evaluate, cat_pairs=new_cat_pairs, test_pairs=new_test_pairs, test_results=None
    )

    print("\nEvaluating bigger number of pairs...")
    for func in eval_funcs:
        evaluate_bigger(func)

    # That makes the difference more significant. Let's see if that is because of the time
    # it takes to build the sets or graph or the serach of each.

    _, new_cat_sets = cats_together(
        cat_pairs=new_cat_pairs, cat0="1", cat1="2", return_sets=True
    )

    print("\nEvaluating search time wihtout graph/set generation...")
    evaluate(cats_together, new_cat_sets, new_test_pairs, None)

    _, graph = cats_together_graph(
        cat_pairs=new_cat_pairs, cat0="1", cat1="2", return_graph=True
    )

    # had to do this instead of partial to pick up func name in evaluate
    def cat_together_graph_with_graph(*args, **kwargs):
        kwargs["graph"] = graph
        return cats_together_graph(*args, **kwargs)

    evaluate(cat_together_graph_with_graph, new_cat_pairs, new_test_pairs, None)

    # Turns out, that the search time is much faster with the graph, it is essentially
    # the same time per search regardless of graph size. The graph can also be created
    # much faster than the set.
