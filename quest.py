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

        # Загружаем картинки
        paper_image = load_image("paper.png")
        paper_image = pygame.transform.scale(paper_image, (24, 24))

        tea_image = load_image("tea.png")
        tea_image = pygame.transform.scale(tea_image, (100, 67))

        cup_image = load_image("cup.png")
        cup_image = pygame.transform.scale(cup_image, (100, 72))

        book1_image = load_image("alyonka.png")
        book1_image = pygame.transform.scale(book1_image, (25, 67))

        book2_image = load_image("alyonka.png")
        book2_image = pygame.transform.scale(book2_image, (50, 70))

        book3_image = load_image("alyonka.png")
        book3_image = pygame.transform.scale(book3_image, (33, 65))

        matryoshka_top_image = load_image("matryoshka_top.png")
        matryoshka_top_image = pygame.transform.scale(matryoshka_top_image, (32, 32))

        matryoshka_bottom_image = load_image("matryoshka_bottom.png")
        matryoshka_bottom_image = pygame.transform.scale(matryoshka_bottom_image, (32, 32))

        # Создаем объект чая и привязываем к нему функцию по клику
        tea_object = RoomObject(tea_image, (400, 320))
        tea_object.click_hook = self.click_tea

        # Создаем кусочек картинки 3
        paper_piece3 = RoomObject(pygame.transform.rotate(paper_image, 90), (720, 220))
        paper_piece3.update_hook = self.update_piece
        paper_piece3.click_hook = self.get_piece_click_handler(3)

        # Добавляем объекты в комнату на стену 0 (переднюю)
        self.add_objects(tea_object, paper_piece3, wall=0)

        # Создаем кусочек картинки 4
        paper_piece4 = RoomObject(pygame.transform.rotate(paper_image, 90), (100, 400))
        paper_piece4.update_hook = self.update_piece
        paper_piece4.click_hook = self.get_piece_click_handler(4)

        # Добавляем объекты в комнату на стену 1 (правую)
        self.add_objects(paper_piece4, wall=1)

        # Создаем лампу
        lamp = RoomObject(load_image("lamp_off.png"), (400, 300))
        lamp.click_hook = self.click_lamp

        # Добавляем объекты на стену 2 по часовой стрелке (заднюю)
        self.add_objects(lamp, wall=2)

        # Создаем объект чашки и привязываем к нему функцию по клику
        cup_object = RoomObject(cup_image, (400, 370))
        cup_object.click_hook = self.click_cup

        # Создаем объекты книг
        book1_object = DraggableObject(book1_image, (250, 280))
        book2_object = DraggableObject(book2_image, (300, 280))
        book3_object = DraggableObject(book3_image, (360, 280))

        # Создаем объекты матрешки
        matryoshka_top = RoomObject(matryoshka_top_image, (400, 185))
        matryoshka_bottom = RoomObject(matryoshka_bottom_image, (400, 185 + matryoshka_top_image.get_height()))
        paper_piece2 = RoomObject(paper_image, (400, 200))

        matryoshka_top.click_hook = self.click_matryoshka_top
        matryoshka_top.update_hook = self.update_matryoshka_top
        paper_piece2.update_hook = self.update_piece
        paper_piece2.click_hook = self.get_piece_click_handler(2)

        # Добавляем объекты в комнату на стену 3 по часовой стрелке (левую)
        self.add_objects(cup_object, book1_object, book2_object, book3_object, paper_piece2, matryoshka_top, matryoshka_bottom, wall=3)

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

    def click_lamp(self, obj, pos):
        """Обработчик клика по лампе"""

        # Сохраняем в переменную информацию о том, была ли лампа включена
        lamp_on = 'on' in obj.storage and obj.storage['on']

        # Если мы нажали на верёвку лампы, то включаем/выключаем лампу
        if 415 < pos[0] < 425 and 315 < pos[1] < 335:
            if lamp_on:
                obj.image = load_image("lamp_off.png")
                obj.storage['on'] = False
            else:
                obj.image = load_image("lamp_on_empty.png" if 'piece_taken' in obj.storage else "lamp_on.png")
                obj.storage['on'] = True

        # Если лампа включена и был нажат кусок картинки, то берём его
        if lamp_on and 'piece_taken' not in obj.storage and 400 < pos[0] < 430 and 300 < pos[1] < 315:
            self.inventory.add(Item("piece_1", "Кусочек картинки", load_image("paper.png")))
            obj.storage['piece_taken'] = True
            obj.image = load_image("lamp_on_empty.png")

    def click_matryoshka_top(self, obj, *_):
        """Обработчик клика по верхней части матрёшки"""

        # Если верхняя часть матрёшки открыта, то ничего не делаем
        if 'opened' in obj.storage:
            return

        # Добавляем в хранилище объекта информацию о том, что матрёшка начала открытие
        obj.storage['opened'] = False

    def update_matryoshka_top(self, obj, dt):
        """Обновление верхней части матрёшки"""

        if 'opened' in obj.storage:
            y_target = 100

            # Если анимация не началась, начинаем её
            if not obj.storage['opened']:
                obj.rect.y -= 10
            else:
                obj.image = pygame.Surface((0, 0))

            # Если верхняя часть матрёшки достигла цели, то сохраняем информацию о том, что она открыта
            if obj.rect.y <= y_target:
                obj.storage['opened'] = True

    def get_piece_click_handler(self, piece: int):
        """Возвращает обработчик клика по куску картинки"""

        def click_piece(obj, *_):
            # Если кусок картинки взят, то ничего не делаем
            if 'taken' in obj.storage:
                return

            # Добавляем в хранилище объекта информацию о том, что кусок картинки взят
            obj.storage['taken'] = True

            # Добавляем кусок картинки в инвентарь
            self.inventory.add(Item(f"piece_{piece}", "Кусочек картинки", load_image("paper.png")))

        return click_piece

    def update_piece(self, obj, dt):
        """Обновление куска картинки"""

        # Если кусок картинки брали, то удаляем его
        if 'taken' in obj.storage:
            obj.image = pygame.Surface((0, 0))


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
