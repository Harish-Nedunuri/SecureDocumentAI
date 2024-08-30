import logging

logging.getLogger("py4j.java_gateway").setLevel(logging.ERROR)

class CustomLogger:
    def __init__(self,name:str,
    level: str, format: str = "%(asctime)s | %(levelname)s | %(filename)s:%(funcName)s | %(message)s"):
        self.name=name
        self.level=level
        self.format=format
        
    def create_logger(self):
        assert self.level in ["INFO", "DEBUG", "WARNING", "ERROR"], "Illegal log level"
        logger = logging.getLogger(self.name)
        if self.level == "DEBUG":
                logger.setLevel(logging.DEBUG)
        elif self.level == "INFO":
                logger.setLevel(logging.INFO)
        elif self.level == "WARNING":
                logger.setLevel(logging.WARNING)
        elif self.level == "ERROR":
                logger.setLevel(logging.ERROR)

        ch = logging.StreamHandler()
        logger.addHandler(ch)
        formatter = logging.Formatter(self.format)
        ch.setFormatter(formatter)

        return logger

logger_cls = CustomLogger(__name__, "INFO")
logger = logger_cls.create_logger()