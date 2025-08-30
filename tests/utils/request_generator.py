from tests.utils.requisition import ClientRequisition, BaseConnectorResponse


class RequestGenerator:
    @staticmethod
    def POST_create_user(payload: dict) -> BaseConnectorResponse:
        response = ClientRequisition.send(
            "POST",
            "/ufop_api/public/create_user",
            payload=payload,
        )

        return response
    
    @staticmethod
    def POST_validate_user(payload: dict) -> BaseConnectorResponse:
        response = ClientRequisition.send(
            "POST",
            "/ufop_api/public/validate_user",
            payload=payload,
        )

        return response
    
    @staticmethod
    def GET_weather_current(header: dict, city: str) -> BaseConnectorResponse:
        response = ClientRequisition.send(
            "GET",
            f"/ufop_api/public/weather/current?city={city}",
            headers=header,
        )

        return response
    
    @staticmethod
    def GET_weather_forecast(header: dict, city: str) -> BaseConnectorResponse:
        response = ClientRequisition.send(
            "GET",
            f"/ufop_api/public/weather/forecast?city={city}",
            headers=header,
        )

        return response

