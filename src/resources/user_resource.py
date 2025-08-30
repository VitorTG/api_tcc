import falcon
from falcon import Request, Response

from controllers import UserController
from dtos import UserDTO
from utils.schema_handler import SchemaHandler


class UserResource:
    @SchemaHandler.validate("incoming_user.json")
    def on_post_create_user(self, req: Request, resp: Response):
        user_controller = UserController(req.context.instance)
        incoming_schema = req.context.instance.media

        user = user_controller.create_user(incoming_schema)

        resp.media = UserDTO.only_obj_key(user)
        resp.status = falcon.code_to_http_status(201)

    @SchemaHandler.validate("incoming_user.json")
    def on_post_validate_user(self, req: Request, resp: Response):
        user_controller = UserController(req.context.instance)
        incoming_schema = req.context.instance.media

        token = user_controller.validate_user(incoming_schema)

        resp.media = UserDTO.login_success(token)
        resp.status = falcon.code_to_http_status(201)


    @SchemaHandler.validate("put_user.json")
    def on_put_by_key(self, req: Request, resp: Response, user_key: str):

        user_controller = UserController(req.context.instance)

        user_dto = user_controller.update_status(user_key, req.context.instance.media)

        resp.media = user_dto
        resp.status = falcon.code_to_http_status(202)

    def on_put_webhook_increment_counter(self, req: Request, resp: Response, user_key: str):

        user_controller = UserController(req.context.instance)

        user_controller.webhook_increment_counter(user_key)

        resp.status = falcon.code_to_http_status(204)

    def on_get_list(self, req: Request, resp: Response):
        user_controller = UserController(req.context.instance)

        limit = req.get_param_as_int(name="limit", min_value=0, max_value=100, default=10)
        page = req.get_param_as_int(name="page", min_value=0, default=0)
        offset = page * limit

        status = req.get_param("status")

        filters_dict = {"status": status}

        sample_entities_page = user_controller.get_list(limit, offset, filters_dict)
        sample_entities_list_dto = sample_entities_page["sample_entities_list_dto"]
        is_last_page = sample_entities_page["is_last_page"]

        resp.media = dict()
        resp.media["data"] = sample_entities_list_dto
        resp.media["limit"] = limit
        resp.media["page"] = page
        resp.media["is_last_page"] = is_last_page

        resp.status = falcon.code_to_http_status(200)
