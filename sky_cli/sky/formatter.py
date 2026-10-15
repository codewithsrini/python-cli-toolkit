from rich.panel import Panel
from rich.table import Table

from .models import Forecast

# WMO weather codes used by Open-Meteo → (label, icon)
WEATHER_CODES: dict[int, tuple[str, str]] = {
    0: ("Clear sky", "☀️"),
    1: ("Mainly clear", "🌤️"),
    2: ("Partly cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Fog", "🌫️"),
    48: ("Icy fog", "🌫️"),
    51: ("Light drizzle", "🌦️"),
    53: ("Drizzle", "🌦️"),
    55: ("Heavy drizzle", "🌦️"),
    61: ("Light rain", "🌧️"),
    63: ("Rain", "🌧️"),
    65: ("Heavy rain", "🌧️"),
    71: ("Light snow", "🌨️"),
    73: ("Snow", "🌨️"),
    75: ("Heavy snow", "❄️"),
    80: ("Rain showers", "🌦️"),
    81: ("Heavy showers", "🌧️"),
    82: ("Violent showers", "⛈️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm with hail", "⛈️"),
    99: ("Severe thunderstorm", "⛈️"),
}


def describe(code: int) -> str:
    label, icon = WEATHER_CODES.get(code, ("Unknown", "❔"))
    return f"{icon}  {label}"


def unit_symbols(units: str) -> tuple[str, str]:
    """Return (temperature symbol, wind speed unit)."""
    return ("°F", "mph") if units == "imperial" else ("°C", "km/h")


def render_current(forecast: Forecast) -> Panel:
    temp, wind = unit_symbols(forecast.units)
    c = forecast.current
    body = (
        f"{describe(c.weather_code)}\n"
        f"Temperature: {c.temperature:.0f}{temp}  (feels like {c.feels_like:.0f}{temp})\n"
        f"Humidity: {c.humidity}%   Wind: {c.wind_speed:.0f} {wind}"
    )
    return Panel(body, title=forecast.location.display_name, expand=False)


def render_daily(forecast: Forecast) -> Table:
    temp, _ = unit_symbols(forecast.units)

    table = Table(title=f"{len(forecast.daily)}-Day Forecast")
    table.add_column("Day")
    table.add_column("Conditions")
    table.add_column("High", justify="right")
    table.add_column("Low", justify="right")
    table.add_column("Rain", justify="right")

    for d in forecast.daily:
        rain = f"{d.rain_chance}%" if d.rain_chance is not None else "–"
        table.add_row(
            d.day.strftime("%a %d %b"),
            describe(d.weather_code),
            f"{d.temp_max:.0f}{temp}",
            f"{d.temp_min:.0f}{temp}",
            rain,
        )

    return table
