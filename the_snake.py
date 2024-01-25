from random import choice, randint
from sys import exit

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTRE = [(SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)]

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (50, 50, 50)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 17

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Общие атрибуты игровых объектов

    Методы: draw(); accident()
    """

    def __init__(self, position=CENTRE, body_color=None):
        """Устанавливает необходимые атрибуты

        Параметры:
            position - позиция.
            body_color - цвет.
        """
        self.body_color = body_color
        self.position = position

    def draw(self, surface=screen):
        """Заготовка метода для отрисовки объекта на игровом поле"""
        pass

    def rect_maker(self, position, body_color, surface=screen):
        """Отрисовывает объекты класса

        Параметры:
            position - позиция.
            body_color - цвет.
            surface - объект класса pygame.surface.Surface.
        """
        rect = pg.Rect(
            (position[0], position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(surface, body_color, rect)
        pg.draw.rect(surface, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, отвечающий за появление яблока

    Методы: randomize_position(); draw()
    """

    def __init__(self, position=CENTRE, body_color=APPLE_COLOR):
        """Устанавливает все параметры класса Apple
           и устанавливает яблоку случайную позицию на игровом поле

        Параметры:
            position - позиция.
            body_color - цвет.
        """
        super().__init__(position, body_color)
        self.randomize_position([CENTRE])

    def randomize_position(self, occupied):
        """Устанавливает случайное положение яблока на игровом поле."""
        while self.position in occupied:
            self.position = [(randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                             (randint(0, GRID_HEIGHT - 1) * GRID_SIZE)]

    def draw(self, surface=screen):
        """Отрисовывает яблоко на игровой поверхности."""
        self.rect_maker(self.position, self.body_color)


class Snake(GameObject):
    """Класс, змейка, в основном отвечающий за её передвижение

    Методы:
        update_direction() - Отвечает за изменение направления змейки
        move() - Отвечает за передвижение змейки
        draw() - Отрисовывает змейку
        get_head_position() - Находит голову змейки
        reset() - Сбрасывает все параметры до исходных
    """

    def __init__(self, position=CENTRE, body_color=SNAKE_COLOR):
        """Устанавливает необходимые параметры.

        Параметры:
            position - позиция.
            body_color - цвет.
            length - длина
            positions - список кортежей с координатами каждого элемента змейки
            direction - направление
            next_direction - следующее направление
            last - координаты последнего элемента змейки
        """
        super().__init__(position, body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions и удаляя
        последний элемент, если длина змейки не увеличилась.
        """
        head = self.get_head_position()
        # Вычисление новых координат
        new_cords = (
            [(head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
             (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT]
        )
        self.positions.insert(0, new_cords)
        # Обработка ситуации "змейка врезается в себя"
        if head in self.positions[2:]:
            self.reset()
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self, surface=screen):
        """Отрисовывает змейку на экране, затирая след"""
        # for position in self.positions[:-1]:
        #     rect = (
        #         pg.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
        #     )
        #     pg.draw.rect(surface, self.body_color, rect)
        #     pg.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка змейки
        for position in self.positions:
            self.rect_maker(position, self.body_color)

        # Затирание последнего сегмента
        if self.last:
            self.rect_maker(self.last, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Созвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние после
        столкновения с собой.
        """
        self.length = 1
        self.positions = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.direction = choice([RIGHT, LEFT, UP, DOWN])


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш, чтобы
    изменить направление движения змейки.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit('Программа завершена')
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                exit('Программа завершена')


def draw_lines():
    """Отрисовывает клетки на игровом поле"""
    for i in range(1, GRID_HEIGHT):
        pg.draw.line(
            screen,
            BORDER_COLOR,
            (0, i * GRID_SIZE),
            (SCREEN_WIDTH, i * GRID_SIZE),
            3
        )

    for i in range(1, GRID_WIDTH):
        pg.draw.line(
            screen,
            BORDER_COLOR,
            (i * GRID_SIZE, 0),
            (i * GRID_SIZE, SCREEN_HEIGHT),
            3
        )


def main():
    """Функция, содержащая основной цикл игры."""
    # Инициализация PyGame:
    pg.init()
    snake = Snake()
    apple = Apple()
    apple.draw(screen)
    while True:
        handle_keys(snake)
        clock.tick(SPEED)
        snake.update_direction()
        snake.move()
        if apple.position in snake.positions:
            snake.length += 1
            apple.randomize_position(snake.positions)
        if snake.get_head_position() == snake.positions[2:]:
            apple.draw(screen)
            snake.reset()
        draw_lines()
        apple.draw(screen)
        snake.draw(screen)
        pg.display.update()


if __name__ == '__main__':
    main()
