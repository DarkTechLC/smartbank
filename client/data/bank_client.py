import socket
import json

from .session import Session


class BankClient:
	def __init__(self, server_port, server_host='localhost'):
		self._server_host = server_host
		self._server_port = server_port
		self._session = Session(self)
		self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._client_socket.connect((self._server_host, self._server_port))

	@property
	def session(self):
		return self._session

	def request(self, action, content={}):
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
		content = {'name': name, 'cpf': cpf, 'password': password}
		data = self.request('register_client', content)

		if not data or not 'token' in data:
			return False

		self._session.login(data['token'])
		return True

	def login_client(self, cpf, password):
		content = {'cpf': cpf, 'password': password}
		data = self.request('login_client', content)

		if not data or not 'token' in data:
			return False

		self._session.login(data['token'])
		return True
	
	def client_is_logged(self):
		data = self.request('client_is_logged')

		if not data or not 'is_logged' in data:
			return False
		return data['is_logged']

	def logout_client(self):
		return self.request('logout_client')
	
	def get_client(self):
		return self.request('get_client')
	
	def get_client_history(self):
		data = self.request('get_client_history')

		if not data or not 'history' in data:
			return []
		return data['history']

	def withdraw(self, amount):
		data = self.request('withdraw', {'amount': amount})
		return True if data else False

	def deposit(self, amount):
		data = self.request('deposit', {'amount': amount})
		return True if data else False

	def transfer(self, amount, destination_acc_code):
		data = self.request('transfer', {'amount': amount, 'destination_acc_code': destination_acc_code})
		return True if data else False
