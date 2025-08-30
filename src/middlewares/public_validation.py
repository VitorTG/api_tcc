from falcon import Request, Response
import jwt
from falcon import HTTPUnauthorized
from repositories import UserRepository
from constants import JWT_SECRET
from utils.context import Context

JWT_ALGORITHM = "HS256"

class PublicValidation:
    def process_request(self, req: Request, resp: Response):
        parts_req_path = req.path.split("/")

        if len(parts_req_path) > 3 and parts_req_path[2] == "public":

            if parts_req_path[3] in ["create_user", "validate_user"]:
                return

            auth_header = req.get_header('Authorization')
            if not auth_header:
                raise HTTPUnauthorized(description="Authorization header missing")

            parts = auth_header.split()
            if parts[0].lower() != 'bearer':
                raise HTTPUnauthorized(description="Authorization header must start with Bearer")
            if len(parts) != 2:
                raise HTTPUnauthorized(description="Malformed authorization header")

            token = parts[1]

            try:
                payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            except jwt.ExpiredSignatureError:
                raise HTTPUnauthorized(description="Token expired")
            except jwt.InvalidTokenError:
                raise HTTPUnauthorized(description="Invalid token")

            user_name = payload.get("user_name")
            if not user_name:
                raise HTTPUnauthorized(description="Token missing user_name")

            if not hasattr(req.context, 'instance') or req.context.instance is None:
                req.context.instance = Context()

            if not hasattr(req.context.instance, 'db_session') or req.context.instance.db_session is None:
                from middlewares.session_manager import SessionManager
                req.context.instance.db_session = SessionManager.ThreadSession()

            user = UserRepository(req.context.instance).get_by_user_name(user_name)
            if not user:
                raise HTTPUnauthorized(description="User not found")

            if payload.get("user_key") != user.user_key:
                raise HTTPUnauthorized(description="Token user_key mismatch")

            req.context['user'] = {"user_name": user.user_name, "id": user.id}

        return
