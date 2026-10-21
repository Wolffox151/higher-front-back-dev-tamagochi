"""Модуль с моделями"""

from dataclasses import dataclass


def _validate_product(name: str, price: int) -> None:
    """Проверить общие данные еды и лекарства

    :param name: название товара
    :param price: цена товара в монетах
    :return: None, если данные допустимы
    :raises ValueError: если название пустое или цена отрицательная
    """
    if not name.strip():
        raise ValueError("Название не должно быть пустым")
    if price < 0:
        raise ValueError("Цена не может быть отрицательной")


@dataclass(frozen=True, slots=True)
class Food:
    """Модель объекта еды"""

    name: str  # наименование
    satiety: int  # на сколько единиц утоляет голод
    price: int  # стоимость

    def __post_init__(self) -> None:
        """Проверить данные созданного объекта еды

        :return: None, если данные допустимы
        :raises ValueError: если данные еды недопустимы
        """
        _validate_product(self.name, self.price)
        if self.satiety <= 0:
            raise ValueError("Насыщение еды должно быть положительным")

    def __repr__(self) -> str:
        """Метод для красивого принтинга объекта

        :return: строка с ключами и значениями свойств объекта
        """
        return (
            f"{self.name} стоимость: {self.price}, "
            f"утоляет голод на {self.satiety} единиц"
        )


@dataclass
class Medicine:
    """Модель объекта лекарства"""

    name: str  # наименование
    price: int  # стоимость
    heal_hp: int  # сколько лечит HP
    number_of_uses: int  # максимальное количество применений
    uses: int = 0  # текущее количество применений

    def __post_init__(self) -> None:
        """Проверить данные созданного лекарства

        :return: None, если данные допустимы
        :raises ValueError: если данные лекарства недопустимы
        """
        _validate_product(self.name, self.price)
        if self.heal_hp <= 0:
            raise ValueError("Лечебный эффект должен быть положительным")
        if self.number_of_uses <= 0:
            raise ValueError("Лимит применений должен быть положительным")
        if not 0 <= self.uses <= self.number_of_uses:
            raise ValueError("Число применений должно быть от 0 до лимита")

    def is_empty(self) -> bool:
        """
        Проверяет, осталось ли еще лекарство

        :return: True если лекарство закончилось, иначе False
        """
        return self.uses >= self.number_of_uses

    def __repr__(self) -> str:
        """Метод для красивого принтинга объекта

        :return: строка с ключами и значениями свойств объекта
        """
        return (
            f'{self.name} стоимость: {self.price}, '
            f'лечит на {self.heal_hp} HP, использований: '
            f'{self.number_of_uses - self.uses}/{self.number_of_uses}'
        )
