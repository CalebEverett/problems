from collections import defaultdict
from typing import List, Tuple
import time

cat_pairs = [
    ("Myu", "Boxes"),
    ("Bounces", "Felix"),
    ("Sam", "Felix"),
    ("Boxes", "Jax"),
    ("Quinn", "Bounces"),
]

# cats_together(cat_pairs, 'Myu', 'Boxes') -> True
# cats_together(cat_pairs, 'Bounces', 'Sam') -> True
# cats_together(cat_pairs, 'Bounces', 'Boxes') -> False
# cats_together(cat_pairs, 'Cat Not In The List', 'Felix') -> False

# Q1. What is the time complexity of your function?


def cats_together(cat_pairs: List[Tuple[str, str]], cat0: str, cat1: str) -> bool:
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

    return any([query_pair.issubset(s) for s in cat_sets])


def cats_together_graph(cat_pairs: List[Tuple[str, str]], cat0: str, cat1: str) -> bool:
    graph = defaultdict(list)
    for pair in cat_pairs:
        graph[pair[0]].append(pair[1])
        graph[pair[1]].append(pair[0])

    # https://www.geeksforgeeks.org/generate-graph-using-dictionary-python/
    def find_path(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        for node in graph[start]:
            if node not in path:
                newpath = find_path(graph, node, end, path)
                if newpath:
                    return newpath

    path = find_path(graph, cat0, cat1)

    return True if path else False


if __name__ == "__main__":
    test_pairs = [
        ("Myu", "Boxes"),
        ("Bounces", "Sam"),
        ("Bounces", "Boxes"),
        ("Cat Not In The List", "Felix"),
    ]
    test_results = [True, True, False, False]

    start = time.perf_counter()
    print([cats_together(cat_pairs, *p) for p in test_pairs] == test_results)
    print(time.perf_counter() - start)

    start = time.perf_counter()
    print([cats_together_graph(cat_pairs, *p) for p in test_pairs] == test_results)
    print(time.perf_counter() - start)
