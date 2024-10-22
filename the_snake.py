from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

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
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, содержит общие атрибуты игровых объектов"""

    def __init__(self, position=(SCREEN_CENTER),
                 body_color=BOARD_BACKGROUND_COLOR):
        """Метод инициализирует базовые атрибуты объекта (позиция и цвет)."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод, предназначен для переопределения"""
        """в дочерних классах"""

        pass


class Apple(GameObject):
    """Класс, унаследованный от GameObject, описывающий яблоко"""

    def __init__(self, body_color=APPLE_COLOR):
        """Метод задаёт цвет яблока."""
        super().__init__(self, body_color)
        self.body_color = body_color

    def randomize_position(self, positions):
        """Устанавливает случайное положение яблока на игровом поле"""
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in positions:
                self.position = new_position
                break

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, унаследованный от GameObject, описывающий змейку"""

    def __init__(self, length=1, positions=None, direction=RIGHT,
                 next_direction=None, body_color=SNAKE_COLOR,
                 last=None):
        """Метод инициализирует начальное состояние змейки."""
        super().__init__(self, body_color)
        self.length = length
        self.position = (SCREEN_CENTER)
        if positions is None:
            self.positions = [self.position]
        else:
            self.positions = positions.copy()
        self.direction = direction
        self.next_direction = next_direction
        self.body_color = body_color
        self.last = last

    def update_direction(self):
        """Обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки, добавляя новую голову в начало списка"""
        current_head = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (current_head[0] + dx * GRID_SIZE) % SCREEN_WIDTH,
            (current_head[1] + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        if new_head in self.positions[2:]:
            self.reset()
            return
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране, затирая след"""
        for position in self.positions[1:]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние после столкновения"""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Функция обрабатывает нажатия клавиш,"""
    """изменяет направление движения змейки."""
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
    """Запускает основной игровой цикл игры.
    Функция инициализирует игровое окружение, объекты змейки и яблока
    и запускает основной игровой цикл. В ходе цикла обрабатываются нажатия
    клавиш, обновляется направление и положение змейки, проверяется, не съела
    ли змейка яблоко и не столкнулась ли сама с собой, а также происходит
    перерисовка экрана.
    Игровой цикл продолжается до тех пор, пока игрок не выйдет из игры.
    """
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake(direction=RIGHT)
    apple.randomize_position(snake.position)

    while True:
        clock.tick(SPEED)

        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.update_direction()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        snake.move()

        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()

        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
