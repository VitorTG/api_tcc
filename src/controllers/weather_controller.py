from controllers.base_controller import BaseController
from utils.context import Context
from connectors import WeatherAPIConnector
from dtos import CurrentWeatherDTO
from errors import RequiredParameter

class WeatherController(BaseController):
    def __init__(self, context: Context) -> None:
        super().__init__(context, __name__)
        self.weather_connector = WeatherAPIConnector(context)
        self.current_weather_dto = CurrentWeatherDTO()

    def get_current(self, city=None):
        if city is None:
            raise RequiredParameter("city")
        
        current_weather = self.weather_connector.get_current_weather(city)

        return self.current_weather_dto.obj_to_dict(current_weather)

    def get_forecast(self, city=None):
        if city is None:
            raise RequiredParameter("city")
        
        forecast_weather = self.weather_connector.get_forecast_weather(city)

        return self.forecast_weather_dto.obj_to_dict(forecast_weather)

