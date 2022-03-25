from telebot.types import InlineKeyboardMarkup
import json


class Grid:
    """
    Класс, для работы сетки в игре крестики-нолики
    """

    def __init__(self, json_str: str = None):
        """Инициализация сетки"""

        if json_str is None:
            # Случай, для создания первой сетки
            self.__grid = [
                {"id": i, "value": "" "", "empty": False} for i in range(1, 10)
            ]

        else:
            # Случай, для создания сетки, на основе другой сетки
            self.__grid = json.loads(json_str)

    def __str__(self):
        """Возвращает json сетки"""
        return json.dumps(self.__grid)


