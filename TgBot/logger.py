import logging

class customLogger:
    def Log(self, log_level=logging.INFO, filename="bot.log"):
        logger = logging.getLogger("test")
        logger.setLevel(log_level)
        fh = logging.FileHandler(filename)
        formatter = logging.Formatter('%(asctime)s   %(levelname)s: %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger
