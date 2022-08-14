from datetime import datetime

from data.db import bank_db


class History:
    __slots__ = [
        '_id',
        '_type',
        '_timestamp',
        '_message',
        '_account_id',
    ]

    table_name = 'history'

    def __init__(self, type, message, account_id, timestamp=datetime.today(), id=None):
        self._id = id
        self._type = type
        self._timestamp = timestamp
        self._message = message
        self._account_id = account_id

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        self._message = message
    
    @property
    def account_id(self):
        return self._account_id

    def save(self):
        data = {
            'type': self._type,
            'timestamp': self._timestamp,
            'message': self._message,
            'account_id': self._account_id
        }

        if bool(self._id) and History.get(self._id):
            result = bank_db.update(History.table_name, 'id=%s', data, [self._id])
            return bool(result)

        result = bank_db.insert(History.table_name, data)
        
        if result:
            self._id = result[0]
            return True
        return False

    @staticmethod
    def migrate():
        bank_db.create_table(History.table_name, f'''
			id SERIAL PRIMARY KEY,
            type VARCHAR(30) NOT NULL,
            timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
            message VARCHAR(200) NOT NULL,
            account_id INTEGER NOT NULL,

            FOREIGN KEY (account_id)
                REFERENCES accounts (id)
                ON UPDATE CASCADE ON DELETE CASCADE
        ''')

    @staticmethod
    def get(identifier):
        result = bank_db.search(History.table_name, f'id=%s', params=[identifier], limit=1)
        return History(result[1], result[3], result[4], result[2], result[0]) if result else None

    @staticmethod
    def getAllByAccountId(account_id):
        result = bank_db.search(History.table_name, f'account_id=%s', params=[account_id]) or []
        return list(map(lambda row: History(row[1], row[3], row[4], row[2], row[0]), result))
    