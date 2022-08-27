from data.db import bank_db
from .history import History


class Account:
    __slots__ = [
        '_id',
        '_balance',
    ]

    table_name = 'accounts'

    def __init__(self, owner_id, balance=0.0):
        self._id = owner_id
        self._balance = balance
    
    @property
    def id(self):
        return self._id
    
    @property
    def code(self):
        return str(self._id).zfill(4)
    
    @property
    def balance(self):
        return self._balance
    
    @property
    def balance_fmt(self):
        return Account.format_money(self._balance)
    
    @property
    def history(self):
        return History.getAllByAccountId(self._id)
    
    def withdraw(self, amount):
        amount = float(amount)

        if amount <= 0 or self._balance < amount:
            return False

        self._balance -= amount
        self.save()
        return True

    def deposit(self, amount):
        amount = float(amount)

        if amount <= 0:
            return False
        
        self._balance += amount
        self.save()
        return True

    def transfer(self, destination, amount):
        if destination.code == self.code:
            return True

        if not self.withdraw(amount):
            return False
        
        return destination.deposit(amount)

    def save(self):
        data = {
            'id': self._id,
            'balance': self._balance,
        }

        if Account.get(self._id):
            result = bank_db.update(Account.table_name, 'id=%s', data, [self._id])
            return bool(result)

        result = bank_db.insert(Account.table_name, data)
        
        if result:
            self._id = result[0]
            return True
        return False

    @staticmethod
    def format_money(amount):
        return f'R$ {float(amount):.2f}'

    @staticmethod
    def migrate():
        bank_db.create_table(Account.table_name, f'''
			id INTEGER PRIMARY KEY,
            balance FLOAT NOT NULL DEFAULT 0,

            FOREIGN KEY (id)
                REFERENCES clients (id)
                ON UPDATE CASCADE ON DELETE CASCADE
        ''')

    @staticmethod
    def get(identifier):
        result = bank_db.search(Account.table_name, f'id=%s', params=[identifier], limit=1)
        return Account(result[0], result[1]) if result else None
