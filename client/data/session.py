class Session:
	__slots__ = [
		'_client',
		'_session_token',
	]

	def __init__(self, client):
		self._client = client
		self._session_token = None

	@property
	def token(self):
		return self._session_token

	@property
	def has_session(self):
		return bool(self._session_token) and self._client.client_is_logged()

	def login(self, token):
		self._session_token = token
		return True

	def logout(self):
		self._session_token = None
		return True
