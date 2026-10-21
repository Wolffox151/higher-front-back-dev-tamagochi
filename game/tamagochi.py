"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod

from .models import Food, Medicine
from .exceptions import TamagochiIsGone

MAX_STAT = 100
MIN_STAT = 0
SICKNESS_THRESHOLD = 80

FEED_ENERGY_COST = 5
PLAY_ENERGY_COST = 15
PLAY_FATIGUE_INCREASE = 15
PLAY_HUNGER_INCREASE = 10

REST_RECOVERY = 25
SICK_REST_RECOVERY = 10
REST_HUNGER_INCREASE = 5

TURN_HUNGER_INCREASE = 5
TURN_FATIGUE_INCREASE = 5
TURN_ENERGY_COST = 5
DAMAGE_PER_CAUSE = 5
SICKNESS_FATIGUE_INCREASE = 5


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи

        :param food: объект еды для кормления
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи

        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи

        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи

        :param medicine: лекарство для лечения
        :return: None
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи

        :return: True если тамагочи болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи
        Должен использоваться после каждого взаимодействия с тамагочи

        :return: None
        """
        raise NotImplementedError

    def ensure_alive(self) -> None:
        """Проверить, что питомец жив, или сообщить о его смерти

        :return: None, если питомец жив
        :raises TamagochiIsGone: если питомец погиб
        """
        if not self.is_alive():
            raise TamagochiIsGone("Питомец погиб")


class SimpleTamagochi(AbstractTamagochi):
    """Питомец с показателями голода, усталости, здоровья и энергии"""

    def __init__(self) -> None:
        """
        Задать начальные показатели здорового питомца

        :return: None
        """
        self._hunger = MIN_STAT
        self._fatigue = MIN_STAT
        self._hp = MAX_STAT
        self._energy = MAX_STAT
        self._sick = False

    @property
    def status(self) -> dict[str, int]:
        """Вернуть текущие показатели питомца

        :return: словарь с показателями питомца
        """
        return {
            "hunger": self._hunger,
            "fatigue": self._fatigue,
            "hp": self._hp,
            "energy": self._energy,
        }

    def is_alive(self) -> bool:
        """Проверить, жив ли питомец

        :return: True если питомец жив, иначе False
        """
        return self._hp >= MIN_STAT

    def is_sick(self) -> bool:
        """Проверить, заболел ли питомец

        :return: True если питомец болеет, иначе False
        """
        return self._sick

    def feed(self, food: Food) -> None:
        """Накормить питомца и потратить
        5 энергии

        :param food: еда с количеством
        насыщения в поле satiety
        :return: None
        :raises TamagochiIsGone: если питомец мертв
        """
        self.ensure_alive()

        self._hunger = max(MIN_STAT, self._hunger - food.satiety)
        self._energy = max(MIN_STAT, self._energy - FEED_ENERGY_COST)

    def play(self) -> None:
        """Поиграть с питомцем, увеличив голод
        и усталость

        :return: None
        :raises TamagochiIsGone: если питомец мертв
        """
        self.ensure_alive()

        self._energy = max(MIN_STAT, self._energy - PLAY_ENERGY_COST)
        self._fatigue = min(MAX_STAT, self._fatigue + PLAY_FATIGUE_INCREASE)
        self._hunger = min(MAX_STAT, self._hunger + PLAY_HUNGER_INCREASE)

    def rest(self) -> None:
        """Восстановить энергию и уменьшить
        усталость питомца

        :return: None
        :raises TamagochiIsGone: если питомец мертв
        """
        self.ensure_alive()

        recovery = SICK_REST_RECOVERY if self.is_sick() else REST_RECOVERY
        self._energy = min(MAX_STAT, self._energy + recovery)
        self._fatigue = max(MIN_STAT, self._fatigue - recovery)
        self._hunger = min(MAX_STAT, self._hunger + REST_HUNGER_INCREASE)

    def heal(self, medicine: Medicine) -> None:
        """Восстановить здоровье питомца и вылечить

        :param medicine: лекарство с кол-ом применений
        :return: None
        :raises TamagochiIsGone: если питомец мертв
        :raises ValueError: если лекарство закончилось
        """
        self.ensure_alive()

        if medicine.is_empty():
            raise ValueError("Лекарство закончилось")

        self._hp = min(MAX_STAT, self._hp + medicine.heal_hp)
        self._sick = False
        medicine.uses += 1

    def update(self) -> None:
        """Обновить показатели питомца за один ход

        :return: None
        :raises TamagochiIsGone: если питомец погиб до или после хода
        """
        self.ensure_alive()

        self._hunger = min(MAX_STAT, self._hunger + TURN_HUNGER_INCREASE)
        self._fatigue = min(MAX_STAT, self._fatigue + TURN_FATIGUE_INCREASE)
        self._energy = max(MIN_STAT, self._energy - TURN_ENERGY_COST)

        if (
            self._hunger >= SICKNESS_THRESHOLD
            or self._fatigue >= SICKNESS_THRESHOLD
        ):
            self._sick = True

        if self._hunger >= SICKNESS_THRESHOLD:
            self._hp -= DAMAGE_PER_CAUSE
        if self._fatigue >= SICKNESS_THRESHOLD or self._energy == 0:
            self._hp -= DAMAGE_PER_CAUSE
        if self.is_sick():
            self._hp -= DAMAGE_PER_CAUSE
            self._fatigue = min(
                MAX_STAT, self._fatigue + SICKNESS_FATIGUE_INCREASE
            )

        self.ensure_alive()
