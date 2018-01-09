import copy


def matrixs(n):
    """
    (int) -> list
    Builds all possible relations on the matrix of n elements
    >>>matrixs(1)
    [[0, 0]]
    >>>matrixs(2)
    [[(0, 0)], [(0, 1)], [(1, 0)], [(1, 1)], [(0, 0), (0, 1)], [(0, 0), (1, 0)]
    , [(0, 0), (1, 1)], [(0, 1), (1, 0)], [(0, 1), (1, 1)], [(1, 0), (1, 1)],[
    (0, 0), (0, 1), (1, 0)], [(0, 0), (0, 1), (1, 1)], [(0, 0), (1, 0), (1, 1)]
    , [(0, 1), (1, 0), (1, 1)], [(0, 0), (0, 1), (1, 0), (1, 1)], []]
    >>>matrixs(0)
    Input n > 0 and integer
    0
    """
    lst = []
    # create matrixs
    if n <= 0 or type(n) != int:
        # if the wrong condition
        print("Input n > 0 and integer")
        return 0
    elif n == 1:
        # if n == 1
        lst.append([0, 0])
        return lst
    else:
        # create relations for n > 1
        for x in range(0, n):
            for y in range(0, n):
                lst.append([(x, y)])
        y = 0
        while len(lst) != 2 ** (2 ** n) - 1:
            for i in range(0, n ** 2 + 1):
                new_lst = []
                if y <= 3:
                    new_lst.append(lst[y][0])
                else:
                    for j in range(len(lst[y])):
                        new_lst.append(lst[y][j])
                if lst[i][0] not in new_lst:
                    new_lst.append(lst[i][0])
                new_lst = sorted(new_lst)
                if new_lst not in lst:
                    lst.append(new_lst)
            y += 1
        lst.append([])
        return lst


def Worshal(lst):
    """
    (list) -> list
    make matrix of transient with Worshall algorithm
    >>> Worshal([[1, 1], [0, 1]])
    [[1, 1], [1, 1]]
    >>> Worshall([[1, 1], [1, 0]])
    [[1, 1], [1, 0]]
    """
    for i in range(len(lst)):
        for j in range(len(lst)):
            if i == j:
                # if i == j then we do not change anything
                pass
            elif lst[j][i] == 1:
                # if i != j and we will add to the element and both the line
                # j item i column and it will be less than 2 then we add in a
                # different situation leave it unchanged
                for k in range(len(lst[i])):
                    if lst[i][k] + lst[j][k] < 2:
                        lst[j][k] = lst[j][k] + lst[i][k]
            else:
                pass
    return lst


def is_transit(n):
    """
    (int) -> int
    counts the number of transient closures
    work slow with n = 4 or more because it takes a long time to create
    relation and then calculate it
    >>>is_transit(2)
    14
    >>>is_transit(3)
    67
    >>>is_transit(0)
    Input n > 0 and integer
    0
    """
    if matrixs(n) == 0:
        # if wrong conditions
        return 0
    # create relations
    all_matrix = matrixs(n)
    k = 0
    for matrix in all_matrix:
        if len(matrix) < 3:
            # check if relations lenght < 3
            k += 1
        else:
            # create new list and make makes a matrix of 0 and 1
            lst_matrix = []
            for i in range(0, len(matrix)):
                new_lst = []
                for j in range(0, len(matrix)):
                    if (i, j) in matrix:
                        new_lst.append(1)
                    else:
                        new_lst.append(0)
                lst_matrix.append(new_lst)
            # then make matrix of transient with Worshall algorithm
            lst_matrix1 = copy.deepcopy(lst_matrix)
            lst_matrix = Worshal(lst_matrix)
            # check if our matrix is transient then it will not change
            if lst_matrix1 == lst_matrix:
                k += 1
    return k
