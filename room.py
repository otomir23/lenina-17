from __future__ import annotations
import pygame
from pygame.sprite import Sprite, Group
from utils import load_image


# Этот файл отвечает за фреймворк комнат, который включает в себя:
# - Создание комнат
# - Создание объектов
# - Добавление объектов на определенную стену комнаты или в оверлей
# - Создание хуков для обработки событий объектов


class Room:
    """Комната, которая содержит четыре стены, представленные группами спрайтов."""

    def __init__(self):
        """Создание комнаты"""

        # Создание групп спрайтов для каждой стены
        self.walls = (
            Group(),
            Group(),
            Group(),
            Group()
        )
        self.overlays = Group()

        # Загрузка иконки стрелочки, которая используется для переключения стен
        arrow_image = load_image("left_arrow.png")
        arrow_image = pygame.transform.scale(arrow_image, (32, 32))

        # Создание стрелочки поворота против часовой стрелки
        left_arrow = InteractableRoomObject(arrow_image, (30, 360))
        left_arrow.click_hook = lambda *_: self.rotate(-1)
        self.add_objects(left_arrow)

        # Создание стрелочки поворота по часовой стрелке
        right_arrow = InteractableRoomObject(pygame.transform.flip(arrow_image, True, False), (1250, 360))
        right_arrow.click_hook = lambda *_: self.rotate(1)
        self.add_objects(right_arrow)

        # Текущая стена, к которой повёрнут игрок
        self.current_wall = 0

    def update(self, delta_time: float):
        """Обновление объектов на текущей стене

        :param delta_time: время, прошедшее с последнего обновления"""

        self.walls[self.current_wall].update(delta_time)
        self.overlays.update(delta_time)

    def draw(self, screen: pygame.Surface):
        """Отрисовка комнаты

        :param screen: экран, на котором отрисовывается комната"""

        self.walls[self.current_wall].draw(screen)
        self.overlays.draw(screen)

    def rotate(self, amount: int):
        """Поворот пользователя на amount стен

        :param amount: количество стен, на которое поворачивается игрок, может быть отрицательным"""

        # Поворачиваем игрока на amount стен
        self.current_wall += amount

        # Если игрок повернулся на стену, которой нет, то возвращаем его на первую стену
        self.current_wall %= 4

    def click(self, pos: tuple[int, int]):
        """Обработка клика по объектам, с которыми можно взаимодействовать

        :param pos: позиция клика"""

        # Проходим по всем объектам на текущей стене и оверлеях
        for obj in [*self.walls[self.current_wall], *self.overlays]:
            # Если объект - объект, с которым можно взаимодействовать и клик был по нему
            if isinstance(obj, InteractableRoomObject) and obj.rect.collidepoint(pos):
                # Вызываем обработчик клика
                obj.click(pos)
                break

    def add_objects(self, *objs: RoomObject, wall: int = None):
        """Добавление объекта в комнату

        :param wall: стена, на которую добавляется объект
        :param objs: объекты, который добавляется в комнату"""

        # Если стена не указана, то добавляем объекты в оверлеи
        if wall is None:
            self.overlays.add(*objs)
        # Иначе добавляем объекты на указанную стену
        else:
            self.walls[wall % 4].add(*objs)


class RoomObject(Sprite):
    """Объект, который находится в комнате"""

    def __init__(self, image: pygame.Surface, pos: tuple[float, float]):
        """Создание объекта

        :param image: изображение объекта
        :param pos: позиция объекта"""

        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.update_hook = None

    def draw(self, surface: pygame.Surface):
        """Отрисовка объекта

        :param surface: поверхность, на которой отрисовывается объект"""

        surface.blit(self.image, self.rect)

    def update(self, delta_time: float):
        """Обновление объекта

        :param delta_time: время, прошедшее с последнего обновления"""

        if self.update_hook is not None:
            self.update_hook(self, delta_time)


class InteractableRoomObject(RoomObject):
    """Объект, с которым можно взаимодействовать"""

    def __init__(self, image: pygame.Surface, pos: tuple[int, int]):
        """Создание объекта

        :param image: изображение объекта
        :param pos: позиция объекта"""

        super().__init__(image, pos)
        self.click_hook = None
        self.storage = {}

    def click(self, pos: tuple[int, int]):
        """Функция, которая инициирует обработчик клика по объекту"""

        if self.click_hook is not None:
            self.click_hook(self, pos)
