import pathlib
import random
import abc
import curses
from copy import deepcopy
from pygame.locals import *

class GameOfLife:

    def __init__(self, size: tuple, randomize: bool=True, max_generations: int=None) -> None:
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

    def create_grid(self, randomize: bool = True) -> list:
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
        grid = [[0] * self.rows for i in range(self.cols)]
        if randomize:
            for i in range(self.cols):
                for j in range(self.rows):
                    grid[i][j] = random.randint(0, 1)
        return grid

    def get_neighbours(self, cell: tuple) -> list:
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
        neighbours = []
        x, y = cell
        for i in range(3):
            for j in range(3):
                nbcols = y -1 + i
                nbrows = x - 1 + j
                if nbcols in range(0, self.cols) and nbrows in range(0, self.rows) and (nbrows != x or nbcols != y):
                    neighbours.append(self.curr_generation[nbrows][nbcols])
        return neighbours

    def get_next_generation(self) -> list:
        """
        Получить следующее поколение клеток.
        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        a = deepcopy(self.curr_generation)
        for i in range(self.rows):
            for j in range(self.cols):
                if sum(self.get_neighbours((i,j))) < 2 or sum(self.get_neighbours((i,j))) > 3:
                    a[i][j] = 0
                elif sum(self.get_neighbours((i,j))) == 3:
                    a[i][j] = 1
        self.curr_generation = a
        return self.curr_generation


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
        count = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.curr_generation[i][j] == 1:
                    count += 1
        if count > self.max_generations:
            return True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.prev_generation != self.curr_generation:
            return True
        return False


    @staticmethod
    def from_file(filename) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        file = open(filename)
        grid = file.readlines()
        for i in range(len(grid)):
            grid[i] = list(map(int, grid[i][0:len(grid[i]) - 2]))
        self.curr_generation = grid
        life = GameOfLife((len(grid[0]),len(grid)))
        file.close()
        return life


    def save(self, filename) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file = open(filename, 'w')
        for i in range(len(self.curr_generation)):
            file.write(str(self.curr_generation[i]) + "/n")
        file.close()
