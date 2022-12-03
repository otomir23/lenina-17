import os
import sys
import pygame


def get_resource_path(asset_type, asset_name):
    """Получает путь к ресурсу"""

    # Если программа запущена из exe-файла
    try:
        # То путь к ресурсам - в временной папке из переменной окружения
        base_path = sys._MEIPASS
    except Exception:
        # Если не удалось загрузить - ресурсы лежат в рабочей директории
        base_path = os.path.abspath(".")

    # Возвращаем путь к ресурсу
    return os.path.join(base_path, 'assets', f'{asset_type}s', asset_name)


def load_image(asset_name):
    """Загружает изображение"""

    # Получаем путь к ресурсу
    asset_path = get_resource_path('image', asset_name)

    # Загружаем изображение
    image = pygame.image.load(asset_path)

    # Возвращаем загруженное изображение
    return image
