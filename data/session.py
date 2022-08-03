class Session:
	__slots__ = [
		'_bank_db',
		'_current_client_id',
	]

	def __init__(self, bank_db):
		self._bank_db = bank_db
		self._current_client_id = None

	@property
	def client(self):
		if not self.has_session:
			return None
		return self._bank_db.clients[self._current_client_id]

	@property
	def current_client_id(self):
		return self._current_client_id

	@property
	def has_session(self):
		return bool(self._current_client_id)

	def login(self, client_id, password):
		if not client_id in self._bank_db.clients:
			return False

		client = self._bank_db.clients[client_id]

		if not password == client.password:
			return False

		self._current_client_id = client_id
		return True

	def logout(self):
		self._current_client_id = None
		return True
