import logging
import os

class Log:
    def __init__(self, model):
        super().__init__()
        self.logger = logging.getLogger(model)
        log_file_path = f"source/logs/{model}.log"
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        if not os.path.exists(log_file_path):
            with open(log_file_path, 'w+'):
                pass

        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.DEBUG)
            handler = logging.FileHandler(log_file_path)
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
    @property
    def msg(self):
        return self.logger
