import uuid
import time

from utils.context import Context
from utils.logger import Logger


class BasicOperation:
    def __init__(self, context: Context, operation_name="", logger_name=__name__):
        self.context = context
        self.logger = Logger(context, logger_name)
        self.operation_id = str(uuid.uuid4())
        self.operation_name = operation_name
        self.start_time = None
        self.stop_time = None
        self.took = BasicOperation.__now()

    def start(self):
        self.start_time = BasicOperation.__now()
        self.context.add_operation(self.operation_id)
        self.logger.debug("Operation %s %s has started" % (self.operation_id, self.operation_name))

    def stop(self):
        self.stop_time = BasicOperation.__now()
        self.took = self.stop_time - self.start_time

    def finish(self):
        self.logger.debug("Operation %s %s finished in %s ms" % (self.operation_id, self.operation_name, self.took))
        self.context.remove_operation(self.operation_id)

    def stop_and_finish(self):
        self.stop()
        self.finish()

    @staticmethod
    def __now():
        return int(round(time.time() * 1000))
