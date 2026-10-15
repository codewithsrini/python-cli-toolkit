import requests

from .errors import WeatherServiceError

TIMEOUT_SECONDS = 10

def get_json(url: str, params: dict, service: str) -> dict:
    try:
        response = requests.get(url, params=params, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        return response.json()
    except requests.Timeout as e:
        raise WeatherServiceError(f"The {service} took too long to respond") from e
    except requests.RequestException as e:
        raise WeatherServiceError(f"Could not reach the {service}: {e}") from e