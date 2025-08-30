import falcon
from resources import (WeatherResource, HealthCheckResource, UserResource)
from errors.base_error import APIException, error_handler
from middlewares import (SessionManager, ContextCreator, InputOutputMiddleware, SecureHeaders, PublicValidation, RateLimit)
from errors import APIErrorHandler

def create():
    api = falcon.App(middleware=[
        ContextCreator(), SessionManager(), 
        InputOutputMiddleware(), SecureHeaders(), 
        PublicValidation(), RateLimit(limit=100, window=60)
        ])

    health_check_resource = HealthCheckResource()
    api.add_route("/ufop_api/health_check", health_check_resource)

    user_resource = UserResource()
    api.add_route("/ufop_api/public/create_user", user_resource, suffix="create_user")
    api.add_route("/ufop_api/public/validate_user", user_resource, suffix="validate_user")

    weather_resource = WeatherResource()
    api.add_route("/ufop_api/public/weather/current", weather_resource, suffix="current")
    api.add_route("/ufop_api/public/weather/forecast", weather_resource, suffix="forecast")
    
    return api


def main():
    api = create()

    api.add_error_handler(falcon.errors.HTTPNotFound, APIErrorHandler.not_found)
    api.add_error_handler(falcon.errors.HTTPMethodNotAllowed, APIErrorHandler.method_not_allowed)
    
    api.add_error_handler(APIException, error_handler)
    
    return api


application = main()
