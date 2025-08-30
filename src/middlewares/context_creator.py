import uuid
from falcon import Request

from utils.context import Context


class ContextCreator:
    def process_request(self, req: Request, resp):
        req.context.instance = Context()
