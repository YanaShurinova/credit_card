"""Модуль для хранения вспомогательных функций."""
import aiohttp
import cv2
import numpy as np
from deepface import DeepFace

from verification.src.app.config import main_url


def read_image(file_path: str):
    """Метод чтения файла.

    Parameters:
        file_path (str): путь к файлу

    Returns:
        numpy: изображение
    """
    with open(file_path, 'rb') as image:
        img = image.read()
        read_file = bytearray(img)
    read_file = np.frombuffer(read_file, np.uint8)
    read_file = cv2.imdecode(read_file, cv2.IMREAD_COLOR)
    read_file = np.array(read_file)
    return read_file[:, :, ::-1].copy()


async def verify(card_number, file1, file2):
    """Верификация двух фотографий.

    Parameters:
        card_number (str): номер карты
        file1 (numpy): селфи человека
        file2 (numpy): фотография на документе

    Returns:
        str: True/False
    """
    is_verify = DeepFace.verify(file1, file2)
    is_verify = is_verify.get('verified')
    session = aiohttp.ClientSession(raise_for_status=True)
    if is_verify:
        await session.post(
            '{0}/api/change_limit'.format(main_url),
            params={'card_number': card_number, 'new_limit': 100000},
        )
    else:
        await session.post(
            '{0}/api/change_limit'.format(main_url),
            params={'card_number': card_number, 'new_limit': 20000},
        )
    return str(is_verify)
