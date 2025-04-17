from datetime import datetime

class Logger:
    _instance = None
    logs = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls.logs = []
        return cls._instance

    def log(self, message):
        self.logs.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": message
        })

    def get_logs(self):
        return self.logs
