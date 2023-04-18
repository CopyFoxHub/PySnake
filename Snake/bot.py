class Brains:
    def __init__(self, window_size: int, pixel_size: int) -> None:

        # Базовые переменные
        self.window_size: int = window_size
        self.pixel_size: int = pixel_size

        # Изменяемые переменные
        self.in_position: bool = False  # Змейка находится на старте
        self.step_count: int = 0  # Шаг в списке

        # Список шагов для цикла
        self.step_list: list = [2] + ([-2] * (window_size // pixel_size - 2) + [2] + [-1] * (window_size // pixel_size - 2) + [2]) * (window_size // pixel_size // 2 - 1) + \
                               [-2] * (window_size // pixel_size - 1) + \
                               [1] * (window_size // pixel_size - 1) + [-1] * (window_size // pixel_size - 1)

    def restart(self) -> None:
        """Вернуться в изначальное положение"""

        self.in_position: bool = False
        self.step_count: int = 0

    def crossroads(self, coordinates: tuple) -> int:
        """Выбор шага в зависимости от координат"""

        # Перемещение змейки в изначальную позицию
        if not self.in_position:
            if coordinates[0] != 0:
                return 1
            elif coordinates[1] != self.window_size - self.pixel_size:
                return -1
            else:
                self.in_position = True
        else:
            self.step_count = self.step_count + 1 if self.step_count < len(self.step_list) else 1
            return self.step_list[self.step_count - 1]
