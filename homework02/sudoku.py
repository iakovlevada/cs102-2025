"""Решатель Судоку"""

import pathlib
import random
import typing as tp
from copy import deepcopy

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    """Создание списка"""
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print("".join(grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)))
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i:i+n] for i in range(0, len(values), n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row, _ = pos
    return grid[row]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    _, col = pos
    return [g[col] for g in grid]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    row, col = pos
    block_row_start = (row // 3) * 3
    block_col_start = (col // 3) * 3
    block = []
    for i in range(block_row_start, block_row_start + 3):
        for j in range(block_col_start, block_col_start + 3):
            block.append(grid[i][j])
    return block


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i, gr in enumerate(grid):
        for j, g in enumerate(gr):
            if g == ".":
                return (i, j)
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество всех возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> set(values) == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> set(values) == {'2', '5', '9'}
    True
    """
    row = get_row(grid, pos)
    col = get_col(grid, pos)
    block = get_block(grid, pos)
    values=set(row + col + block)
    return {str(i) for i in range(1, 10)} - values


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """Решение пазла, заданного в grid"""
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos = find_empty_positions(grid)
    if pos is None:
        return grid
    row, col = pos
    values = find_possible_values(grid, pos)
    for v in values:
        grid[row][col] = v
        result = solve(grid)
        if result is not None:
            return result
        grid[row][col] = "."
    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """
    Если решение solution верно, то вернуть True, в противном случае False

    >>> check_solution([
    ...     ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
    ...     ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
    ...     ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
    ...     ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
    ...     ["4", "2", "6", "8", "1", "3", "7", "9", "1"],
    ...     ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
    ...     ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
    ...     ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
    ...     ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ... ])
    False
    >>> check_solution([
    ...     ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
    ...     ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
    ...     ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
    ...     ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
    ...     ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
    ...     ["7", ".", "3", "9", "2", "4", "8", "5", "6"],
    ...     ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
    ...     ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
    ...     ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ... ])
    False
    >>> check_solution([
    ...     ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
    ...     ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
    ...     ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
    ...     ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
    ...     ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
    ...     ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
    ...     ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
    ...     ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
    ...     ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
    ... ])
    True
    """
    for r in range(9):
        row = get_row(solution, (r, 0))
        if len(set(row)) != 9 or "." in row:
            return False
    for c in range(9):
        col = get_col(solution, (0, c))
        if len(set(col)) != 9:
            return False
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            block = get_block(solution, (br, bc))
            if len(set(block)) != 9:
                return False
    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    grid = [["."] * 9 for _ in range(9)]
    for i in range(9):
        for j in range(9):
            possible_values = list(find_possible_values(grid, (i, j)))
            random.shuffle(possible_values)
            for value in possible_values:
                grid[i][j] = value
                temp_grid = deepcopy(grid)
                if solve(temp_grid) is not None:
                    break
                grid[i][j] = "."
    N = min(N, 81)
    if N == 81:
        return grid
    all_positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(all_positions)
    result = [["."] * 9 for _ in range(9)]
    for idx in range(N):
        i, j = all_positions[idx]
        result[i][j] = grid[i][j]
    return result


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
