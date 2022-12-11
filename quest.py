import pygame

from inventory import Item
from room import Room, RoomObject
from ui import apply_ui
from utils import load_image


class QuestRoom(Room):
    """Основная комната"""

    def __init__(self):
        """Создание комнаты"""

        super().__init__()

        # Применение интерфейса к комнате
        apply_ui(self)

        # Добавление тестовых объектов
        self.apply_objects()

    def apply_objects(self):
        """Добавление объектов"""

        s = pygame.transform.scale(load_image('lemon.png'), (200, 200))

        # Демонстрация работы хука click (клик по объекту)
        a = RoomObject(s, (100, 100))
        a.click_hook = self.basic_click_hook
        self.add_objects(a, wall=0)

        # Демонстрация работы хука update (обновление объекта)
        b = RoomObject(s, (200, 100))
        b.update_hook = self.basic_update_hook
        self.add_objects(b, wall=1)

        # Демонстрация работы хранилища данных
        c = RoomObject(s, (300, 100))
        c.click_hook = self.basic_storage_example
        self.add_objects(c, wall=2)

        # Демонстрация работы с инвентарем
        d = RoomObject(s, (400, 100))
        d.click_hook = self.basic_inventory_example
        self.add_objects(d, wall=3)

    def basic_click_hook(self, obj, pos):
        """Пример хука клика по объекту"""

        print("тулуз нажат !", pos)

    def basic_update_hook(self, obj, dt):
        """Пример хука обновления объекта"""

        print("тулуз на экране !", int(1 / dt), "FPS")

    def basic_storage_example(self, obj, pos):
        """Пример работы с хранилищем данных"""

        if 'test' not in obj.storage:
            obj.storage['test'] = 0

        obj.storage['test'] += 1
        print("тулуз был нажат ", obj.storage['test'], "раз !")

    def basic_inventory_example(self, obj, pos):
        """Пример работы с инвентарем"""

        inv = obj.room.inventory
        if inv.selected is not None and inv.get_selected().uid == 'cup':
            inv.remove_selected()
            return

        inv.add(Item('cup', 'Чашка', load_image('cup.png')))