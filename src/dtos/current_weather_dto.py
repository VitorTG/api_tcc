class CurrentWeatherDTO:
    @staticmethod
    def obj_to_dict(api_response: dict) -> dict:
        return {
            "location": {
                "name": api_response["location"]["name"],
                "region": api_response["location"]["region"],
                "country": api_response["location"]["country"],
                "local_time": api_response["location"]["localtime"]
            },
            "current": {
                "temperature_c": api_response["current"]["temp_c"],
                "condition": api_response["current"]["condition"]["text"],
                "wind_kph": api_response["current"]["wind_kph"],
                "humidity": api_response["current"]["humidity"],
                "feelslike_c": api_response["current"]["feelslike_c"]
            }
        }
