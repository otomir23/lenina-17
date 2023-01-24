import pygame

from utils import load_sound


class Item:
    """Предмет, который можно взять в инвентарь"""

    def __init__(self, uid: str, name: str, image: pygame.Surface):
        """Создание предмета

        :param uid: уникальный идентификатор предмета
        :param name: название предмета
        :param image: изображение предмета"""
        self.image = image
        self.uid = uid
        self.name = name

    def __str__(self):
        return f"<Item: {self.uid} ({self.name})>"

    def __repr__(self):
        return self.__str__()


class Inventory:
    """Инвентарь игрока"""

    def __init__(self, size: int, room):
        """Создание инвентаря

        :param size: максимальное количество предметов в инвентаре
        :param room: комната, в которой находится игрок"""
        self.size = size
        self.items = []
        self.selected = None
        self.room = room

        # Загружаем звуки
        self.__pickup_sound = load_sound("pickup.mp3")
        self.__drop_sound = load_sound("drop.mp3")

    def add(self, item: Item):
        """Добавление предмета в инвентарь

        :param item: предмет"""

        # Проверка на наличие свободного места и отсутствие предмета в инвентаре
        if len(self.items) < self.size and self.get(item.uid) is None:
            # Если есть свободное место, то добавляем предмет
            self.items.append(item)
            self.room.channel.play(self.__pickup_sound)
            self.room.send_message("text", f"Вы подобрали {item.name}")

    def remove(self, item_uid: str):
        """Удаление предмета из инвентаря

        :param item_uid: уникальный идентификатор предмета"""

        # Перебираем все предметы в инвентаре
        for item in self.items:
            # Если уникальный идентификатор предмета совпадает с искомым
            if item.uid == item_uid:
                # Удаляем предмет из инвентаря
                self.items.remove(item)
                # Выходим из цикла
                break

    def remove_selected(self):
        """Удаление выбранного предмета"""

        if self.selected is not None:
            self.items.pop(self.selected)
            self.selected = None
            self.room.channel.play(self.__drop_sound)

    def get(self, item_uid: str) -> Item:
        """
        Получение предмета из инвентаря

        :param item_uid: уникальный идентификатор предмета
        :return: предмет
        """

        for item in self.items:
            if item.uid == item_uid:
                return item

    def all(self) -> list[Item]:
        """Получение всех предметов из инвентаря

        :return: список предметов"""

        # Возвращаем копию списка предметов (чтобы нельзя было изменить список предметов извне)
        return self.items[:]

    def select(self, i):
        """Выбор предмета по индексу

        :param i: индекс предмета"""

        if self.selected == i:
            self.selected = None
        else:
            self.selected = i

    def get_selected(self) -> Item:
        """Получение выбранного предмета

        :return: предмет"""

        if self.selected is not None:
            return self.items[self.selected]
