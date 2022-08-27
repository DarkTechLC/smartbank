from lib.server import Server
from lib.json import Json
from data import bank, session_manager


class AppController:
    def __init__(self, request, response):
        self._request = request
        self._response = response
        self._data = Json.parse_from_json(self._request)
        self._router = {
            'register_client': {
                'is_private': False,
                'handler': self._register_client,
            },
            'client_is_logged': {
                'is_private': False,
                'handler': self._client_is_logged,
            },
            'login_client': {
                'is_private': False,
                'handler': self._login_client,
            },
            'logout_client': {
                'is_private': True,
                'handler': self._logout_client,
            },
            'get_client': {
                'is_private': True,
                'handler': self._get_client,
            },
            'get_client_history': {
                'is_private': True,
                'handler': self._get_client_history,
            },
            'withdraw': {
                'is_private': True,
                'handler': self._withdraw,
            },
            'deposit': {
                'is_private': True,
                'handler': self._deposit,
            },
            'transfer': {
                'is_private': True,
                'handler': self._transfer,
            },
        }

        self._middlewares()

    def _middlewares(self):
        if not self._data:
            return self.send({'error': True, 'message': 'Não foi possível ler a requisição.'})

        if not 'action' in self._data or not self._data['action'].lower() in self._router:
            return self.send({'error': True, 'message': 'Operação inválida.'})

        action = self._router[self._data['action'].lower()]

        if action['is_private']:
            token = self._data['token'] if 'token' in self._data else None

            if not token or not session_manager.check(token):
                return self.send({'error': True, 'message': 'Usuário não autenticado.'})

        return action['handler']()

    def send(self, content):
        return self._response(Json.parse_to_json(content) or '{"error": true, "message": "Erro no servidor."}')

    def _register_client(self):
        name = self._data['name']
        cpf = self._data['cpf']
        password = self._data['password']

        client = bank.register_client(name, cpf, password)

        if not client:
            return self.send({'error': True, 'message': 'Não foi possível realizar o cadastro.'})

        token = session_manager.add(client.id)
        return self.send({'error': False, 'message': 'Usuário cadastrado com sucesso.', 'token': token})

    def _client_is_logged(self):
        token = self._data['token'] if 'token' in self._data else None
        is_logged = token and session_manager.check(token)
        return self.send({'error': False, 'is_logged': is_logged})

    def _login_client(self):
        cpf = self._data['cpf']
        password = self._data['password']

        token = session_manager.login(cpf, password)

        if not token:
            return self.send({'error': True, 'message': 'Credenciais inválidas.'})

        return self.send({'error': False, 'message': 'Acesso liberado com sucesso.', 'token': token})

    def _logout_client(self):
        token = self._data['token']
        session_manager.logout(token)
        return self.send({'error': False, 'message': 'Sessão destruída com sucesso.'})

    def _get_client(self):
        token = self._data['token']
        client_id = session_manager.get_id_by_token(token)
        client = bank.get_client(client_id)

        if not client:
            return self.send({'error': True, 'message': 'Usuário não encontrado.'})

        account = bank.get_client_account(client.id)

        return self.send({
            'error': False,
            'id': client.id,
            'name': client.name,
            'cpf': client.cpf,
            'account': {
                'code': account.code,
                'balance': account.balance,
            },
        })

    def _get_client_history(self):
        token = self._data['token']
        client_id = session_manager.get_id_by_token(token)
        client = bank.get_client(client_id)

        if not client:
            return self.send({'error': True, 'message': 'Usuário não encontrado.'})

        history = bank.get_client_history(client.id)

        return self.send({
            'error': False,
            'history': list(map(lambda log: {
                'id': log.id,
                'type': log.type,
                'timestamp': str(log.timestamp),
                'message': log.message,
            }, history))
        })

    def _withdraw(self):
        token = self._data['token']
        amount = self._data['amount']
        
        client_id = session_manager.get_id_by_token(token)
        account = bank.get_client_account(client_id)

        if not account:
            return self.send({'error': True, 'message': 'Conta não encontrada.'})

        if not bank.withdraw(amount, account.id):
            return self.send({'error': True, 'message': 'Não foi possível sacar a quantia.'})
        return self.send({'error': False, 'message': 'Saque realizado.'})

    def _deposit(self):
        token = self._data['token']
        amount = self._data['amount']
        
        client_id = session_manager.get_id_by_token(token)
        account = bank.get_client_account(client_id)

        if not account:
            return self.send({'error': True, 'message': 'Conta não encontrada.'})

        if not bank.deposit(amount, account.id):
            return self.send({'error': True, 'message': 'Não foi possível depositar a quantia.'})
        return self.send({'error': False, 'message': 'Depósito realizado.'})

    def _transfer(self):
        token = self._data['token']
        amount = self._data['amount']
        destination_acc_code = self._data['destination_acc_code']

        client_id = session_manager.get_id_by_token(token)
        origin_account = bank.get_client_account(client_id)

        if not bank.transfer(amount, origin_account.id, destination_acc_code):
            return self.send({'error': True, 'message': 'Não foi possível transferir a quantia.'})
        return self.send({'error': False, 'message': 'Transferência realizada.'})


app = Server(AppController)
