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

if __name__ == "__main__":
    n = 3

    parens_list = valid_parens(n)
    print(f"{len(parens_list)} total combinations of valid parens.")

    if True:
        for paren in parens_list:
            print(paren)