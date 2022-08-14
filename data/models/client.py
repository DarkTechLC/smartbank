from data.db import bank_db
from .account import Account


class Client:
    __slots__ = [
        '_id',
        '_name',
        '_cpf',
        '_password',
    ]

    table_name = 'clients'

    def __init__(self, name, cpf, password, id=None):
        self._id = id
        self._name = name
        self._cpf = cpf
        self._password = password

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def account(self):
        return Account.get(self._id)

    def save(self):
        data = {
            'name': self._name,
            'cpf': self._cpf,
            'password': self._password,
        }

        if bool(self._id) and Client.get(self._id):
            result = bank_db.update(Client.table_name, 'id=%s', data, [self._id])
            return bool(result)

        result = bank_db.insert(Client.table_name, data)
        
        if result:
            self._id = result[0]
            return True
        return False

    @staticmethod
    def migrate():
        bank_db.create_table(Client.table_name, '''
			id SERIAL PRIMARY KEY,
            name VARCHAR(150) NOT NULL,
            cpf VARCHAR(11) NOT NULL UNIQUE,
            password VARCHAR(30) NOT NULL
        ''')

    @staticmethod
    def get(identifier):
        identifier = str(identifier)
        result = bank_db.search(Client.table_name, f'(id::varchar=%s) OR (cpf=%s)', params=[identifier, identifier], limit=1)
        return Client(result[1], result[2], result[3], result[0]) if result else None

    @staticmethod
    def getAll():
        result = bank_db.search(Client.table_name) or []
        return list(map(lambda row: Client(row[1], row[2], row[3], row[0]), result))
