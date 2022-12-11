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

        # Загружаем картинку чая и меняем ей размер
        tea_image = load_image("tea.png")
        tea_image = pygame.transform.scale(tea_image, (100, 67))

        # Создаем объект чая и привязываем к нему функцию по клику
        tea_object = RoomObject(tea_image, (400, 320))
        tea_object.click_hook = self.click_tea

        # Добавляем объект в комнату на стену 0 (переднюю)
        self.add_objects(tea_object, wall=0)

        # Загружаем картинку чашки и меняем ей размер
        cup_image = load_image("cup.png")
        cup_image = pygame.transform.scale(cup_image, (100, 72))

        # Создаем объект чашки и привязываем к нему функцию по клику
        cup_object = RoomObject(cup_image, (400, 320))
        cup_object.click_hook = self.click_cup

        # Добавляем объект в комнату на стену 3 по часовой стрелке (левую)
        self.add_objects(cup_object, wall=3)

    def click_tea(self, obj, *_):
        """Обработчик клика по чаю"""

        # Проверяем брали ли мы уже чай
        if 'used' in obj.storage:
            # Если да, то ничего не делаем
            return

        # Добавляем чай в инвентарь
        self.inventory.add(Item("tea", "Чай", load_image("tea.png")))

        # Удаляем картинку чая
        obj.image = pygame.Surface((0, 0))

        # Добавляем в хранилище объекта информацию о том, что чай уже брали
        obj.storage['used'] = True

    def click_cup(self, obj, *_):
        """Обработчик клика по чашке"""

        # Проверяем выделен ли какой-то предмет в инвентаре и является ли он чаем
        if self.inventory.get_selected() is not None and self.inventory.get_selected().uid == "tea":
            # Если да, то удаляем чай из инвентаря
            self.inventory.remove_selected()
            print("Чай налит в чашку")
            # И сохраняем информацию о том, что чай налит в чашку
            obj.storage['has_tea'] = True
