def create_grid(filled={}):
    grid = [[(0, 0, 0) for _ in range(10)] for i in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in filled:
                c = filled[(j, i)]
                grid[i][j] = c
    return grid


def clear_rows(grid):
    temp_score = 0
    del_row = [i for i, row in enumerate(grid) if (0, 0, 0) not in row]
    if del_row:
        for i in del_row:
            del grid[i]
            grid.insert(0, [(0, 0, 0) for _ in range(10)])
            temp_score += 1
    return temp_score


def is_gameover(grid):
    for col in grid[0]:
        if col != (0, 0, 0):
            return True
    return False
