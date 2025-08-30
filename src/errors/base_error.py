import falcon
from falcon import Request, Response
class APIException(Exception):
    def __init__(
        self,
        code: str,
        title: str,
        description: str,
        translation: str,
        http_status: int = 400,
    ):
        self.code = code
        self.title = title
        self.description = description
        self.translation = translation
        self.http_status = http_status

    def to_dict(self):
        return {
                "code": self.code,
                "title": self.title,
                "description": self.description,
                "translation": self.translation,
            }

class APIErrorHandler:
    @staticmethod
    def method_not_allowed(exc, req: Request, resp: Response, params):
        error = MethodNotAllowed()
        resp.status = falcon.get_http_status(error.http_status)
        resp.media = error.to_dict()
    
    @staticmethod
    def not_found(exc, req: Request, resp: Response, params):
        error = NotFound("endpoint")
        resp.status = falcon.get_http_status(error.http_status)
        resp.media = error.to_dict()
        
class UserAlreadyExists(APIException):
    def __init__(self, user_name):
        super().__init__(
            code="API_ERROR_0001",
            title="User Already Exists",
            description=f"A user with this username {user_name} already exists in the database.",
            translation=f"Este nome de usuário {user_name} já está em uso.",
            http_status=409,
        )


class InvalidParameter(APIException):
    def __init__(self, detail: str = "Invalid request parameters."):
        super().__init__(
            code="API_ERROR_0002",
            title="Invalid Parameter",
            description=detail,
            translation="Parâmetros inválidos foram fornecidos na requisição.",
            http_status=400,
        )


class NotFound(APIException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            code="API_ERROR_0003",
            title="Not Found",
            description=f"The requested {resource} was not found.",
            translation="O recurso solicitado não foi encontrado.",
            http_status=404,
        )


class MethodNotAllowed(APIException):
    def __init__(self):
        super().__init__(
            code="API_ERROR_0004",
            title="Method Not Allowed",
            description="The HTTP method used is not allowed for this endpoint.",
            translation="O método HTTP usado não é permitido para esse endpoint.",
            http_status=405,
        )


class InternalServerError(APIException):
    def __init__(self, detail: str = "An internal server error occurred."):
        super().__init__(
            code="API_ERROR_0005",
            title="Internal Server Error",
            description=detail,
            translation="Um erro interno ocorreu no servidor.",
            http_status=500,
        )

class InvalidCredentials(APIException):
    def __init__(self, detail: str = "Invalid username or password."):
        super().__init__(
            code="ERR0002",
            title="Invalid Credentials",
            description=detail,
            translation="Nome de usuário ou senha inválidos.",
            http_status=401,
        )

class InvalidSchema(APIException):
    def __init__(self, details="Invalid request schema."):
        super().__init__(
            code="ERR000400",
            title="Invalid Schema",
            description=details,
            translation="Schema da requisição é inválido.",
            http_status=400
        )

class RequiredParameter(APIException):
    def __init__(self, parameter):
        super().__init__(
            code="API_ERROR_0006",
            title="Missing a required parameter.",
            description=f"The {parameter} is a required parameter.",
            translation=f"O parâmetro {parameter} é obrigatório na requisição.",
            http_status=400
        )

        


def error_handler(exc: APIException, req, resp, params):
    resp.status = falcon.get_http_status(exc.http_status)
    resp.media = exc.to_dict()
