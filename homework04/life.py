import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        grid = [[0] * self.cols for _ in range(self.rows)]
        if randomize:
            for i in range(self.rows):
                for j in range(self.cols):
                    grid[i][j] = random.randint(0, 1)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        y, x = cell
        cells = []
        if x - 1 >= 0 and y - 1 >= 0:
            if self.curr_generation[y - 1][x - 1] == 1:
                cells.append(1)
            else:
                cells.append(0)
        if y - 1 >= 0:
            if self.curr_generation[y - 1][x] == 1:
                cells.append(1)
            else:
                cells.append(0)
        if x + 1 < self.cols and y - 1 >= 0:
            if self.curr_generation[y - 1][x + 1] == 1:
                cells.append(1)
            else:
                cells.append(0)
        if x - 1 >= 0:
            if self.curr_generation[y][x - 1] == 1:
                cells.append(1)
            else:
                cells.append(0)
        if x + 1 < self.cols:
            if self.curr_generation[y][x + 1] == 1:
                cells.append(1)
            else:
                cells.append(0)
        if x - 1 >= 0 and y + 1 < self.rows:
            if self.curr_generation[y + 1][x - 1] == 1:
                cells.append(1)
            else:
                cells.append(0)
        if y + 1 < self.rows:
            if self.curr_generation[y + 1][x] == 1:
                cells.append(1)
            else:
                cells.append(0)
        if x + 1 < self.cols and y + 1 < self.rows:
            if self.curr_generation[y + 1][x + 1] == 1:
                cells.append(1)
            else:
                cells.append(0)
        return cells

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """

        new_grid = [[0] * self.cols for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                neighbours = self.get_neighbours((i, j))
                if self.curr_generation[i][j] == 1:
                    if sum(neighbours) == 2 or sum(neighbours) == 3:
                        new_grid[i][j] = 1
                else:
                    if sum(neighbours) == 3:
                        new_grid[i][j] = 1
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations:
            return self.generations >= self.max_generations
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        file = open(filename, "r")
        l = file.readlines()
        k = 0
        new_grid = []
        while True:
            try:
                s = l[k].strip().split()
                new_grid.append(list(map(int, s)))
                k += 1
            except IndexError:
                break
        file.close()
        rows = len(new_grid)
        cols = len(new_grid[0])
        grid = GameOfLife(size=(rows, cols), randomize=False)
        grid.curr_generation = new_grid
        grid.prev_generation = grid.create_grid()
        return grid

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file = open(filename, "w")
        for rows in self.curr_generation:
            for el in rows:
                file.write(str(el))
            file.write("\n")
        file.close()
