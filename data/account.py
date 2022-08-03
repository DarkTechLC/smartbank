from .history import History


class Account:
    __slots__ = [
        '_code',
        '_owner',
        '_balance',
        '_history',
    ]

    def __init__(self, code, owner, balance=0):
        self._code = code
        self._owner = owner
        self._balance = balance
        self._history = History()

        self._history.add_log('ABERTURA DA CONTA', f'Saldo inicial: {self._format_money(self._balance)}')
    
    @property
    def code(self):
        return self._code
    
    @property
    def owner(self):
        return self._owner
    
    @property
    def balance(self):
        return self._balance
    
    @property
    def balance_fmt(self):
        return self._format_money(self._balance)
    
    @property
    def history(self):
        return self._history
    
    def withdraw(self, amount, type='', log_message=''):
        amount = float(amount)

        if amount <= 0 or self._balance < amount:
            return False

        self._balance -= amount
        self._history.add_log(type or 'SAQUE', log_message or f'Quantia: {self._format_money(amount)}')
        return True

    def deposit(self, amount, type='', log_message=''):
        amount = float(amount)

        if amount <= 0:
            return False
        
        self._balance += amount
        self._history.add_log(type or 'DEPÓSITO', log_message or f'Quantia: {self._format_money(amount)}')
        return True

    def transfer(self, destination, amount):
        if destination.code == self._code:
            return True

        if not self.withdraw(amount, 'TRANSFERÊNCIA ENVIADA', f'Quantia: {self._format_money(amount)}, N° conta destino: {destination.code}'):
            return False
        
        return destination.deposit(amount, 'TRANSFERÊNCIA RECEBIDA', f'Quantia: {self._format_money(amount)}, N° conta origem: {self._code}')
    
    def _format_money(self, amount):
        return f'R$ {float(amount):.2f}'
