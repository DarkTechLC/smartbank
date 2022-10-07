from lib.crypt import Crypt
from data.db import bank_db
from .account import Account


class Client:
    '''Classe modelo que realiza as operações na tabela de clientes.

    Attributes
    ----------
    id : int
        ID do cliente
    name : str
        Nome do cliente
    cpf : str
        CPF do cliente
    password : str
        Senha de acesso do cliente
    account : Account
        Conta bancária do cliente

    Methods
    -------
    save()
        Persiste os atributos do objeto no banco de dados
    migrate():
        Cria a tabela de clientes no banco de dados
    get(identifier)
        Obtém a instância de um cliente a partir do ID ou CPF
    getAll()
        Obtém uma listagem de todos os clientes
    '''
    __slots__ = [
        '_id',
        '_name',
        '_cpf',
        '_password',
    ]

    table_name = 'clients'

    def __init__(self, name, cpf, password, id=None):
        '''
        Parameters
        ----------
        name : str
            Nome do cliente
        cpf : str
            CPF do cliente
        password : str
            Senha de acesso do cliente
        id : Optional[int, None]
            ID do cliente
        '''
        self._id = id
        self._name = name
        self._cpf = cpf
        self._password = password

    @property
    def id(self):
        '''ID do cliente.

        Returns
        -------
        int
            ID do cliente.
        '''
        return self._id

    @property
    def name(self):
        '''Nome do cliente.

        Returns
        -------
        str
            Nome do cliente.
        '''
        return self._name

    @name.setter
    def name(self, name):
        '''Modifica o nome do cliente.

        Parameters
        ----------
        name : str
            Nome do cliente
        '''
        self._name = name
    
    @property
    def cpf(self):
        '''CPF do cliente.

        Returns
        -------
        str
            CPF do cliente.
        '''
        return self._cpf
    
    @property
    def password(self):
        '''Senha de acesso do cliente.

        Returns
        -------
        str
            Senha de acesso do cliente.
        '''
        return self._password

    @password.setter
    def password(self, password):
        '''Modifica a senha do cliente.

        Parameters
        ----------
        password : str
            Senha do cliente
        '''
        self._password = password

    @property
    def account(self):
        '''Conta bancária do cliente.

        Returns
        -------
        Account
            Conta bancária do cliente.
        '''
        return Account.get(self._id)

    def save(self):
        '''Persiste os atributos do objeto no banco de dados.

        Returns
        -------
        bool
            Booleano indicando se a operação foi concluída.
        '''
        data = {
            'name': self._name,
            'cpf': self._cpf,
            'password': Crypt.hash(self._password),
        }

        # TODO: update hashed password only when it changes
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
        '''Cria a tabela de clientes no banco de dados.
        '''
        bank_db.create_table(Client.table_name, '''
			id SERIAL PRIMARY KEY,
            name VARCHAR(150) NOT NULL,
            cpf VARCHAR(11) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL
        ''')

    @staticmethod
    def get(identifier):
        '''Obtém a instância de um cliente a partir do ID ou CPF.

        Parameters
        ----------
        identifier : Union[int, str]
            ID ou CPF do cliente

        Returns
        -------
        Client
            Instância de um cliente.
        None
            Caso não seja encontrada um cliente.
        '''
        identifier = str(identifier)
        result = bank_db.search(Client.table_name, f'(id::varchar=%s) OR (cpf=%s)', params=[identifier, identifier], limit=1)
        return Client(result[1], result[2], result[3], result[0]) if result else None

    @staticmethod
    def getAll():
        '''Obtém uma listagem de todos os clientes.

        Returns
        -------
        list[Client]
            Lista de clientes.
        '''
        result = bank_db.search(Client.table_name) or []
        return list(map(lambda row: Client(row[1], row[2], row[3], row[0]), result))
