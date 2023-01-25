import sys

import pygame

from room import RoomObject, Room
from utils import load_image, load_font


class TextOverlay(RoomObject):
    """Оверлей для отображения текста (Например: названий предметов, диалогов)"""

    def __init__(self):
        """Создание оверлея с текстом"""

        self.font = load_font("arkhip.ttf", 24)
        self.surface = pygame.Surface((1086, 48))
        self.surface.fill((0, 0, 0))
        self.surface.set_alpha(0)
        self.alpha = 0
        self.alpha_speed = 0
        self.alpha_target = 0

        super().__init__(self.surface, (543, 24))

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
        self.alpha_target = 255 * 6
        self.surface.fill((0, 0, 0))
        self.surface.blit(self.font.render(text, True, (255, 255, 255)), (8, 8))


class InventoryUI(RoomObject):
    """Интерфейс инвентаря"""

    def __init__(self, room: Room):
        """Создание интерфейса инвентаря

        :param room: комната, в которой находится игрок"""

        self.width = 96
        self.height = 720
        self.x = 1086 - self.width / 2
        self.y = self.height / 2
        self.surface = pygame.Surface((self.width, self.height))
        self.inventory = room.inventory
        self.room = room
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
            img = pygame.transform.scale(item.image, (int(self.cell_size) - 4, int(self.cell_size) - 4))
            pos = (10, 10 + i * (self.cell_size + 16))
            if self.inventory.selected == i:
                self.surface.fill((96, 96, 96), (pos[0] - 2, pos[1] - 2, self.cell_size, self.cell_size))
            self.surface.blit(img, pos)

    def click(self, pos: tuple[int, int]):
        """Обработка клика по интерфейсу инвентаря

        :param pos: координаты клика"""

        # Перебираем все предметы в инвентаре
        for i, item in enumerate(self.inventory.items):
            # Если клик был по ячейке
            if 8 < pos[0] < 8 + self.cell_size and \
                    8 + i * (self.cell_size + 16) < pos[1] < 8 + (i + 1) * (self.cell_size + 16):
                # Выбираем предмет
                self.inventory.select(i)
                s = self.inventory.get_selected()
                if s is not None:
                    self.room.send_message("text", s.name)


class TransitionOverlay(RoomObject):
    """Оверлей перехода между комнатами"""

    def __init__(self, room: Room):
        """Создание оверлея перехода

        :param room: комната в которой будет отрисован оверлей"""

        self.room = room
        self.surface = pygame.Surface((1086, 720))
        self.surface.fill((0, 0, 0))
        self.surface.set_alpha(0)
        self.alpha = 0
        self.alpha_speed = 0
        self.alpha_target = 0
        self.rotation_target = 0

        super().__init__(self.surface, (543, 360))

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


class PauseMenu(RoomObject):
    """Меню паузы"""

    def __init__(self):
        """Создание меню паузы"""

        self.surface = pygame.Surface((1086, 720), pygame.SRCALPHA, 32)
        self.surface.fill((0, 0, 0, 172))
        self.surface.set_alpha(0)

        # Заголовок
        self.surface.blit(load_font("arkhip.ttf", 64).render("Пауза", True, (255, 255, 255)), (140, 180))

        # Кнопки
        f = load_font("arkhip.ttf", 24)
        self.buttons = []

        for i, b in enumerate([
            "Продолжить",
            "Громкость музыки",
            "Громкость звуков",
            "Выйти"
        ]):
            pos = (140, 270 + i * 30)
            img = f.render(b, True, (255, 255, 255))
            self.surface.blit(img, pos)
            self.buttons.append((b, pos, img))

        # Остальные параметры
        super().__init__(self.surface, (543, 360))

        self.visible = False
        self.passthrough = True

    def toggle(self):
        """Переключение видимости меню паузы"""

        self.visible = not self.visible
        self.passthrough = not self.visible
        self.surface.set_alpha(255 if self.visible else 0)
        self.room.paused = self.visible

    def click(self, pos: tuple[int, int]):
        """Обработка клика по меню паузы

        :param pos: позиция клика"""

        if not self.visible:
            return

        for b, p, i in self.buttons:
            if i.get_rect(topleft=p).collidepoint(pos):
                if b == "Продолжить":
                    self.toggle()
                elif b == "Громкость музыки":
                    pygame.mixer.music.set_volume((pygame.mixer.music.get_volume() + 0.1) % 1)
                elif b == "Громкость звуков":
                    self.room.channel.set_volume((self.room.channel.get_volume() + 0.1) % 1)
                elif b == "Выйти":
                    pygame.quit()
                    sys.exit()


class CompletionUI(RoomObject):
    def __init__(self):
        """Создание интерфейса завершения комнаты"""

        # Загрузка изображений
        self.surface = pygame.Surface((1086, 720), pygame.SRCALPHA, 32)
        self.surface.fill((0, 0, 0, 172))
        self.surface.set_alpha(0)

        # Остальные параметры
        super().__init__(self.surface, (543, 360))

        self.visible = False
        self.passthrough = True
        self.time = 0

    def update(self, delta_time: float):
        """Обновление интерфейса

        :param delta_time: время, прошедшее с последнего обновления"""

        self.time += delta_time

    def complete(self):
        """Завершение уровня"""

        self.visible = True
        self.passthrough = False
        self.surface.set_alpha(255)

        self.surface.blit(load_font("arkhip.ttf", 64).render("Комната пройдена", True, (255, 255, 255)), (140, 180))
        self.surface.blit(load_font("arkhip.ttf", 24).render("Время: " + str(round(self.time, 2)) + " секунд", True, (255, 255, 255)), (140, 270))
        self.surface.blit(load_font("arkhip.ttf", 24).render("Нажмите пробел, чтобы продолжить", True, (255, 255, 255)), (140, 300))

        self.room.paused = True


def apply_ui(room: Room):
    """Применение интерфейса

    :param room: комната в которой будет отрисован интерфейс"""

    # Загрузка иконки стрелочки, которая используется для переключения стен
    arrow_image = load_image("left_arrow.png")
    arrow_image = pygame.transform.scale(arrow_image, (32, 32))

    # Создания оверлея с текстом
    text_overlay = TextOverlay()
    room.register_message_handler(lambda channel, text, *_:
                                  text_overlay.display(str(text)) if (channel == "text") else None)

    # Создание инвентаря
    inv_ui = InventoryUI(room)

    # Создание меню паузы
    pause_menu = PauseMenu()

    def pause(channel, key, *_):
        if channel == "key_down" and key == pygame.K_ESCAPE:
            pause_menu.toggle()

    room.register_message_handler(pause)

    # Создание оверлея перехода
    transition_overlay = TransitionOverlay(room)

    def rotate(channel, key, *_):
        if channel == "key_down" and transition_overlay.passthrough:
            if key == pygame.K_LEFT:
                transition_overlay.start(-1)
            elif key == pygame.K_RIGHT:
                transition_overlay.start(1)

    room.register_message_handler(rotate)

    # Создание оверлея завершения уровня
    completion_ui = CompletionUI()
    room.register_message_handler(lambda channel, *_: completion_ui.complete() if (channel == "complete") else None)
    room.register_message_handler(lambda channel, key: exit(0) if (
            channel == "key_down" and key == pygame.K_SPACE and completion_ui.visible
    ) else None)

    # Создание стрелочки поворота против часовой стрелки
    left_arrow = RoomObject(arrow_image, (48, 360))
    left_arrow.click_hook = lambda *_: transition_overlay.start(-1)

    # Создание стрелочки поворота по часовой стрелке
    right_arrow = RoomObject(pygame.transform.flip(arrow_image, True, False), (1086 - inv_ui.width - 48, 360))
    right_arrow.click_hook = lambda *_: transition_overlay.start(1)

    # Добавление объектов в оверлей
    room.add_objects(transition_overlay, text_overlay, left_arrow, right_arrow, inv_ui, pause_menu, completion_ui)
