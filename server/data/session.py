import random, string

from lib.crypt import Crypt
from .bank_handler import Bank


class Session:
	__slots__ = [
		'_db',
		'_session_tokens',
	]

	def __init__(self, db: Bank):
		self._db = db
		self._session_tokens = {}

	def get_id_by_token(self, token):
		if self.check(token):
			return self._session_tokens[token]
		return None

	def check(self, token):
		return token in self._session_tokens

	def login(self, cpf, password):
		client = self._db.get_client(cpf)

		if not client:
			return None

		if not Crypt.compare(password, client.password):
			return None
		return self.add(client.id)

	def add(self, client_id):
		token = f'{self._generate_token()}_{client_id}'
		self._session_tokens[token] = client_id
		return token

	def logout(self, token):
		if self.check(token):
			del self._session_tokens[token]

	def _generate_token(self, size=10):
		letters = string.ascii_lowercase
		return ''.join(random.choice(letters) for i in range(size))
