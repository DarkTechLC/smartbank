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
        '''
        Parameters
        ----------
        type : str
            Tipo de transação
        message : str
            Descrição da transação
        account_id : str
            ID da conta bancária
        timestamp : Optional[datetime]
            Data e hora do registro da transação
        id : Optional[int, None]
            ID do registro da transação
        '''
        self._id = id
        self._type = type
        self._timestamp = timestamp
        self._message = message
        self._account_id = account_id

    @property
    def id(self):
        '''ID do registro da transação.

        Returns
        -------
        int
            ID do registro da transação.
        '''
        return self._id

    @property
    def type(self):
        '''Tipo de transação.

        Returns
        -------
        str
            Tipo de transação.
        '''
        return self._type

    @property
    def timestamp(self):
        '''Data e hora do registro da transação.

        Returns
        -------
        datetime
            Data e hora do registro da transação.
        '''
        return self._timestamp

    @property
    def message(self):
        '''Descrição da transação.

        Returns
        -------
        str
            Descrição da transação.
        '''
        return self._message

    @message.setter
    def message(self, message):
        '''Modifica a descrição da transação.

        Parameters
        ----------
        message : str
            Descrição da transação
        '''
        self._message = message
    
    @property
    def account_id(self):
        '''ID da conta bancária.

        Returns
        -------
        int
            ID da conta bancária.
        '''
        return self._account_id

    def save(self):
        '''Persiste os atributos do objeto no banco de dados.

        Returns
        -------
        bool
            Booleano indicando se a operação foi concluída.
        '''
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
        '''Cria a tabela de histórico de transações no banco de dados.
        '''
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
        '''Obtém a instância de um registro de transação a partir do ID.

        Parameters
        ----------
        identifier : str
            ID do registro de transação

        Returns
        -------
        History
            Instância de um registro de transação.
        None
            Caso não seja encontrada um registro de transação.
        '''
        result = bank_db.search(History.table_name, f'id=%s', params=[identifier], limit=1)
        return History(result[1], result[3], result[4], result[2], result[0]) if result else None

    @staticmethod
    def getAllByAccountId(account_id):
        '''Obtém uma listagem de todos os registros de transações a partir da
        conta bancária.

        Parameters
        ----------
        account_id : int
            ID da conta bancária

        Returns
        -------
        list[History]
            Lista de registros de transações.
        '''
        result = bank_db.search(History.table_name, f'account_id=%s', params=[account_id]) or []
        return list(map(lambda row: History(row[1], row[3], row[4], row[2], row[0]), result))
    