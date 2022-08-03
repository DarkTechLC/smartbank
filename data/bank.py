from .account import Account


class Bank:
    def __init__(self):
        self._clients = {} # {<client_id>: <Client>}
        self._accounts = {} # {<account_id>: <Account>}
        self._clients_accounts = {} # {<client_id>: <account_id>}
    
    @property
    def clients(self):
        return self._clients

    def register_client(self, client):
        if client.cpf in self._clients:
            return False
        
        account_code = self._generate_account_id()
        self._clients[client.cpf] = client
        self._accounts[account_code] = Account(account_code, client)
        self._clients_accounts[client.cpf] = account_code
        return True
    
    # def delete_client(self, client_id):
    #     pass
    
    def get_client(self, client_id):
        return self._clients[client_id]
    
    def get_client_account(self, client_id):
        return self._accounts[self._clients_accounts[client_id]]

    def withdraw(self, amount, account_code):
        return self._accounts[account_code].withdraw(amount)

    def deposit(self, amount, account_code):
        return self._accounts[account_code].deposit(amount)

    def transfer(self, amount, origin_acc_code, destination_acc_code):
        if not origin_acc_code in self._accounts or not destination_acc_code in self._accounts:
            return False
        
        origin_account = self._accounts[origin_acc_code]
        destination_account = self._accounts[destination_acc_code]
        return origin_account.transfer(destination_account, amount)

    def _generate_account_id(self):
        return str(len(self._accounts) + 1000)
