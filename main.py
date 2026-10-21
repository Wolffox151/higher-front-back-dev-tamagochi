from collections.abc import Callable

from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi
from game.clicker import SimpleRandomClicker
from game.game import AbstractGame, SimpleGame
from game.exceptions import NotEnoughMoney, TamagochiIsGone


def create_game() -> AbstractGame:
    """Создать игру с питомцем, кликером и каталогами товаров

    :return: готовый экземпляр игры
    """
    all_food = [
        Food(name='Бургер', satiety=20, price=40),
        Food(name='Салат', satiety=10, price=20),
        Food(name='Яблоко', satiety=10, price=15),
    ]
    all_medicine = [
        Medicine(name='Ибупрофен', price=30, heal_hp=20, number_of_uses=2),
    ]
    tamagochi = SimpleTamagochi()
    clicker = SimpleRandomClicker(10, 20)
    return SimpleGame(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine,
    )


def display_game(game: AbstractGame, message: str) -> None:
    """Вывести сообщение, состояние игры и меню действий

    :param game: текущая игра
    :param message: результат предыдущего действия или сообщение об ошибке
    :return: None
    """
    print(message)

    print(f"Сумка с едой: {game.food}")
    print(f"Сумка с лекарствами: {game.medicine}")

    status = game.get_status()
    print(
        f"\nСтатус: голод {status['hunger']}, "
        f"усталость {status['fatigue']}, здоровье {status['hp']}, "
        f"энергия {status['energy']}, монет {status['coins']}\n"
    )
    if game.tamagochi.is_sick():
        print("=======Тамагочи болеет======")
        print("=======Отдых действует менее эффективно=======")
    print("1. Пойти на работу")
    print("2. Купить еду")
    print("3. Купить лекарство")
    print("4. Покормить")
    print("5. Вылечить")
    print("6. Играть")
    print("7. Отдых")
    print("0. Выход")


def execute_action(game: AbstractGame, command: str) -> str:
    """Выполнить игровое действие и вернуть сообщение о результате

    :param game: текущая игра
    :param command: номер действия
    :return: сообщение об успешном действии
    :raises ValueError: если команда неизвестна или действие недопустимо
    :raises NotEnoughMoney: если не хватает монет для покупки
    :raises TamagochiIsGone: если питомец погиб
    """
    if command == "1":
        income = game.work()
        return f"Вы заработали {income} монет"

    actions: dict[str, tuple[Callable[[], None], str]] = {
        "2": (game.buy_food, "Еда куплена"),
        "3": (game.buy_medicine, "Лекарство куплено"),
        "4": (game.feed_tamagochi, "Питомец накормлен"),
        "5": (game.heal_tamagochi, "Питомец получил лекарство"),
        "6": (game.play_with_tamagochi, "Вы поиграли с питомцем"),
        "7": (game.rest_tamagochi, "Питомец отдохнул"),
    }
    selected_action = actions.get(command)
    if selected_action is None:
        raise ValueError("Неверная команда")

    action, message = selected_action
    action()
    return message


def main() -> None:
    """Запустить игру и обрабатывать команды до её завершения

    :return: None.
    """
    game = create_game()
    print("Добро пожаловать в Тамагочи-кликер!")
    output = ''

    while True:
        display_game(game, output)

        try:
            command = input("Выберите действие: ").strip()
            if command == "0":
                break
            output = execute_action(game, command)
            game.tamagochi.update()
        except TamagochiIsGone as error:
            print(f"\n{error}. Игра окончена.")
            break
        except (NotEnoughMoney, ValueError) as error:
            output = str(error)
        except (EOFError, KeyboardInterrupt):
            print("\nИгра завершена.")
            break


if __name__ == "__main__":
    main()
