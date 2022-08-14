from .bank_handler import Bank


class Session:
	__slots__ = [
		'_bank',
		'_current_client_id',
	]

	def __init__(self, bank: Bank):
		self._bank = bank
		self._current_client_id = None

	@property
	def client(self):
		if not self.has_session:
			return None
		return self._bank.get_client(self._current_client_id)

	@property
	def current_client_id(self):
		return self._current_client_id

	@property
	def has_session(self):
		return bool(self._current_client_id)

	def login(self, cpf, password):
		client = self._bank.get_client(cpf)

		if not client:
			return False

		if not (password == client.password):
			return False

		self._current_client_id = client.id
		return True

	def logout(self):
		self._current_client_id = None
		return True
