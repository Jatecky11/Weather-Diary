
import sys
from datetime import datetime
from manager import WeatherDiary
from models import SunnyWeather, RainyWeather


def get_input(prompt, validator_func, error_msg="Некорректный ввод. Попробуйте снова."):
    """Универсальная функция для валидации ввода."""
    while True:
        data = input(prompt).strip()
        try:
            return validator_func(data)
        except Exception:
            print(f"❌ {error_msg}")


def validate_date(date_str):
    """Проверка формата даты YYYY-MM-DD."""
    return datetime.strptime(date_str, "%Y-%m-%d")


def validate_temp(temp_str):
    """Проверка, что температура — это число в разумных пределах."""
    temp = float(temp_str)
    if not (-100 <= temp <= 70):
        raise ValueError("Температура вне диапазона")
    return temp


def validate_choice(choice_str, min_val, max_val):
    """Проверка выбора пункта меню."""
    val = int(choice_str)
    if not (min_val <= val <= max_val):
        raise ValueError
    return val


def main():
    diary = WeatherDiary()

    while True:
        print("\n" + "=" * 30)
        print("      WEATHER DIARY v1.0")
        print("=" * 30)
        print("1. Добавить запись")
        print("2. Просмотреть все записи")
        print("3. Удалить запись")
        print("4. Построить график")
        print("5. Выход")

        choice = get_input("Выберите пункт (1-5): ", lambda x: validate_choice(x, 1, 5))

        if choice == 1:
            # Валидация даты
            date = get_input(
                "Введите дату (ГГГГ-ММ-ДД): ",
                validate_date,
                "Ошибка! Используйте формат ГГГГ-ММ-ДД (например, 2024-05-20)."
            )

            # Валидация температуры
            temp = get_input(
                "Введите температуру (°C): ",
                validate_temp,
                "Ошибка! Введите числовое значение от -100 до +70."
            )

            desc = input("Краткое описание (например, Облачно): ").strip() or "Без описания"

            is_rainy = input("Были ли осадки? (да/нет): ").lower() == 'да'

            if is_rainy:
                precip = get_input("Уровень осадков (мм): ", float, "Введите число.")
                entry = RainyWeather(date, temp, desc, precip)
            else:
                entry = SunnyWeather(date, temp, desc)

            diary.add_entry(entry)
            print("✅ Запись успешно добавлена!")

        elif choice == 2:
            if not diary.entries:
                print("\n📭 Дневник пока пуст.")
            else:
                print("\n{:<5} {:<12} {:<10} {:<15}".format("ID", "Дата", "Темп.", "Описание"))
                print("-" * 45)
                for i, e in enumerate(diary.entries):
                    print(f"{i:<5} {e.date.strftime('%Y-%m-%d'):<12} {e.temperature:<10} {e.description:<15}")

        elif choice == 3:
            if not diary.entries:
                print("Удалять нечего.")
                continue

            idx = get_input(
                "Введите ID записи для удаления: ",
                lambda x: validate_choice(x, 0, len(diary.entries) - 1),
                "Ошибка! Введите существующий ID."
            )
            if diary.delete_entry(idx):
                print("🗑️  Запись удалена.")

        elif choice == 4:
            print("📊  Формирование графика...")
            diary.plot_temperature()

        elif choice == 5:
            print("До свидания!")
            sys.exit()


if __name__ == "__main__":
    main()
