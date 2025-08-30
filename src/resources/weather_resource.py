import falcon
from falcon import Request, Response

from controllers import WeatherController



class WeatherResource:
    def on_get_current(self, req: Request, resp: Response):
        weather_controller = WeatherController(req.context.instance)
        city = req.get_param("city")

        sample_entity_dto = weather_controller.get_current(city)

        resp.media = sample_entity_dto
        resp.status = falcon.code_to_http_status(200)

    def on_get_forecast(self, req: Request, resp: Response):
        weather_controller = WeatherController(req.context.instance)
        city = req.get_param("city")

        sample_entity_dto = weather_controller.get_forecast(city)

        resp.media = sample_entity_dto
        resp.status = falcon.code_to_http_status(200)
