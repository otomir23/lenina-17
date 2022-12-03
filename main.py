import pygame
import sys


class Game:
    """Основной класс игры, который отвечает за обработку событий, обновление и отрисовку"""

    def __init__(self):
        """Инициализация игры"""

        # Инициализация pygame
        pygame.init()

        # Создание окна
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Unnamed Room Escape Game")

        # Создание часов
        self.clock = pygame.time.Clock()
        self.delta_time = 0

    def run(self):
        """Основной игровой цикл"""

        while True:
            # Обновление часов (60 FPS)
            # delta_time - время, прошедшее с прошлого кадра
            self.delta_time = self.clock.tick(60) / 1000

            # Вызов методов для обработки событий, обновления и отрисовки
            self.events()
            self.update()
            self.draw()

    def events(self):
        """Обработка событий"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        """Обновление состояния игры"""

        # Пока пусто, только вывод FPS
        print(int(1 / self.delta_time))

        # В этом методе будут вызываться методы обновления всех объектов игры
        # Это позволит разделить логику обновления и отрисовки

    def draw(self):
        """Отрисовка игры"""

        # Заполнение экрана черным цветом
        self.screen.fill((0, 0, 0))

        # Обновление экрана
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
