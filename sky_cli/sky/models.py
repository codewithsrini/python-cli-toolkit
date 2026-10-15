from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Location:
    name: str
    latitude: float
    longitude: float
    country: str
    region: str | None = None  # state / province e.g. Tamil Nadu

    @classmethod
    def from_api(cls, data: dict) -> "Location":
        return cls(
        name=data["name"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        country=data.get("country", ""),
        region=data.get("region", ""),
        )

    @property
    def display_name(self) -> str:
        parts = [self.name, self.country, self.region]
        return ", ".join(p for p in parts if p)


@dataclass(frozen=True)
class CurrentWeather:
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    weather_code: int

    @classmethod
    def from_api(cls, data: dict) -> "CurrentWeather":
        return cls(
            temperature=data["temperature_2m"],
            feels_like=data["aparent_temperature"],
            humidity=data["relative_humidity_2m"],
            wind_speed=data["wind_speed_10m"],
            weather_code=data["weather_code"],
        )


@dataclass(frozen=True)
class DailyForecast:
    day: date
    temp_max: float
    temp_min: float
    rain_chance: int | None
    weather_code: int


@dataclass(frozen=True)
class Forecast:
    location: Location
    current: CurrentWeather
    daily: list[DailyForecast]
    units: str  # "metric" or "imperial"


# def parse_daily(daily: dict) -> list[DailyForecast]:
#     forecasts = []

#     for day_str, t_max, t_min, rain, code in zip(
#         daily["time"],
#         daily["temperature_2m_max"],
#         daily["temperature_2m_min"],
#         daily["precipitation_probability_max"],
#         daily["weather_code"],
#     ):

#     forecast = DailyForecast(
#         day=date.fromisoformat(day_str),
#         temp_max=t_max,
#         temp_min=t_min,
#         rain_chance=rain,
#         weather_code=code,
#     )

#     forecasts.append(forecast)
#     return forecasts

def parse_daily(daily: dict) -> list[DailyForecast]:
    return[
        DailyForecast(
            day=date.fromisoformat(day_str),
            temp_max=t_max,
            temp_min=t_min,
            rain_chance=rain,
            weather_code=code,
        )
        for day_str, t_max, t_min, rain, code in zip(
            daily["time"],
            daily["temperature_2m_max"],
            daily["temperature_2m_min"],
            daily["precipitation_probability_max"],
            daily["weather_code"],
        )
    ]

if __name__ == "__main__":
    result = parse_daily({
        "time": ["2026-10-15", "2026-10-16", "2026-10-17"],
        "temperature_2m_max": [32.1, 31.4, 30.8],
        "temperature_2m_min": [25.0, 24.6, 24.9],
        "precipitation_probability_max": [40, 75, 60],
        "weather_code": [2, 61, 80],
    })

    print( len(result))
    for f in result:
        print(f)