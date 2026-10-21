"""Модуль с интерфейсом и реализацией кликера"""

from abc import ABC, abstractmethod
from random import randint


class AbstractClicker(ABC):
    """Интерфейс для кликера"""

    @abstractmethod
    def __init__(self) -> None:
        """
        Абстрактный метод инициализации

        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет

        :return: None
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик

        :return: кол-во монет за клик
        """
        raise NotImplementedError


class SimpleRandomClicker(AbstractClicker):
    """Кликер со случайным доходом в заданных границах"""

    def __init__(
        self, min_income: int = 10, max_income: int = 20
    ) -> None:
        """Создать кликер и сохранить границы дохода
        :param min_income: минимальный доход за клик
        :param max_income: максимальный доход за клик
        :return: None
        :raises ValueError: если границы дохода недопустимы
        """
        if min_income < 1 or max_income < min_income:
            raise ValueError(
                "Нужны границы 1 <= min_income <= max_income"
            )
        self._min_income = min_income
        self._max_income = max_income
        self._income_per_click = 0

    def click(self) -> None:
        """Выбрать и сохранить доход за клик

        :return: None; результат доступен через income_per_click
        """
        self._income_per_click = randint(self._min_income, self._max_income)

    @property
    def income_per_click(self) -> int:
        """Вернуть доход последнего клика

        :return: число монет за последний клик
        """
        return self._income_per_click
