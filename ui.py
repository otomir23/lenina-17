import pygame

from inventory import Inventory
from room import RoomObject, Room
from utils import load_image, load_font


class TextOverlay(RoomObject):
    """Оверлей для отображения текста (Например: названий предметов, диалогов)"""

    def __init__(self):
        """Создание оверлея с текстом"""

        self.font = load_font("arkhip.ttf", 12)
        self.surface = pygame.Surface((1280, 24))
        self.surface.fill((0, 0, 0))
        self.surface.set_alpha(0)
        self.alpha = 0
        self.alpha_speed = 0
        self.alpha_target = 0

        super().__init__(self.surface, (640, 12))

        self.passthrough = True

    def update(self, delta_time: float):
        """Обновление оверлея текста

        :param delta_time: время, прошедшее с последнего обновления"""

        # Обновляем прозрачность
        self.alpha += self.alpha_speed * delta_time
        self.surface.set_alpha(self.alpha)

        # Если прозрачность достигла цели
        if (self.alpha_speed > 0 and self.alpha > self.alpha_target) or \
                (self.alpha_speed < 0 and self.alpha < self.alpha_target):
            # Если цель - полная непрозрачность
            if self.alpha_target > 0:
                # Запускаем обратную анимацию
                self.alpha_speed = -self.alpha_speed
                self.alpha_target = 0
            else:
                # Иначе останавливаем анимацию
                self.alpha_speed = 0
                self.passthrough = True

    def display(self, text: str):
        """Запуск анимации перехода"""

        self.alpha_speed = 255 * 6
        self.alpha_target = 255 * 3
        self.surface.fill((0, 0, 0))
        self.surface.blit(self.font.render(text, True, (255, 255, 255)), (4, 4))


class InventoryUI(RoomObject):
    """Интерфейс инвентаря"""

    def __init__(self, inventory: Inventory, text_overlay: TextOverlay):
        """Создание интерфейса инвентаря

        :param inventory: инвентарь"""

        self.width = 96
        self.height = 720
        self.x = 1280 - self.width / 2
        self.y = self.height / 2
        self.surface = pygame.Surface((self.width, self.height))
        self.inventory = inventory
        self.cell_size = self.height / self.inventory.size - 16
        self.text_overlay = text_overlay

        super().__init__(self.surface, (self.x, self.y))

    def update(self, delta_time: float):
        """Обновление интерфейса инвентаря

        :param delta_time: время, прошедшее с последнего обновления"""

        # Очищаем поверхность
        self.surface.fill((0, 0, 0))

        # Перебираем все предметы в инвентаре
        for i, item in enumerate(self.inventory.items):
            # Рисуем предмет
            img = pygame.transform.scale(item.image, (int(self.cell_size) - 4, int(self.cell_size) - 4))
            pos = (10, 10 + i * (self.cell_size + 16))
            if self.inventory.selected == i:
                self.surface.fill((96, 96, 96), (pos[0] - 2, pos[1] - 2, self.cell_size, self.cell_size))
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
                s = self.inventory.get_selected()
                if s is not None:
                    self.text_overlay.display(s.name)


class TransitionOverlay(RoomObject):
    """Оверлей перехода между комнатами"""

    def __init__(self, room: Room):
        """Создание оверлея перехода

        :param room: комната в которой будет отрисован оверлей"""

        self.room = room
        self.surface = pygame.Surface((1280, 720))
        self.surface.fill((0, 0, 0))
        self.surface.set_alpha(0)
        self.alpha = 0
        self.alpha_speed = 0
        self.alpha_target = 0
        self.rotation_target = 0

        super().__init__(self.surface, (640, 360))

        self.passthrough = True

    def update(self, delta_time: float):
        """Обновление оверлея перехода

        :param delta_time: время, прошедшее с последнего обновления"""

        # Обновляем прозрачность
        self.alpha += self.alpha_speed * delta_time
        self.surface.set_alpha(self.alpha)

        # Если прозрачность достигла цели
        if (self.alpha_speed > 0 and self.alpha > self.alpha_target) or \
                (self.alpha_speed < 0 and self.alpha < self.alpha_target):
            # Если цель - полная непрозрачность
            if self.alpha_target > 0:
                # Запускаем обратную анимацию
                self.alpha_speed = -self.alpha_speed
                self.alpha_target = 0
                # Поворачиваем игрока
                self.room.rotate(self.rotation_target)
            else:
                # Иначе останавливаем анимацию
                self.alpha_speed = 0
                self.passthrough = True

    def start(self, target: int):
        """Запуск анимации перехода"""

        self.alpha_speed = 255 * 6
        self.alpha_target = 255
        self.rotation_target = target
        self.passthrough = False


def apply_ui(room: Room):
    """Применение интерфейса

    :param room: комната в которой будет отрисован интерфейс"""

    # Загрузка иконки стрелочки, которая используется для переключения стен
    arrow_image = load_image("left_arrow.png")
    arrow_image = pygame.transform.scale(arrow_image, (32, 32))

    # Создания оверлея с текстом
    text_overlay = TextOverlay()
    room.text_overlay = text_overlay

    # Создание инвентаря
    inv_ui = InventoryUI(room.inventory, text_overlay)

    # Создание оверлея перехода
    transition_overlay = TransitionOverlay(room)

    # Создание стрелочки поворота против часовой стрелки
    left_arrow = RoomObject(arrow_image, (48, 360))
    left_arrow.click_hook = lambda *_: transition_overlay.start(-1)

    # Создание стрелочки поворота по часовой стрелке
    right_arrow = RoomObject(pygame.transform.flip(arrow_image, True, False), (1280 - inv_ui.width - 48, 360))
    right_arrow.click_hook = lambda *_: transition_overlay.start(1)

    # Добавление объектов в оверлей
    room.add_objects(transition_overlay, text_overlay, left_arrow, right_arrow, inv_ui)
