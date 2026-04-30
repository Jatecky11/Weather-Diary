import json
import matplotlib.pyplot as plt
from models import SunnyWeather, RainyWeather
from datetime import datetime


class WeatherDiary:
    def __init__(self, filename="data.json"):
        self.filename = filename
        self.entries = self.load_data()

    def add_entry(self, entry):
        self.entries.append(entry)
        self.save_data()

    def delete_entry(self, index):
        if 0 <= index < len(self.entries):
            self.entries.pop(index)
            self.save_data()
            return True
        return False

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([e.to_dict() for e in self.entries], f, indent=4, ensure_ascii=False)

    def load_data(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                entries = []
                for item in data:
                    date = datetime.strptime(item['date'], "%Y-%m-%d")
                    if item['type'] == "RainyWeather":
                        entries.append(RainyWeather(date, item['temperature'], item['description']))
                    else:
                        entries.append(SunnyWeather(date, item['temperature'], item['description']))
                return entries
        except FileNotFoundError:
            return []

    def plot_temperature(self):
        if not self.entries:
            print("Нет данных для графика!")
            return

        # Сортировка по дате для корректного графика
        sorted_entries = sorted(self.entries, key=lambda x: x.date)
        dates = [e.date.strftime("%d.%m") for e in sorted_entries]
        temps = [e.temperature for e in sorted_entries]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, temps, marker='o', linestyle='-', color='b')
        plt.title("Дневник температуры")
        plt.xlabel("Дата")
        plt.ylabel("Температура (°C)")
        plt.grid(True)
        plt.show()