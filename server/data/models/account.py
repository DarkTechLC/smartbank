from data.db import bank_db
from .history import History


class Account:
    '''Classe modelo que realiza as operações na tabela de contas bancárias.

    Attributes
    ----------
    id : int
        ID da conta bancária
    code : str
        Número da conta formatado
    balance : float
        Saldo da conta
    balance_fmt : str
        Saldo da conta formatado em reais
    history : list[History]
        Obtém o histórico de transações da conta bancária atual

    Methods
    -------
    withdraw(amount)
        Realiza a operação de saque na conta atual
    deposit(amount)
        Realiza a operação de depósito na conta atual
    transfer(destination, amount):
        Realiza a operação de transferência entre contas a partir da conta
        atual.
    save():
        Persiste os atributos do objeto no banco de dados
    format_money(amount):
        Formata um valor em reais
    migrate():
        Cria a tabela de contas bancárias no banco de dados
    get(identifier):
        Obtém a instância de uma conta a partir do ID
    '''
    __slots__ = [
        '_id',
        '_balance',
    ]

    table_name = 'accounts'

    def __init__(self, owner_id, balance=0.0):
        '''
        Parameters
        ----------
        owner_id : id
            ID do cliente dono da conta.
        balance : float
            Saldo bancário.
        '''
        self._id = owner_id
        self._balance = balance
    
    @property
    def id(self):
        '''ID da conta bancária.

        Returns
        -------
        int
            ID da conta bancária.
        '''
        return self._id
    
    @property
    def code(self):
        '''Número da conta formatado.

        Returns
        -------
        str
            Número da conta formatado.
        '''
        return str(self._id).zfill(4)
    
    @property
    def balance(self):
        '''Saldo da conta.

        Returns
        -------
        float
            Saldo da conta.
        '''
        return self._balance
    
    @property
    def balance_fmt(self):
        '''Saldo da conta formatado em reais.

        Returns
        -------
        str
            Saldo formato em reais (R$).
        '''
        return Account.format_money(self._balance)
    
    @property
    def history(self):
        '''Obtém o histórico de transações da conta bancária atual.

        Returns
        -------
        list[History]
            Lista com o histórico de transações.
        '''
        return History.getAllByAccountId(self._id)
    
    def withdraw(self, amount):
        '''Realiza a operação de saque na conta atual.

        Parameters
        ----------
        amount : float
            Quantia a ser sacada

        Returns
        -------
        bool
            Booleano indicando se a operação foi concluída.
        '''
        amount = float(amount)

        if amount <= 0 or self._balance < amount:
            return False

        self._balance -= amount
        self.save()
        return True

    def deposit(self, amount):
        '''Realiza a operação de depósito na conta atual.

        Parameters
        ----------
        amount : float
            Quantia a ser depositada

        Returns
        -------
        bool
            Booleano indicando se a operação foi concluída.
        '''
        amount = float(amount)

        if amount <= 0:
            return False
        
        self._balance += amount
        self.save()
        return True

    def transfer(self, destination, amount):
        '''Realiza a operação de transferência entre contas a partir da conta
        atual.

        Parameters
        ----------
        destination : Account
            Objeto que representa a conta de destino para onde será realizada
            a transferência.
        amount : float
            Quantia a ser transferida

        Returns
        -------
        bool
            Booleano indicando se a operação foi concluída.
        '''
        if destination.code == self.code:
            return True

        if not self.withdraw(amount):
            return False
        
        return destination.deposit(amount)

    def save(self):
        '''Persiste os atributos do objeto no banco de dados.

        Returns
        -------
        bool
            Booleano indicando se a operação foi concluída.
        '''
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
        '''Formata um valor em reais.

        Parameters
        ----------
        amount : float
            Valor em ponto flutuante

        Returns
        -------
        str
            Valor com formatação em reais.
        '''
        return f'R$ {float(amount):.2f}'

    @staticmethod
    def migrate():
        '''Cria a tabela de contas bancárias no banco de dados.
        '''
        bank_db.create_table(Account.table_name, f'''
			id INTEGER PRIMARY KEY,
            balance FLOAT NOT NULL DEFAULT 0,

            FOREIGN KEY (id)
                REFERENCES clients (id)
                ON UPDATE CASCADE ON DELETE CASCADE
        ''')

    @staticmethod
    def get(identifier):
        '''Obtém a instância de uma conta a partir do ID.

        Parameters
        ----------
        identifier : int
            ID da conta bancária

        Returns
        -------
        Account
            Instância de uma conta bancária.
        None
            Caso não seja encontrada uma conta.
        '''
        result = bank_db.search(Account.table_name, f'id=%s', params=[identifier], limit=1)
        return Account(result[0], result[1]) if result else None
