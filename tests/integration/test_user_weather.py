from tests.utils import RequestGenerator, DbUtils


class TestWeather:
    def test_create_user(self):
        DbUtils.rollback()

        payload = {
                    "user_name": "Tavares",
                    "password": "teste_123"
                }
        response = RequestGenerator.POST_create_user(payload)
        assert response.response_status == 201


    def test_validate_user(self):
        DbUtils.rollback()

        payload = {
                    "user_name": "Tavares",
                    "password": "teste_123"
                }
        response = RequestGenerator.POST_create_user(payload)
        assert response.response_status == 201

        response = RequestGenerator.POST_validate_user(payload)
        assert response.response_status == 201

    def test_validate_access_token(self):
        DbUtils.rollback()

        payload = {
                    "user_name": "Tavares",
                    "password": "teste_123"
                }
        response = RequestGenerator.POST_create_user(payload)
        assert response.response_status == 201

        response = RequestGenerator.POST_validate_user(payload)
        assert response.response_status == 201


    def test_get_weather_current(self):
        DbUtils.rollback()

        payload = {
                    "user_name": "Tavares",
                    "password": "teste_123"
                }
        response = RequestGenerator.POST_create_user(payload)
        assert response.response_status == 201

        response = RequestGenerator.POST_validate_user(payload)
        assert response.response_status == 201

        access_token = response.response_json["access_token"]

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = RequestGenerator.GET_weather_current(headers, "Ouro Preto")
        assert response.response_status == 200