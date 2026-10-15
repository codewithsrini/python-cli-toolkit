import argparse

from rich.console import Console

from .errors import SkyError
from .formatter import render_current, render_daily
from .geocoding import search_locations
from .models import Location
from .weather import fetch_forecast


def forecast_days(value: str) -> int:
    """argparse type: a whole number from 1 to 16 (Open-Meteo's limit)."""
    try:
        days = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' is not a whole number")
    if not 1 <= days <= 16:
        raise argparse.ArgumentTypeError("must be between 1 and 16")
    return days


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sky",
        description="Current weather and forecast for any city.",
    )
    parser.add_argument("city", nargs="+", help="city name, e.g. Chennai or New York")
    parser.add_argument("-d", "--days", type=forecast_days, default=3,
                        help="forecast days, 1-16 (default: 3)")
    parser.add_argument("-u", "--units", choices=["metric", "imperial"], default="metric",
                        help="unit system (default: metric)")
    parser.add_argument("-p", "--pick", action="store_true",
                        help="choose from all matching places instead of the top match")
    return parser


def choose_location(locations: list[Location], console: Console) -> Location:
    console.print("Multiple matches found:")
    for i, loc in enumerate(locations, start=1):
        console.print(f"  {i}. {loc.display_name}")

    while True:
        choice = console.input("Pick a number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(locations):
            return locations[int(choice) - 1]
        console.print(f"[red]Please enter a number from 1 to {len(locations)}.[/red]")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    city = " ".join(args.city)
    console = Console()

    try:
        locations = search_locations(city)

        if args.pick and len(locations) > 1:
            location = choose_location(locations, console)
        else:
            location = locations[0]
            if len(locations) > 1:
                console.print(f"[dim]Showing {location.display_name}. "
                              f"Use --pick to choose from {len(locations)} matches.[/dim]")

        with console.status("Fetching weather..."):
            forecast = fetch_forecast(location, days=args.days, units=args.units)

    except SkyError as e:
        console.print(f"[red]Error:[/red] {e}")
        return 1
    except KeyboardInterrupt:
        console.print("\nCancelled.")
        return 130

    console.print(render_current(forecast))
    console.print(render_daily(forecast))
    return 0