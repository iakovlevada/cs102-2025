from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    x_remove, y_remove = x, y
    random_direction = choice(("up", "right"))
    cols = len(grid[0])
    if random_direction == "up" and x - 2 >= 0:
        x_remove, y_remove = x - 1, y
    else:
        random_direction = "right"

    if random_direction == "right" and y + 1 < cols - 1:
        x_remove, y_remove = x, y + 1
    elif x - 2 >= 0:
        x_remove, y_remove = x - 1, y
    grid[x_remove][y_remove] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for cell in empty_cells:
        x, y = cell
        grid = remove_wall(grid, (x, y))

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"
    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    exits = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if grid[x][y] == "X":
                exits.append((x, y))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    rows = len(grid)
    cols = len(grid[0])
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if grid[x][y] == k:
                if x + 1 < rows and grid[x + 1][y] == 0:
                    grid[x + 1][y] = k + 1
                if x - 1 >= 0 and grid[x - 1][y] == 0:
                    grid[x - 1][y] = k + 1
                if y + 1 < cols and grid[x][y + 1] == 0:
                    grid[x][y + 1] = k + 1
                if y - 1 >= 0 and grid[x][y - 1] == 0:
                    grid[x][y - 1] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """

    def neighbors(grid, coord, k):
        rows = len(grid)
        cols = len(grid[0])
        x, y = coord
        if x + 1 < rows and grid[x + 1][y] == k - 1:
            return (x + 1, y)
        if x - 1 >= 0 and grid[x - 1][y] == k - 1:
            return (x - 1, y)
        if y + 1 < cols and grid[x][y + 1] == k - 1:
            return (x, y + 1)
        if y - 1 >= 0 and grid[x][y - 1] == k - 1:
            return (x, y - 1)

    path = []
    current = exit_coord
    max_k = grid[current[0]][current[1]]
    path.append(exit_coord)
    while int(grid[current[0]][current[1]]) > 1:
        neighbor = neighbors(grid, current, grid[current[0]][current[1]])
        path.append(neighbor)
        current = neighbor
    if len(path) != max_k:
        x_error, y_error = path[1]
        grid[x_error][y_error] = 0
        return shortest_path(grid, exit_coord)
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    rows = len(grid)
    cols = len(grid[0])
    x, y = coord
    if x == 0 and y == 0 or x == 0 and y == cols - 1 or x == rows - 1 and y == 0 or x == rows - 1 and y == cols - 1:
        return True
    elif (
        x == 0
        and grid[x + 1][y] != " "
        or x == rows - 1
        and grid[x - 1][y] != " "
        or y == 0
        and grid[x][y + 1] != " "
        or y == cols - 1
        and grid[x][y - 1] != " "
    ):
        return True
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """
    exits = get_exits(grid)
    if len(exits) < 1:
        return grid, None
    if len(exits) == 1:
        return grid, exits[0]
    if encircled_exit(grid, exits[0]) or encircled_exit(grid, exits[1]):
        return grid, None
    grid_copy = deepcopy(grid)
    for x, row in enumerate(grid_copy):
        for y, _ in enumerate(row):
            if grid_copy[x][y] == " " or grid_copy[x][y] == "X":
                grid_copy[x][y] = 0
    x, y = exits[0]
    grid_copy[x][y] = 1
    k = 1
    x_exit, y_exit = exits[1]
    while True:
        almost_solved = make_step(grid_copy, k)
        k += 1
        if int(grid_copy[x_exit][y_exit]) > 0:
            break
    path = shortest_path(grid_copy, exits[1])
    return grid_copy, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
