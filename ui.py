import pygame

from inventory import Inventory
from room import RoomObject, Room
from utils import load_image


class InventoryUI(RoomObject):
    """Интерфейс инвентаря"""

    def __init__(self, inventory: Inventory):
        """Создание интерфейса инвентаря

        :param inventory: инвентарь"""

        self.width = 96
        self.height = 720
        self.x = 1280 - self.width / 2
        self.y = self.height / 2
        self.surface = pygame.Surface((self.width, self.height))
        self.inventory = inventory
        self.cell_size = self.height / self.inventory.size - 16

        super().__init__(self.surface, (self.x, self.y))

    def update(self, delta_time: float):
        """Обновление интерфейса инвентаря

        :param delta_time: время, прошедшее с последнего обновления"""

        # Очищаем поверхность
        self.surface.fill((0, 0, 0))

        # Перебираем все предметы в инвентаре
        for i, item in enumerate(self.inventory.items):
            # Рисуем предмет
            img = pygame.transform.scale(item.image, (int(self.cell_size), int(self.cell_size)))
            pos = (8, 8 + i * (self.cell_size + 16))
            if self.inventory.selected == i:
                self.surface.fill((96, 96, 96), (*pos, self.cell_size, self.cell_size))
            self.surface.blit(img, pos)

    def click(self, pos: tuple[int, int]):
        """Обработка клика по интерфейсу инвентаря

        :param pos: координаты клика"""

        pos = (pos[0] - self.x + self.width / 2, pos[1] - self.y + self.height / 2)

        # Перебираем все предметы в инвентаре
        for i, item in enumerate(self.inventory.items):
            # Если клик был по ячейке
            if 8 < pos[0] < 8 + self.cell_size and \
                    8 + i * (self.cell_size + 16) < pos[1] < 8 + (i + 1) * (self.cell_size + 16):
                # Выбираем предмет
                self.inventory.select(i)


def apply_ui(room: Room):
    """Применение интерфейса инвентаря

    :param room: комната в которой будет отрисован интерфейс"""

    # Загрузка иконки стрелочки, которая используется для переключения стен
    arrow_image = load_image("left_arrow.png")
    arrow_image = pygame.transform.scale(arrow_image, (32, 32))

    # Создание инвентаря
    inv_ui = InventoryUI(room.inventory)

    # Создание стрелочки поворота против часовой стрелки
    left_arrow = RoomObject(arrow_image, (48, 360))
    left_arrow.click_hook = lambda *_: room.rotate(-1)

    # Создание стрелочки поворота по часовой стрелке
    right_arrow = RoomObject(pygame.transform.flip(arrow_image, True, False), (1280 - inv_ui.width - 48, 360))
    right_arrow.click_hook = lambda *_: room.rotate(1)

    # Добавление объектов в оверлей
    room.add_objects(left_arrow, right_arrow, inv_ui)
