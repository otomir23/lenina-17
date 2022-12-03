import pygame
import sys
from room import RoomObject, InteractableRoomObject, Room
from utils import load_image


class Game:
    """Основной класс игры, который отвечает за обработку событий, обновление и отрисовку"""

    def __init__(self):
        """Инициализация игры"""

        # Инициализация pygame
        pygame.init()

        # Создание окна
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Безымянная игра")

        # Создание часов
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        # Создание комнаты
        self.room = Room()

        # Добавление тестовых объектов
        s = pygame.transform.scale(load_image('h.jpg'), (200, 200))

        a = InteractableRoomObject(s, (100, 100))
        a.click_hook = lambda obj, pos: print("тулуз нажат !", pos)

        b = RoomObject(s, (200, 100))
        b.update_hook = lambda obj, dt: print("тулуз на экране !", int(1 / dt), "FPS")

        c = RoomObject(s, (300, 100))
        d = RoomObject(s, (400, 100))

        self.room.add_objects(a, wall=0)
        self.room.add_objects(b, wall=1)
        self.room.add_objects(c, wall=2)
        self.room.add_objects(d, wall=3)

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
