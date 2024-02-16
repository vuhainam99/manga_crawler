import logging
from concurrent.futures import ThreadPoolExecutor

_logger = logging.getLogger(__name__)
excutor_thread = ThreadPoolExecutor()


def run_task(func, *args, **kwargs):
    _logger.info("add task run on thread")
    task = excutor_thread.submit(func, *args, **kwargs)
    return task