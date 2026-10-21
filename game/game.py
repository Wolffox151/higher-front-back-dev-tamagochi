"""Модуль с интерфейсом и реализацией класса игры"""

from abc import ABC, abstractmethod
from typing import Any
from dataclasses import replace

from .tamagochi import AbstractTamagochi
from .clicker import AbstractClicker
from .models import Food, Medicine
from .exceptions import NotEnoughMoney


class AbstractGame(ABC):
    """Интерфейс для логики игры"""

    tamagochi: AbstractTamagochi

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ) -> None:
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия работа

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """
        Абстрактный метод для покупки еды

        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства

        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи

        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи

        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self) -> None:
        """Абстрактный метод для отдыха тамагочи

        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self) -> None:
        """Абстрактный метод для игры с тамагочи

        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
        raise NotImplementedError


class SimpleGame(AbstractGame):
    """
    Игра, объединяющая питомца, кликер,
    магазин и запасы
    """

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """Создать игру с пустыми сумками и нулевым балансом

        :param tamagochi: питомец с интерфейсом AbstractTamagochi
        :param clicker: кликер с интерфейсом AbstractClicker
        :param all_food: каталог еды, доступной для покупки
        :param all_medicine: каталог лекарств, доступных для покупки
        :return: None
        """
        self.tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = list(all_food)
        self._all_medicine = list(all_medicine)
        self._food: list[Food] = []
        self._medicine: list[Medicine] = []
        self._coins = 0

    @property
    def food(self) -> list[Food]:
        """Вернуть список купленной еды.

        :return: копия списка еды в инвентаре
        """
        return self._food

    @property
    def medicine(self) -> list[Medicine]:
        """Вернуть список купленных лекарств

        :return: копия списка лекарств в инвентаре
        """
        return self._medicine

    def get_status(self) -> dict[str, int]:
        """Получить показатели питомца и баланс игры

        :return: новый словарь с показателями питомца и монетами
        """
        status = dict(self.tamagochi.status)
        status["coins"] = self._coins
        return status

    def work(self) -> int:
        """Заработать монеты за клик

        :return: доход за текущий вызов,
        добавленный к балансу
        :raises TamagochiIsGone: если питомец погиб
        """
        self.tamagochi.ensure_alive()
        self._clicker.click()
        income = self._clicker.income_per_click
        self._coins += income
        return income

    def play_with_tamagochi(self) -> None:
        """Передать питомцу действие игры

        :return: None
        :raises TamagochiIsGone: если питомец погиб
        """
        self.tamagochi.play()

    def rest_tamagochi(self) -> None:
        """Передать питомцу действие отдыха

        :return: None
        :raises TamagochiIsGone: если питомец погиб
        """
        self.tamagochi.rest()

    def _select_index(self, items: list[Food] | list[Medicine]) -> int:
        """Показать предметы и получить индекс выбранного

        :param items: список еды или лекарств для выбора
        :return: индекс выбранного предмета, начиная с нуля
        :raises ValueError: если список пуст, выбор отменён
        или не верен
        """
        if not items:
            raise ValueError("Список пуст")
        for number, item in enumerate(items, start=1):
            print(f"{number}. {item}")
        print("0. Отмена")

        try:
            number = int(input("Выберите номер: "))
        except ValueError as error:
            raise ValueError("Введите целый номер") from error

        if number == 0:
            raise ValueError("Действие отменено")
        if not 1 <= number <= len(items):
            raise ValueError("Такого номера нет")
        return number - 1

    def _pay(self, price: int) -> None:
        """Списать стоимость покупки с баланса

        :param price: неотрицательная цена товара в монетах
        :return: None после успешной оплаты
        :raises NotEnoughMoney: если не хватает монет
        """
        if self._coins < price:
            raise NotEnoughMoney("Недостаточно монет для покупки")
        self._coins -= price

    def buy_food(self) -> None:
        """Купить выбранную еду и добавить её в инвентарь

        :return: None
        :raises TamagochiIsGone: если питомец погиб
        :raises ValueError: если каталог пуст, выбор отменён или неверен
        :raises NotEnoughMoney: если не хватает монет
        """
        self.tamagochi.ensure_alive()
        index = self._select_index(self._all_food)
        food = self._all_food[index]
        self._pay(food.price)
        self._food.append(food)

    def buy_medicine(self) -> None:
        """Купить выбранное лекарство

        :return: None.
        :raises TamagochiIsGone: если питомец погиб
        :raises ValueError: если данные или выбор лекарства недопустимы
        :raises NotEnoughMoney: если не хватает монет
        """
        self.tamagochi.ensure_alive()
        index = self._select_index(self._all_medicine)
        medicine = replace(self._all_medicine[index], uses=0)
        self._pay(medicine.price)
        self._medicine.append(medicine)

    def feed_tamagochi(self) -> None:
        """Накормить питомца выбранной едой из сумки

        :return: None.
        :raises TamagochiIsGone: если питомец погиб
        :raises ValueError: если сумка пуста, выбор
        отменён или неверен
        """
        self.tamagochi.ensure_alive()
        index = self._select_index(self._food)
        food = self._food[index]
        self.tamagochi.feed(food)
        self._food.pop(index)

    def heal_tamagochi(self) -> None:
        """Вылечить питомца выбранным лекарством из сумки

        :return: None.
        :raises TamagochiIsGone: если питомец погиб
        :raises ValueError: если выбор неверен,
        отменён или лечить нечем
        """
        self.tamagochi.ensure_alive()
        index = self._select_index(self._medicine)
        medicine = self._medicine[index]
        self.tamagochi.heal(medicine)
        if medicine.is_empty():
            self._medicine.pop(index)
