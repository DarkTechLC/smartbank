import random, string

from lib.crypt import Crypt
from .bank_handler import Bank


class Session:
    '''Classe que permite gerenciar as sessões dos usuários.

    Methods
    -------
    get_id_by_token(token)
        Obtém o ID do usuário a partir do token salvo nas sessões
    check(token)
        Verifica se o token existe nas sessões salvas
    login(cpf, password)
        Cria a sessão de um usuário a partir do CPF e senha
    add(client_id)
        Cria a sessão de um usuário a partir do ID
    logout(token)
        Deleta a sessão de um usuário a partir do token
    '''
    __slots__ = [
        '_db',
        '_session_tokens',
    ]

    def __init__(self, db: Bank):
        '''
        Parameters
        ----------
        db : Bank
            Instância do manipulador do banco de dados.
        '''
        self._db = db
        self._session_tokens = {}

    def get_id_by_token(self, token):
        '''Obtém o ID do usuário a partir do token salvo nas sessões.

        Parameters
        ----------
        token : str
            Token do usuário

        Returns
        -------
        str
            ID do usuário.
        None
            Caso o token não exista nas sessões salvas.
        '''
        if self.check(token):
            return self._session_tokens[token]
        return None

    def check(self, token):
        '''Verifica se o token existe nas sessões salvas.

        Parameters
        ----------
        token : str
            Token do usuário

        Returns
        -------
        bool
            Booleano indicando se o token existe nas sessões salvas.
        '''
        return token in self._session_tokens

    def login(self, cpf, password):
        '''Cria a sessão de um usuário a partir do CPF e senha.

        Parameters
        ----------
        cpf : str
            CPF do usuário
        password : str
            Senha do usuário
        
        Returns
        -------
        str
            Token gerado.
        '''
        client = self._db.get_client(cpf)

        if not client:
            return None

        if not Crypt.compare(password, client.password):
            return None
        return self.add(client.id)

    def add(self, client_id):
        '''Cria a sessão de um usuário a partir do ID.

        Parameters
        ----------
        client_id : Union[str, int]
            ID do usuário
        
        Returns
        -------
        str
            Token gerado.
        '''
        token = f'{self._generate_token()}_{client_id}'
        self._session_tokens[token] = client_id
        return token

    def logout(self, token):
        '''Deleta a sessão de um usuário a partir do token.

        Parameters
        ----------
        token : str
            Token do usuário
        '''
        if self.check(token):
            del self._session_tokens[token]

    def _generate_token(self, size=10):
        '''Gera um token de tamanho determinado.

        Parameters
        ----------
        size : int
            Comprimento do token
        
        Returns
        -------
        str
            Token gerado.
        '''
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(size))
