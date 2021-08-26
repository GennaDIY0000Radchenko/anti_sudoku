def print_matrix(m):
    for x in range(81):
        if m[x // 9][x % 9] == 0:
            print("_", end=" ")
        else:
            print(m[x // 9][x % 9], end=" ")
        if x % 27 == 26:
            print("\n\n", end="")
        elif x % 9 == 8:
            print("\n", end="")
        elif x % 3 == 2:
            print("  ", end="")


def print_m_pos(m_p):
    for x in range(81):
        a = 9 - m_p[x // 9][x % 9].count(0)
        b = 0
        print("[", end="")
        if a == 0:
            print("___", end="")
        else:
            for i in range(9):
                if m_p[x // 9][x % 9][i] != 0 and b + 1 < a:
                    b += 1
                    print(i + 1, ", ", sep="", end="")
                elif b + 1 == a:
                    while m_p[x // 9][x % 9][i] == 0:
                        i += 1
                    print(i + 1, end="")
                    break
        print("]", end="")

        if x % 27 == 26:
            print("\n\n", end="")
        elif x % 9 == 8:
            print("\n", end="")
        elif x % 3 == 2:
            print(" " * 2 * (9 - a), end="")


def clean_p_r_c(m, m_p, r, c):
    m_p[r][c] = [0 for i in range(9)]
    #
    list_of_num_col = []
    for y in range(9):
        if m[y][c] != 0:
            list_of_num_col.append(m[y][c])

    for num_col in range(len(list_of_num_col)):
        for y in range(9):
            if list_of_num_col[num_col] in m_p[y][c]:
                m_p[y][c][list_of_num_col[num_col] - 1] = 0
    #
    list_of_num_row = []
    for x in range(9):
        if m[r][x] != 0:
            list_of_num_row.append(m[r][x])

    for num_row in range(len(list_of_num_row)):
        for x in range(9):
            if list_of_num_row[num_row] in m_p[r][x]:
                m_p[r][x][list_of_num_row[num_row] - 1] = 0
    #
    low_row = (r // 3) * 3
    low_col = (c // 3) * 3

    list_of_num_sqr = []
    for x in range(low_col, low_col + 3):
        for y in range(low_row, low_row + 3):
            if m[x][y] != 0:
                list_of_num_sqr.append(m[x][y])

    for num_sqr in range(len(list_of_num_sqr)):
        for x in range(low_col, low_col + 3):
            for y in range(low_row, low_row + 3):
                if list_of_num_sqr[num_sqr] in m_p[x][y]:
                    m_p[x][y][list_of_num_sqr[num_sqr] - 1] = 0
    #
    return m, m_p


def clean_possible(m, m_p):
    for y in range(9):
        for x in range(9):
            if m[y][x] != 0:
                m, m_p = clean_p_r_c(m, m_p, y, x)

    return m, m_p


def solve_0(m, m_p):
    m, m_p = clean_possible(m, m_p)
    cont = 0
    for row in range(9):
        for col in range(9):
            if m_p[row][col].count(0) == 8:
                cont = 1
                num = 0
                for i in range(9):
                    if m_p[row][col][i] != 0:
                        num = i + 1
                        break
                m[row][col] = num
                m, m_p = clean_p_r_c(m, m_p, row, col)

    if cont:
        return solve_0(m, m_p)
    else:
        return m, m_p


def nowhere_else(m, m_p):
    cont = 0
    for row in range(9):
        d_row = {i: 0 for i in range(1, 10)}
        for c in range(9):
            for i in range(9):
                if m_p[row][c][i] != 0:
                    d_row[i + 1] += 1

        list_of_lonely_num = []
        for i in range(9):
            if d_row[i + 1] == 1:
                cont = 1
                list_of_lonely_num.append(i + 1)

        for lonely in range(len(list_of_lonely_num)):
            for c in range(9):
                if list_of_lonely_num[lonely] in m_p[row][c]:
                    m[row][c] = list_of_lonely_num[lonely]
                    m, m_p = clean_p_r_c(m, m_p, row, c)

    for col in range(9):
        d_col = {i: 0 for i in range(1, 10)}
        for r in range(9):
            for i in range(9):
                if m_p[r][col][i] != 0:
                    d_col[i + 1] += 1

        list_of_lonely_num = []
        for i in range(9):
            if d_col[i + 1] == 1:
                cont = 1
                list_of_lonely_num.append(i + 1)

        for lonely in range(len(list_of_lonely_num)):
            for r in range(9):
                if list_of_lonely_num[lonely] in m_p[r][col]:
                    m[r][col] = list_of_lonely_num[lonely]
                    m, m_p = clean_p_r_c(m, m_p, r, col)

    for r in range(3):
        for c in range(3):
            d_sqr = {i: 0 for i in range(1, 10)}
            for row in range(r * 3, r * 3 + 3):
                for col in range(c * 3, c * 3 + 3):
                    for i in range(9):
                        if m_p[row][col][i] != 0:
                            d_sqr[i + 1] += 1

            list_of_lonely_num = []
            for i in range(9):
                if d_sqr[i + 1] == 1:
                    cont = 1
                    list_of_lonely_num.append(i + 1)

            for lonely in range(len(list_of_lonely_num)):
                for row in range(r * 3, r * 3 + 3):
                    for col in range(c * 3, c * 3 + 3):
                        if list_of_lonely_num[lonely] in m_p[row][col]:
                            m[row][col] = list_of_lonely_num[lonely]
                            m, m_p = clean_p_r_c(m, m_p, row, col)

    if cont:
        return nowhere_else(m, m_p)
    else:
        return m, m_p


def pairs(m, m_p):
    for i in range(81):
        if m[i // 9][i % 9] == 0:
            if 9 - m_p[i // 9][i % 9].count(0) == 2:
                # in column
                find_r = -1
                for r in range(9):
                    if r != (i // 9):
                        find = 1
                        for num in range(9):
                            if m_p[i // 9][i % 9][num] != m_p[r][i % 9][num]:
                                find = 0
                                break
                        if find == 1:
                            find_r = r
                            break
                if find_r != -1:
                    cont = 1
                    list_of_index = []
                    for num in range(9):
                        if m_p[i // 9][i % 9][num] != 0:
                            list_of_index.append(num)
                    for r in range(9):
                        if r != find_r and r != (i // 9):
                            m_p[r][i % 9][list_of_index[0]], m_p[r][i % 9][list_of_index[1]] = 0, 0
                    # if in same sqr
                    if (i // 9) // 3 == find_r // 3:
                        for row in range(((i // 9) // 3) * 3, ((i // 9) // 3) * 3 + 3):
                            for col in range(((i % 9) // 3) * 3, ((i % 9) // 3) * 3 + 3):
                                if row != ((i // 9) or find_r) and col != (i % 9):
                                    m_p[row][col][list_of_index[0]], m_p[row][col][list_of_index[1]] = 0, 0
                # in row
                else:
                    find_c = -1
                    for c in range(9):
                        if c != (i % 9):
                            find = 1
                            for num in range(9):
                                if m_p[i // 9][i % 9][num] != m_p[i // 9][c][num]:
                                    find = 0
                                    break
                            if find == 1:
                                find_c = c
                                break
                    if find_c != -1:
                        cont = 1
                        list_of_index = []
                        for num in range(9):
                            if m_p[i // 9][i % 9][num] != 0:
                                list_of_index.append(num)
                        for c in range(9):
                            if c != find_c and c != (i % 9):
                                m_p[i // 9][c][list_of_index[0]], m_p[i // 9][c][list_of_index[1]] = 0, 0
                        # if in same sqr
                        if (i % 9) // 3 == find_c // 3:
                            for row in range(((i // 9) // 3) * 3, ((i // 9) // 3) * 3 + 3):
                                for col in range(((i % 9) // 3) * 3, ((i % 9) // 3) * 3 + 3):
                                    if col != ((i % 9) or find_c) and row != (i // 9):
                                        m_p[row][col][list_of_index[0]], m_p[row][col][list_of_index[1]] = 0, 0
                # in square
                    else:
                        for row in range(((i // 9) // 3) * 3, ((i // 9) // 3) * 3 + 3):
                            for col in range(((i % 9) // 3) * 3, ((i % 9) // 3) * 3 + 3):
                                if row != (i // 9) and col != (i % 9):
                                    find = 1
                                    for num in range(9):
                                        if m_p[i // 9][i % 9][num] != m_p[row][col][num]:
                                            find = 0
                                            break
                                    if find == 1:
                                        find_r = row
                                        find_c = col
                                        break
                        if find_r != -1 and find_c != -1:
                            cont = 1
                            list_of_index = []
                            for num in range(9):
                                if m_p[i // 9][i % 9][num] != 0:
                                    list_of_index.append(num)
                            for row in range(((i // 9) // 3) * 3, ((i // 9) // 3) * 3 + 3):
                                for col in range(((i % 9) // 3) * 3, ((i % 9) // 3) * 3 + 3):
                                    if (row != ((i // 9) or find_r)) and (col != ((i % 9) or find_c)):
                                        m_p[row][col][list_of_index[0]], m_p[row][col][list_of_index[1]] = 0, 0

    return m, m_p


matrix_possible = [[[p + 1 for p in range(9)] for ii in range(9)] for i in range(9)]

matrix_given = \
    [
        [0, 0, 0, 1, 0, 2, 4, 9, 3],
        [5, 0, 0, 0, 4, 0, 0, 0, 0],
        [0, 9, 0, 7, 0, 0, 8, 0, 0],
        [9, 0, 3, 4, 0, 0, 0, 0, 0],
        [0, 4, 0, 0, 3, 5, 0, 7, 0],
        [0, 0, 5, 0, 0, 8, 9, 3, 0],
        [4, 0, 8, 3, 0, 7, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 7, 0, 0],
        [1, 0, 9, 0, 0, 4, 0, 0, 0],
    ]


# start
print_matrix(matrix_given)
print("-" * 30)

# by rules
matrix_given, matrix_possible = solve_0(matrix_given, matrix_possible)

print_matrix(matrix_given)
print_matrix(matrix_possible)
print("-" * 30)

# by noWhere else
matrix_given, matrix_possible = nowhere_else(matrix_given, matrix_possible)

print_matrix(matrix_given)
print_matrix(matrix_possible)
print("-" * 30)

# by pairs
matrix_given, matrix_possible = pairs(matrix_given, matrix_possible)

print_matrix(matrix_given)
print_matrix(matrix_possible)
print("-" * 30)


print("#"*30)


# by rules
matrix_given, matrix_possible = solve_0(matrix_given, matrix_possible)

print_matrix(matrix_given)
print_matrix(matrix_possible)
print("-" * 30)

# by noWhere else
matrix_given, matrix_possible = nowhere_else(matrix_given, matrix_possible)

print_matrix(matrix_given)
print_matrix(matrix_possible)
print("-" * 30)

# what`s left
print_matrix(matrix_given)
print_m_pos(matrix_possible)
