from functools import partial
from random import randint
from typing import List


def max_sum(array2d: List[List[int]]) -> int:
    n_col = len(array2d[0])
    n_row = len(array2d)

    rowlist = [sum(array2d[0][0 : i + 1]) for i in range(n_col)]
    for r in range(1, n_row):
        rowlist[0] += array2d[r][0]
        for c in range(1, n_col):
            rowlist[c] = array2d[r][c] + max(rowlist[c - 1], rowlist[c])
    return rowlist[-1]


if __name__ == "__main__":
    n_rows = 2
    n_col = 3
    val_abs_max = 10
    get_val = partial(randint, a=-val_abs_max, b=val_abs_max)
    array2d = [[get_val() for r in range(n_col)] for c in range(n_rows)]

    print("array2d = ")
    if True:
        print(*array2d, sep="\n")
    print("max sum = ", max_sum(array2d))

    print("\narray2d = \n[[-10, 1, 2]]")
    array2d = [[-10, 1, 2]]
    print("max sum = ", max_sum(array2d))
