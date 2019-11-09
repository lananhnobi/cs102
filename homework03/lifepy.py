import pygame
from pygame.locals import *
import random
import abc
import time
import copy


class GameOfLife:

    def __init__(self, size, randomize=True, max_generations=False) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.cell_list()
        # Текущее поколение клеток
        self.curr_generation = self.cell_list(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def cell_list(self, randomize=False):
        """ Создание списка клеток.
        :param randomize: Если True, то создается список клеток, где
        каждая клетка равновероятно может быть живой (1) или мертвой (0).
        :return: Список клеток, представленный в виде матрицы
        """
        self.clist = [[random.randint(0, 1) if randomize else 0 for i in range(
                                        self.rows)] for i in range(self.cols)]
        return self.clist

    def get_neighbours(self, cell):
        """ Вернуть список соседей для указанной ячейки
        :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col)
        :return: Одномерный список ячеек, смежных к ячейке cell
        """
        neighbours = []
        cell_row, cell_col = cell
        for row in range(3):
            for col in range(3):
                cur_row, cur_col = cell_row - 1 + row, cell_col - 1 + col

                if(
                    (cur_row, cur_col) != cell and
                    cur_row >= 0 and cur_col >= 0 and
                    cur_col < self.cols and
                    cur_row < self.rows
                ):
                    neighbours.append((cell_row - 1 + row, cell_col - 1 + col))

        return neighbours

    def update_cell_list(self, cell_list):
        """ Выполнить один шаг игры.
        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.
        :param cell_list: Игровое поле, представленное в виде матрицы
        :return: Обновленное игровое поле
        """
        new_clist = [[0 for i in range(self.cols)] for i in range(self.rows)]

        for row in range(self.rows):
            for col in range(self.cols):
                neighbours_count = 0

                for cur_cell in self.get_neighbours((row, col)):
                    if cell_list[cur_cell[0]][cur_cell[1]]:
                        neighbours_count += 1

                if(
                    cell_list[row][col] == 1 and neighbours_count >= 2 and
                    neighbours_count <= 3
                ):
                    new_clist[row][col] = 1
                elif cell_list[row][col] == 0 and neighbours_count == 3:
                    new_clist[row][col] = 1

        self.clist = new_clist
        return self.clist

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = copy.deepcopy(self.curr_generation)
        self.curr_generation = copy.deepcopy(self.update_cell_list(
                                                    self.curr_generation))
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
    def from_file(filename) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid_file = open(filename)

        grid = grid_file.readlines()
        for i in range(len(grid)):
            grid[i] = list(map(int, list(grid[i][0:len(grid[i])-1])))
        life = GameOfLife((len(grid), len(grid[i])))
        life.curr_generation = grid

        grid_file.close()

        return life

    def save(self, filename) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file = open(filename, 'w')
        for row in range(len(self.curr_generation)):
            file.write("".join(map(str, self.curr_generation[row])) + '\n')

        file.close()


class UI(abc.ABC):
    def __init__(self, life: GameOfLife) -> None:
        self.life = life

    @abc.abstractmethod
    def run(self) -> None:
        pass


class GUI(UI):
    def __init__(self, life, cell_size=10, speed=10):
        self.width = 640
        self.height = 480
        self.cell_size = cell_size

        self.screen_size = self.width, self.height

        self.screen = pygame.display.set_mode(self.screen_size)

        self.cell_width = self.width // life.cols
        self.cell_height = self.height // life.rows

        self.speed = speed

        self.is_pause = 0

        super().__init__(life)

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_width):
            pygame.draw.line(
                self.screen,
                pygame.Color('black'),
                (x, 0),
                (x, self.height)
            )
        for y in range(0, self.height, self.cell_height):
            pygame.draw.line(
                self.screen,
                pygame.Color('black'),
                (0, y),
                (self.width, y)
            )

    def draw_grid(self) -> None:
        for line_ind in range(len(life.curr_generation)):
            for cell_ind in range(len(life.curr_generation[line_ind])):
                pygame.draw.rect(
                    self.screen,
                    pygame.Color('green') if (
                                life.curr_generation[line_ind][cell_ind]
                                            )
                    else pygame.Color('white'),
                    (
                        cell_ind * self.cell_width,
                        line_ind * self.cell_height,
                        self.cell_width,
                        self.cell_height
                    )
                )

        self.draw_lines()

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        running = True
        self.draw_grid()

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.is_pause = 1 - self.is_pause

                    elif event.key == pygame.K_RIGHT:
                        if self.is_pause:
                            life.step()

                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

                    row = pos[1] // self.cell_height
                    col = pos[0] // self.cell_width

                    life.curr_generation[row][col] = (
                            1 - life.curr_generation[row][col]
                    )
            if life.is_max_generations_exceeded:
                running = False

            if not self.is_pause and life.is_changing:
                life.step()

            self.draw_grid()
            generation = myfont.render(
                'Поколение: ' + str(life.generations),
                False,
                (0, 0, 0)
            )
            self.screen.blit(generation, (0, 0))
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == '__main__':
    randomize = True


    print('''
            SPACE - поставить паузу
            LEFT  - сделать один шаг во время паузы
        ''')
    size = tuple(map(int, input("(r,c): ").split(',')))
    max_generations = int(input('Максимальное : '))
    print('''
        Сгенерировать случайное поле?
        0 - Нет
        1 - Да
    ''')

    randomize = int(input("0/1: "))

    life = GameOfLife(
        size,
        randomize=randomize,
        max_generations=max_generations
    )
    gui = GUI(life)
    gui.run()
