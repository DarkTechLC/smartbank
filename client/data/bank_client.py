import socket
import json

from .session import Session


class BankClient:
	'''Cliente que conecta com o servidor do banco para fornecer as ações.

	Attributes
    ----------
	session : Session
		Objeto que armazena e gerencia a sessão do usuário

    Methods
    -------
	request(action, content={})
		Método para simplificar a realização de requisições para o servidor
	register_client(name, cpf, password)
		Ação de cadastro do usuário
	login_client(cpf, password)
		Ação de login do usuário
	client_is_logged()
		Verifica se o usuário está autenticado
	logout_client()
		Ação de encerramento da sessão do usuário
	get_client()
		Ação de obter as informações do usuário
	get_client_history()
		Ação de obter histórico de transações do usuário
	withdraw(amount)
		Ação de saque bancário da conta do usuário
	deposit(amount)
		Ação de depósito bancário da conta do usuário
	transfer(amount, destination_acc_code)
		Ação de transferência bancária entre contas bancárias
	'''
	def __init__(self, server_port, server_host='localhost'):
		'''
		Parameters
        ----------
		server_port : int
			Porta em que o servidor está sendo executado
		server_host : int
			Endereço em que o servidor está sendo executado (o padrão é `localhost`)
		'''
		self._server_host = server_host
		self._server_port = server_port
		self._session = Session(self)
		self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._client_socket.connect((self._server_host, self._server_port))

	@property
	def session(self):
		'''Objeto que armazena e gerencia a sessão do usuário.
		
		Returns
        -------
		Session
			Sessão do usuário.
		'''
		return self._session

	def request(self, action, content={}):
		'''Método para simplificar a realização de requisições para o servidor.

		Parameters
        ----------
		action : str
			Ação que será solicitada para o servidor
		content : dict
			Dados que serão enviados para executar a ação

		Returns
        -------
		Any
			Dados da resposta da requisição que obteve sucesso.
		None
			Caso haja algum erro na requisição.
		'''
		content.update({'action': action, 'token': self._session.token})

		try:
			self._client_socket.send(json.dumps(content).encode())

			response = self._client_socket.recv(1024 * 256).decode()
			data = json.loads(response)
			
			if data and 'error' in data and data['error']:
				return None
			return data
		except (Exception, socket.error) as error:
			print(error)
			return None
		finally:
			pass
	
	def register_client(self, name, cpf, password):
		'''Ação de cadastro do usuário.

		Parameters
        ----------
		name : str
			Nome do usuário
		cpf : str
			CPF do usuário
		password : str
			Senha de acesso do usuário

		Returns
        -------
		bool
			Indicando se o cadastro foi realizado com sucesso.
		'''
		content = {'name': name, 'cpf': cpf, 'password': password}
		data = self.request('register_client', content)

		if not data or not 'token' in data:
			return False

		self._session.login(data['token'])
		return True

	def login_client(self, cpf, password):
		'''Ação de login do usuário.

		Parameters
        ----------
		cpf : str
			CPF do usuário
		password : str
			Senha de acesso do usuário

		Returns
        -------
		bool
			Indicando se o login foi realizado com sucesso.
		'''
		content = {'cpf': cpf, 'password': password}
		data = self.request('login_client', content)

		if not data or not 'token' in data:
			return False

		self._session.login(data['token'])
		return True
	
	def client_is_logged(self):
		'''Verifica se o usuário está autenticado.

		Returns
        -------
		bool
			Indicando se o usuário está autenticado.
		'''
		data = self.request('client_is_logged')

		if not data or not 'is_logged' in data:
			return False
		return data['is_logged']

	def logout_client(self):
		'''Ação de encerramento da sessão do usuário.
		'''
		return self.request('logout_client')
	
	def get_client(self):
		'''Ação de obter as informações do usuário.

		Returns
        -------
		dict
			Informações do usuário.
		'''
		return self.request('get_client')
	
	def get_client_history(self):
		'''Ação de obter histórico de transações do usuário.

		Returns
        -------
		list
			Histórico de transações do usuário.
		'''
		data = self.request('get_client_history')

		if not data or not 'history' in data:
			return []
		return data['history']

	def withdraw(self, amount):
		'''Ação de saque bancário da conta do usuário.

		Parameters
        ----------
		amount : float
			Quantia a ser sacada

		Returns
        -------
		bool
			Indicando se a operação foi realizada com sucesso.
		'''
		data = self.request('withdraw', {'amount': amount})
		return True if data else False

	def deposit(self, amount):
		'''Ação de depósito bancário da conta do usuário.

		Parameters
        ----------
		amount : float
			Quantia a ser depositada

		Returns
        -------
		bool
			Indicando se a operação foi realizada com sucesso.
		'''
		data = self.request('deposit', {'amount': amount})
		return True if data else False

	def transfer(self, amount, destination_acc_code):
		'''Ação de transferência bancária entre contas bancárias.

		Parameters
        ----------
		amount : float
			Quantia a ser transferida
		destination_acc_code : int
			Número da conta de destino

		Returns
        -------
		bool
			Indicando se a operação foi realizada com sucesso.
		'''
		data = self.request('transfer', {'amount': amount, 'destination_acc_code': destination_acc_code})
		return True if data else False
