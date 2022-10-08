class Session:
	'''Classe que permite gerenciar a sessão do usuário.

	Attributes
    ----------
	token : str
		Token salvo na sessão do usuário
	has_session : bool
		Verifica se o usuário tem uma sessão ativa

    Methods
    -------
    login(token)
        Cria a sessão do usuário a partir do token
    logout()
        Deleta a sessão do usuário
    '''
	__slots__ = [
		'_client',
		'_session_token',
	]

	def __init__(self, client):
		'''
		Parameters
        ----------
		client : BankClient
			Instância do cliente que conecta com o servidor do banco
		'''
		self._client = client
		self._session_token = None

	@property
	def token(self):
		'''Token salvo na sessão do usuário.
        
        Returns
        -------
        str
            Token salvo.
        '''
		return self._session_token

	@property
	def has_session(self):
		'''Verifica se o usuário tem uma sessão ativa.

        Returns
        -------
        bool
            Booleano indicando se o usuário tem uma sessão ativa.
        '''
		return bool(self._session_token) and self._client.client_is_logged()

	def login(self, token):
		'''Cria a sessão do usuário a partir do token.

		Parameters
        ----------
		token : str
			Token de autorização do usuário
		'''
		self._session_token = token
		return True

	def logout(self):
		'''Deleta a sessão do usuário.
		'''
		self._session_token = None
		return True
