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
        cup_object = RoomObject(cup_image, (400, 370))
        cup_object.click_hook = self.click_cup

        # Добавляем объект в комнату на стену 3 по часовой стрелке (левую)
        self.add_objects(cup_object, wall=3)

        # Загружаем картинки книг и меняем их размер
        book1_image = load_image("alyonka.png")
        book1_image = pygame.transform.scale(book1_image, (25, 67))

        book2_image = load_image("alyonka.png")
        book2_image = pygame.transform.scale(book1_image, (50, 70))

        book3_image = load_image("alyonka.png")
        book3_image = pygame.transform.scale(book1_image, (33, 65))

        # Создаем объекты книг
        book1_object = DraggableObject(book1_image, (250, 280))
        book2_object = DraggableObject(book2_image, (300, 280))
        book3_object = DraggableObject(book3_image, (360, 280))

        # Добавляем объекты в комнату на стену 3 по часовой стрелке (левую)
        self.add_objects(book1_object, wall=3)
        self.add_objects(book2_object, wall=3)
        self.add_objects(book3_object, wall=3)

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


class DraggableObject(RoomObject):
    """Объект, который можно перетаскивать"""

    def __init__(self, image, pos):
        """Создание объекта"""

        super().__init__(image, pos)

        # Сохраняем начальную позицию
        self.pos = pos
        self.offset = None

    def update(self, delta_time: float):
        # Если мышь нажата и не была нажата раньше, а также мышь над объектом
        if pygame.mouse.get_pressed()[0] and self.offset is None\
                and self.rect.collidepoint(pygame.mouse.get_pos()):
            # Сохраняем смещение относительно объекта
            self.offset = pygame.mouse.get_pos()[0] - self.pos[0], pygame.mouse.get_pos()[1] - self.pos[1]

        # Если мышь отпущена
        if not pygame.mouse.get_pressed()[0]:
            # Сбрасываем смещение
            self.offset = None

        # Если смещение не равно None

        if self.offset is not None:
            # Перемещаем объект на новую позицию
            self.pos = pygame.mouse.get_pos()[0] - self.offset[0], pygame.mouse.get_pos()[1] - self.offset[1]

        # Обновляем позицию объекта
        self.rect = self.image.get_rect(center=self.pos)

        # Вызываем метод родителя
        super().update(delta_time)
