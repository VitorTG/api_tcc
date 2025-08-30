import falcon


class HealthCheckResource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_204
