from datetime import datetime


class History:
    __slots__ = [
        '_logs',
    ]

    def __init__(self):
        self._logs = []

    @property
    def logs(self):
        return reversed(self._logs)

    def add_log(self, type, message):
        self._logs.append({
            'type': type,
            'timestamp': datetime.today(),
            'message': message
        })
