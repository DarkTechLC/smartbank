from data.models import Client, Account, History


class Bank:
    def __init__(self):
        self._migrate()
    
    def _migrate(self):
        Client.migrate()
        Account.migrate()
        History.migrate()

    def register_client(self, name, cpf, password):
        client = Client(name, cpf, password)

        if not client.save():
            return False
        
        account = Account(client.id)

        if not account.save():
            return False

        log = History('ABERTURA DA CONTA', f'Saldo inicial: {Account.format_money(account.balance)}', account.id)
        return log.save()
    
    # def delete_client(self, client_id):
    #     pass
    
    def get_client(self, client_id):
        return Client.get(client_id)
    
    def get_client_account(self, client_id):
        return Account.get(client_id)
    
    def get_client_history(self, client_id):
        return Account.get(client_id).history

    def withdraw(self, amount, account_code):
        account = Account.get(account_code)

        if (not account) or (account and not account.withdraw(amount)):
            return False
        
        log = History('SAQUE', f'Quantia: {Account.format_money(amount)}', account.id)
        return log.save()

    def deposit(self, amount, account_code):
        account = Account.get(account_code)

        if (not account) or (account and not account.deposit(amount)):
            return False
        
        log = History('DEPÓSITO', f'Quantia: {Account.format_money(amount)}', account.id)
        return log.save()

    def transfer(self, amount, origin_acc_code, destination_acc_code):
        origin_account = Account.get(origin_acc_code)
        destination_account = Account.get(destination_acc_code)
        
        if not origin_account or not destination_account:
            return False
        
        if not origin_account.transfer(destination_account, amount):
            return False
        
        origin_log = History('TRANSFERÊNCIA ENVIADA', f'Quantia: {Account.format_money(amount)}, N° conta destino: {destination_account.code}', origin_account.id)
        destination_log = History('TRANSFERÊNCIA RECEBIDA', f'Quantia: {Account.format_money(amount)}, N° conta origem: {origin_account.code}', destination_account.id)
        return origin_log.save() and destination_log.save()
