class SkyError(Exception):
    """Base class for all the error exception"""

class LocationNotFoundError(SkyError):
    """The city name didn't match any place"""

class WeatherServiceError(SkyError):
    """The API was unreachable, slow or returned an error."""

