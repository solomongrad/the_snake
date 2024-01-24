from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

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
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 17

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """общие атрибуты игровых объектов

    Методы: draw(); accident()"""

    def __init__(
            self,
            position=CENTRE,
            body_color=(0, 0, 0)
    ):
        """Устанавливает необходимые атрибуты

        Параметры:
            position - позиция.
            body_color - цвет.
        """
        self.body_color = body_color
        self.position = position
        self.object = None

    def draw(self):
        """заготовка метода для отрисовки объекта на игровом поле"""
        pass

    def accident(self, object):
        """Проверка на столкновение с объектом.

        Параметры: object - второй объект, с которым
        идёт проверка на столкновение

        Возвращает - булеву переменную (True или False)
        """
        return True if self.position in object else False


class Apple(GameObject):
    """Класс, отвечающий за появление яблока

    Методы: randomize_position(); draw()"""

    def __init__(self,
                 position=CENTRE,
                 body_color=APPLE_COLOR):
        """Устанавливает все параметры класса Apple
           и устанавливает яблоку случайную позицию на игровом поле

        Параметры:
            position - позиция.
            body_color - цвет.
        """
        super().__init__(position, body_color)
        self.randomize_position()
        self.body_color = body_color

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле """
        self.position = [(randint(0, GRID_WIDTH - 1) * GRID_SIZE),
                         (randint(0, GRID_HEIGHT - 1) * GRID_SIZE)]

    # Метод draw класса Apple
    def draw(self, surface=screen):
        """Отрисовывает яблоко на игровой поверхности"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, змейка, в основном отвечающий за её передвижение

    Методы:
        update_direction() - Отвечает за изменение направления змейки
        move() - Отвечает за передвижение змейки
        draw() - Отрисовывает змейку
        get_head_position() - Находит голову змейки
        reset() - Сбрасывает все параметры до исходных
    """

    def __init__(self, position=CENTRE,
                 body_color=SNAKE_COLOR):
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
        """обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions и удаляя
        последний элемент, если длина змейки не увеличилась."""
        head = self.get_head_position()
        # Вычисление новых координат
        new_cords = (
            [(head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
             (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT]
        )
        # new_x = [(head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH]
        # new_y = [(head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT]
        # Запись новых координат в список
        self.positions.insert(0, new_cords)

        # Обработка ситуации "змейка врезается в себя"
        if head in self.positions[2:]:
            self.reset()
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self, surface=screen):
        """отрисовывает змейку на экране, затирая след"""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """сбрасывает змейку в начальное состояние после
        столкновения с собой."""
        self.length = 1
        self.positions = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        list_directions = [RIGHT, LEFT, UP, DOWN]
        self.direction = choice(list_directions)
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """ обрабатывает нажатия клавиш, чтобы
    изменить направление движения змейки"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция, содержащая основной цикл игры"""
    # Инициализация PyGame:
    pygame.init()
    apple = Apple()
    snake = Snake()
    while True:
        handle_keys(snake)
        clock.tick(SPEED)
        snake.update_direction()
        snake.move()
        if apple.accident(snake.positions):
            snake.length += 1
            apple.randomize_position()
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
