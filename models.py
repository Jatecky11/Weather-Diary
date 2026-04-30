from datetime import datetime

class WeatherEntry:
    def __init__(self, date, temperature, description):
        self._date = date  # Инкапсуляция
        self.temperature = temperature
        self.description = description

    @property
    def date(self):
        return self._date

    def to_dict(self):
        return {
            "date": self.date.strftime("%Y-%m-%d"),
            "temperature": self.temperature,
            "description": self.description,
            "type": self.__class__.__name__
        }

class SunnyWeather(WeatherEntry):
    def __init__(self, date, temperature, description="Ясно"):
        super().__init__(date, temperature, description)
        self.precipitation = 0

class RainyWeather(WeatherEntry):
    def __init__(self, date, temperature, description="Дождь", precipitation=5):
        super().__init__(date, temperature, description)
        self.precipitation = precipitation