from connectors.rest_connector import RestConnector
from constants import WEATHER_API_KEY

class WeatherAPIConnector(RestConnector):
    def __init__(self, context):
        super().__init__(
            context=context,
            class_name="WeatherAPIConnector",
            base_url="http://api.weatherapi.com/v1",
            timeout=5
        )

    def get_current_weather(self, city: str):
        endpoint = "/current.json"
        params = {
            "key": WEATHER_API_KEY,
            "q": city,
            "aqi": "no"
        }
        response = self.send(endpoint=endpoint, method="GET", params=params)
        return response.response_json

    def get_forecast_weather(self, city: str, days: int = 3):
        endpoint = "/forecast.json"
        params = {
            "key": WEATHER_API_KEY,
            "q": city,
            "days": days,
            "aqi": "no",
            "alerts": "no"
        }
        response = self.send(endpoint=endpoint, method="GET", params=params)
        return response.response_json
