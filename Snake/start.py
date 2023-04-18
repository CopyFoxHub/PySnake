import pygame
from random import randrange
from bot import Brains


class Snake:

    def __init__(self, window_size: int, window_name: str, pixel_size: int) -> None:
        """Старт программы"""

        # Инициализация PyGame
        pygame.init()
        pygame.display.set_caption(window_name)  # Название окна

        # Инициализация базовых переменных
        self.window_size: int = window_size  # Размер окна
        self.pixel_size: int = pixel_size  # Размер клетки
        self.steps: int = 0  # Количество шагов обучения
        self.mode: int = 1  # Режим игры

        # Координаты головы змейки
        self.x: int = 0
        self.y: int = 0

        # Координаты яблока
        self.apple: tuple = ()

        # Настройки игры
        self.lenght: int = 0  # Длина змейки
        self.fps: int = 0  # Частота обновления игры
        self.snake: list = []  # Список звеньев змейки
        self.direction: int = 0  # Направление движения

        # Переменные для работы с PyGame
        self.display = pygame.display.set_mode((self.window_size, self.window_size))  # Дисплей
        self.clock = pygame.time.Clock()  # Частота обновления кадров
        self.font = pygame.font.SysFont("Comic Sans MS", 30)  # Шрифт программы

        # Таблицы
        self.label_score = None  # Счётчик яблок
        self.label_steps = None  # Количество попыток обучения

        # Первая игра
        self.start()

    def start(self) -> None:
        """Начало новой игры"""

        # Начальная позиция змейки
        self.x = randrange(0, self.window_size, self.pixel_size)
        self.y = randrange(0, self.window_size, self.pixel_size)

        # Начальная позиция яблока
        self.apple = (randrange(0, self.window_size, self.pixel_size),
                      randrange(0, self.window_size, self.pixel_size))

        # Начальные настройки игры
        self.lenght = 1  # Только голова
        self.fps = 5  # Медленное начало
        self.snake = [(self.x, self.y)]  # Змейка состоит только из головы
        self.direction = 0  # Змейка стоит на месте

        # Увеличение количества попыток
        self.steps += 1

        # Изменение надписи таблиц
        self.label_score = self.font.render(f"Счёт: {self.lenght - 1}", True, (255, 255, 255))  # Очки/яблоки
        self.label_steps = self.font.render(f"Попытка: {self.steps}", True, (255, 255, 255))  # Шаги

    def move(self) -> None:
        """Движение в каком-то направление"""

        # Движение вверх
        if self.direction == -2:
            self.y -= self.pixel_size

        # Движение вниз
        elif self.direction == -1:
            self.y += self.pixel_size

        # Движение влево
        elif self.direction == 1:
            self.x -= self.pixel_size

        # Движение вправо
        elif self.direction == 2:
            self.x += self.pixel_size

        # Добавление звена в змейку
        self.snake.append((self.x, self.y))  # Добавление новой координаты
        self.snake = self.snake[-self.lenght:]  # Удаление лишней координаты

    def eat_apple(self) -> None:
        """Змейка съела яблоко"""

        # Генерация нового яблока
        self.apple = (randrange(0, self.window_size, self.pixel_size),
                      randrange(0, self.window_size, self.pixel_size))
        # Изменения в игре
        self.lenght += 1  # Увеличение длины змейки
        self.fps += 1  # Увеличение скорости

        # Изменение в таблице
        self.label_score = self.font.render(f"Счёт: {self.lenght - 1}", True, (255, 255, 255))

    def user_read(self) -> None:
        """Чтение движений человека"""

        # Проверка событий пользователя
        for event in pygame.event.get():

            # Выход при нажатии на крестик
            if event.type == pygame.QUIT:
                exit()

            # Отклик при нажатии на клавишу
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w:  # Движение вперёд
                    self.direction = -2

                elif event.key == pygame.K_s:  # Движение назад
                    self.direction = -1

                elif event.key == pygame.K_a:  # Движение влево
                    self.direction = 1

                elif event.key == pygame.K_d:  # Движение вправо
                    self.direction = 2

                elif event.key == pygame.K_r:  # Начать игру заново
                    self.start()

                elif event.key == pygame.K_m:  # Изменить режим игры
                    self.mode = 0  # Новая переменная режима
                    self.steps = 0
                    self.start()

    def update(self) -> None:
        """Обновление экрана"""

        # Закрашивание старых текстур
        self.display.fill(color=pygame.Color("black"))

        # Отрисовка яблока
        pygame.draw.rect(self.display, pygame.Color("red"), (*self.apple, self.pixel_size, self.pixel_size))

        # Отрисовка змейки
        [(pygame.draw.rect(self.display, pygame.Color('green'),
                           (i, j, self.pixel_size, self.pixel_size))) for i, j in self.snake]

        # Отрисовка таблиц
        self.display.blits([(self.label_score, (0, 0)), (self.label_steps, (0, 40))])

        # Обновление экрана
        pygame.display.flip()


# Запуск программы
if __name__ == "__main__":

    # Переменные окна
    window_size = 600  # Размер окна
    pixel_size = 60  # Размер пикселя
    window_name = "Змейка"  # Название окна

    # Объект для управления игрой
    snake = Snake(window_size=window_size, pixel_size=pixel_size, window_name=window_name)

    # Объект для управления мозгами
    bot = Brains(window_size=window_size, pixel_size=pixel_size)

    # Главный цикл
    while True:

        # Выбор движения
        if snake.mode:  # Если играет человек
            snake.user_read()

        else:  # Если играет алгоритм

            #  Получение направления от мозгов
            snake.direction = bot.crossroads((snake.x, snake.y))

            # Считывание событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Выход из игры
                    exit()
                # Считывание кнопок
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_m:  # Изменение режима
                        snake.steps = 0
                        snake.mode = 1
                        bot.restart()
                        snake.start()

                    elif event.key == pygame.K_r:  # Начать игру заново
                        bot.restart()
                        snake.start()

                    elif event.key == pygame.K_EQUALS:  # Увеличение скорости
                        snake.fps += 10
                    elif event.key == pygame.K_MINUS:  # Понижение скорости
                        snake.fps = (snake.fps - 10 if snake.fps > 11 else 1)

        # Изменение положения змейки
        snake.move()

        # Отрисовка положения змейки
        snake.update()

        # Игровые события
        if snake.snake[-1] == snake.apple:  # Голова змейки съела яблоко
            snake.eat_apple()  # Изменение параметров

        elif (snake.x < 0) or (snake.x > snake.window_size - snake.pixel_size):  # Вышли за границу по X
            if snake.mode:  # Если играет человек
                snake.start()  # Запуск новой сессии
            else:  # Если играет алгоритм
                bot.restart()
                snake.start()
            continue

        elif (snake.y < 0) or (snake.y > snake.window_size - snake.pixel_size):  # Вышли за границу по Y
            if snake.mode:  # Если играет человек
                snake.start()  # Запуск новой сессии
            else:  # Если играет алгоритм
                bot.restart()
                snake.start()
            continue

        elif len(snake.snake) != len(set(snake.snake)):  # Врезались в себя
            if snake.mode:  # Если играет человек
                snake.start()  # Запуск новой сессии
            else:  # Если играет алгоритм
                bot.restart()
                snake.start()
            continue

        # Изменение скорости
        snake.clock.tick(snake.fps)
