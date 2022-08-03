class Client:
    __slots__ = [
        '_name',
        '_cpf',
        '_password',
    ]

    def __init__(self, name, cpf, password):
        self._name = name
        self._cpf = cpf
        self._password = password

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password
