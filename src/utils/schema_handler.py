import os
from json import JSONDecodeError
import json
import functools
from constants import SCHEMA_PATH

from jsonschema import validate, RefResolver, ValidationError
from errors import InvalidSchema


class SchemaCache:
    schemas = {}

    @staticmethod
    def getSchema(schema_file_name):
        schema_path = SCHEMA_PATH + schema_file_name

        if not os.path.isfile(schema_path):
            raise Exception(
                "Internal Error",
                "There was an internal error loading JSON Schema - " + schema_file_name,
            )

        if schema_path in SchemaCache.schemas:
            return SchemaCache.schemas[schema_path]

        try:
            SchemaCache.schemas[schema_path] = json.loads(open(schema_path, "r").read())
            return SchemaCache.schemas[schema_path]
        except JSONDecodeError:
            raise Exception("Internal Error", "There was an internal error validating JSON Schema")
        except IOError:
            raise Exception("Internal Error", "There was an internal error validating JSON Schema")


class SchemaHandler:
    @staticmethod
    def validate(schema_file_name):
        def decorator_validate(func):
            @functools.wraps(func)
            def wrapper_validate(*args, **kwargs):
                req = args[1]

                schema_file = SchemaCache.getSchema(schema_file_name)
                resolver = RefResolver("file://%s" % SCHEMA_PATH, None)
                try:
                    validate(req.context.instance.media, schema_file, resolver=resolver)
                except ValidationError as ex:
                    absolute_path = ex.absolute_path
                    if absolute_path:
                        error_path = ".".join(str(part) for part in absolute_path)
                        error_message = f"{ex.message} in {error_path}"
                    else:
                        error_message = str(ex.message)
                    raise InvalidSchema(error_message)

                value = func(*args, **kwargs)
                return value

            return wrapper_validate

        return decorator_validate
