import pygame
import sys
from quest import QuestRoom
from utils import load_image


class Game:
    """Основной класс игры, который отвечает за обработку событий, обновление и отрисовку"""

    def __init__(self):
        """Инициализация игры"""

        # Инициализация pygame
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.font.init()
        pygame.init()

        # Создание окна
        self.screen = pygame.display.set_mode((1086, 720))
        pygame.display.set_caption("Ленина, 17")
        pygame.display.set_icon(load_image("teapot.png"))

        # Создание часов
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        # Создание комнаты
        self.room = QuestRoom()

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
            # Выход из игры
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Нажатие на кнопку мыши
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.room.click(event.pos)
            # Нажатие на клавишу
            elif event.type == pygame.KEYDOWN:
                self.room.key_down(event.key)

    def update(self):
        """Обновление состояния игры"""

        # Обновляем текущую комнату
        self.room.update(self.delta_time)

    def draw(self):
        """Отрисовка игры"""

        # Заполнение экрана черным цветом
        self.screen.fill((0, 0, 0))

        # Отрисовываем текущую комнату
        self.room.draw(self.screen)

        # Обновление экрана
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
