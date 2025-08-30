from tests.utils.requisition import ClientRequisition


class TestHealthCheck:
    def test_health_check(self):
        response = ClientRequisition.send("GET", "/ufop_api/health_check")
        assert response.response_status == 204

    def test_no_token(self):
        response = ClientRequisition.send("PUT", "/ufop_api/sample")
        assert response.response_status == 404
        assert response.response_json["code"] == "API_ERROR_0003"


    def test_method_not_allowed(self):
        response = ClientRequisition.send("PUT", "/ufop_api/health_check")
        assert response.response_status == 405
        assert response.response_json["code"] == "API_ERROR_0004"

    def test_secure_headers_middleware(self):
        response = ClientRequisition.send("GET", "/ufop_api/health_check")
        assert response.response_status == 204
        headers_response = response.response.headers
        assert headers_response["Server"] == "undisclosed"
        assert headers_response["x-frame-options"] == "SAMEORIGIN"
        assert headers_response["x-xss-protection"] == "1; mode=block"
        assert headers_response["x-content-type-options"] == "nosniff"
        assert headers_response["strict-transport-security"] == "max-age=63072000; includeSubdomains"
        assert headers_response["content-security-policy"] == "default-src 'self'"


    # TODO - Teste de rate limit atrapalha os outros testes, tem que fazer um reset de tempo na função ou algo assim.
    # def test_rate_limit(self):
    #     headers = {"X-Forwarded-For": "123.123.123.123"}
    #     last_status = None
    #     for i in range(105): 
    #         response = ClientRequisition.send("GET", "/ufop_api/health_check", headers=headers)
    #         last_status = response.response_status

    #     assert last_status == 429 