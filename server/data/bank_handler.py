from threading import Lock

from data.models import Client, Account, History


class Bank:
    '''Classe responsável por executar todas as operações bancárias no banco
    de dados.

    Methods
    -------
    register_client(name, cpf, password)
        Realiza o cadastro e criação de conta de um usuário
    get_client(client_id):
        Obtém as informações de um usuário
    get_client_account(client_id):
        Obtém as informações da conta de um usuário
    get_client_history(client_id):
        Obtém as informações do histórico de transações de um usuário
    withdraw(amount, account_code):
        Realiza a operação de saque em uma conta
    deposit(amount, account_code):
        Realiza a operação de depósito em uma conta
    transfer(amount, origin_acc_code, destination_acc_code):
        Realiza a operação de transferência entre conta contas
    '''
    _locker = Lock()

    def __init__(self):
        self._migrate()
    
    def _migrate(self):
        '''Realiza a migração de todas as tabelas no banco de dados.
        '''
        Client.migrate()
        Account.migrate()
        History.migrate()

    def register_client(self, name, cpf, password):
        '''Realiza o cadastro e criação de conta de um usuário.

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
        tuple
            Tupla com as informações do usuário criado.
        None
            Caso não seja possível realizar o cadastro.
        '''
        client = Client(name, cpf, password)

        if not client.save():
            return None
        
        account = Account(client.id)
        account.save()

        log = History('ABERTURA DA CONTA', f'Saldo inicial: {Account.format_money(account.balance)}', account.id)
        log.save()
        return client
    
    def delete_client(self, client_id):
        pass
    
    def get_client(self, client_id):
        '''Obtém as informações de um usuário.

        Parameters
        ----------
        client_id : int
            ID de um usuário

        Returns
        -------
        tuple
            Tupla com as informações do usuário buscado.
        None
            Caso não seja possível encontrar o usuário.
        '''
        return Client.get(client_id)
    
    def get_client_account(self, client_id):
        '''Obtém as informações da conta de um usuário.

        Parameters
        ----------
        client_id : int
            ID de um usuário

        Returns
        -------
        tuple
            Tupla com as informações da conta do usuário buscado.
        None
            Caso não seja possível encontrar o usuário e a conta.
        '''
        return Account.get(client_id)
    
    def get_client_history(self, client_id):
        '''Obtém as informações do histórico de transações de um usuário.

        Parameters
        ----------
        client_id : int
            ID de um usuário

        Returns
        -------
        lis[tuple]
            Lista de tuplas com o histórico de transações do usuário buscado.
        '''
        return Account.get(client_id).history

    def withdraw(self, amount, account_code):
        '''Realiza a operação de saque em uma conta.

        Parameters
        ----------
        amount : float
            Quantia a ser sacada
        account_code : int
            Número da conta de onde será realizado o saque

        Returns
        -------
        bool
            Booleano indicando se a operação foi concluída.
        '''
        Bank._lock()
        account = Account.get(account_code)

        if (not account) or (account and not account.withdraw(amount)):
            return False
        
        log = History('SAQUE', f'Quantia: {Account.format_money(amount)}', account.id)
        saved = log.save()
        Bank._unlock()
        return saved

    def deposit(self, amount, account_code):
        '''Realiza a operação de depósito em uma conta.

        Parameters
        ----------
        amount : float
            Quantia a ser depositada
        account_code : int
            Número da conta de onde será realizado o depósito

        Returns
        -------
        bool
            Booleano indicando se a operação foi concluída.
        '''
        Bank._lock()
        account = Account.get(account_code)

        if (not account) or (account and not account.deposit(amount)):
            return False
        
        log = History('DEPÓSITO', f'Quantia: {Account.format_money(amount)}', account.id)
        saved = log.save()
        Bank._unlock()
        return saved

    def transfer(self, amount, origin_acc_code, destination_acc_code):
        '''Realiza a operação de transferência entre contas.

        Parameters
        ----------
        amount : float
            Quantia a ser transferida
        account_code : int
            Número da conta de origem de onde será realizada a transferência
        destination_acc_code : int
            Número da conta de destino para onde será realizada a transferência

        Returns
        -------
        bool
            Booleano indicando se a operação foi concluída.
        '''
        Bank._lock()
        origin_account = Account.get(origin_acc_code)
        destination_account = Account.get(destination_acc_code)
        
        if not origin_account or not destination_account:
            return False
        
        if not origin_account.transfer(destination_account, amount):
            return False
        
        origin_log = History('TRANSFERÊNCIA ENVIADA', f'Quantia: {Account.format_money(amount)}, N° conta destino: {destination_account.code}', origin_account.id)
        destination_log = History('TRANSFERÊNCIA RECEBIDA', f'Quantia: {Account.format_money(amount)}, N° conta origem: {origin_account.code}', destination_account.id)
        saved = origin_log.save() and destination_log.save()
        Bank._unlock()
        return saved

    @staticmethod
    def _lock():
        Bank._locker.acquire()

    @staticmethod
    def _unlock():
        Bank._locker.release()
