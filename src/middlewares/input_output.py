from datetime import datetime
from falcon import Request, Response
import json

from utils.context import Context
from utils.logger import Logger

from errors import InvalidSchema
from constants import BYPASS_ENDPOINTS
from copy import deepcopy


class InputOutputMiddleware:
    def process_request(self, req: Request, resp: Response):
        if req.method == "OPTIONS" or req.path in BYPASS_ENDPOINTS:
            return

        logger = Logger(context=req.context.instance, class_name=__name__)
        req.context.instance.timing = {}
        req.context.instance.timing["request_start_time"] = datetime.utcnow()

        self.deserialize_request(req)
        to_log_json = {}
        if req.context.instance.media is not None:
            to_log_json["media"] = req.context.instance.media
        if len(req.params) > 0:
            to_log_json["params"] = req.params

        
        if to_log_json.get("media") is not None:
            if isinstance(to_log_json["media"], dict):
                if to_log_json["media"].get("document_b64") is not None:
                    to_log_json = deepcopy(to_log_json)
                    to_log_json["media"]["document_b64"] = "BASE64 HIDDEN"

        logger.info(
            f"INCOMING REQUEST {req.method} {req.path} {req.remote_addr}",
            to_log_json,
        )

    def process_response(self, req, resp, resource, req_succeeded):
        if req.method == "OPTIONS" or req.path in BYPASS_ENDPOINTS:
            return

        logger = Logger(context=req.context.instance, class_name=__name__)

        req.context.instance.timing["request_finish_time"] = datetime.utcnow()
        start_time = req.context.instance.timing["request_start_time"]
        finish_time = req.context.instance.timing["request_finish_time"]
        total_request_time = (finish_time - start_time).total_seconds() * 1000.0

        logger_media = None
        if resp.media is not None:
            logger_media = deepcopy(resp.media)
        elif resp.data is not None:
            logger_media = json.loads(resp.data.decode("utf8"))

        if logger_media is not None and logger_media.get("document_b64"):
            logger_media["document_b64"] = "BASE64 HIDDEN"

        logger.info(
            f"OUTGOING RESPONSE {resp.status} {req.method} {req.path} {req.remote_addr} {total_request_time} ms",
            logger_media,
        )

    def deserialize_request(self, req: Request):
        binary_data = req.bounded_stream.read()

        ctx = req.context.instance
        ctx: Context
        ctx.binary_body = binary_data

        req_media = None
        if (req.content_length is not None and req.content_length > 0) and (
            req.content_type is None or "json" in req.content_type
        ):
            try:
                req_media = json.loads(binary_data.decode("utf-8"))
            except json.JSONDecodeError:
                raise InvalidSchema("Malformed JSON File")

        ctx.media = req_media
