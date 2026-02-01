
import logging
import functools

class LoggingHandler:
    def __init__(self, name="csv_transformer"):
        self.logger = logging.getLogger(name)
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.INFO)
            handler     = logging.StreamHandler()
            formatter   = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def log(self, func):
        """Log entry and exit of a function/method"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.logger.info(f"Entering {func.__qualname__}")
            result = func(*args, **kwargs)
            self.logger.info(f"Exiting {func.__qualname__}")
            return result
        return wrapper

    def catch(self, func):
        """Catch and log exceptions"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.logger.exception(
                    f"Exception in {func.__qualname__}: {e}"
                )
                raise
        return wrapper


# one shared logger instance (singleton)
logging_handler = LoggingHandler()
