import bcrypt


class Crypt:
    '''Classe para simplificar o manipulação de hashs.

    Classe que contêm métodos estáticos para criação e comparação de hashs. Muito
    útil para, por exemplo, criar hash de senhas antes de salvar no banco de
    dados.

    Methods
    -------
    hash(raw_value)
        Gera o hash de uma string
    compare(raw_value, hashed_value)
        Compara uma string com um hash para verificar se a string passada foi
        originalmente usada para gerar o hash.
    '''
    _salt = bcrypt.gensalt()

    @staticmethod
    def hash(raw_value):
        '''Gera o hash de uma string.

        Parameters
        ----------
        raw_value : str
            Uma string qualquer
        
        Returns
        -------
        str
            O hash gerado a partir da string passada
        '''
        return bcrypt.hashpw(raw_value.encode('utf-8'), Crypt._salt).decode('utf-8')
    
    @staticmethod
    def compare(raw_value, hashed_value):
        '''Compara uma string com um hash.
        
        Verifica se a string passada foi originalmente usada para gerar o hash.

        Parameters
        ----------
        raw_value : str
            Uma string qualquer
        hashed_value : str
            O hash que será comparado com a string
        
        Returns
        -------
        bool
            Um booleano indicando se a string foi originalmente usada para gerar
            o hash informado.
        '''
        return bcrypt.checkpw(raw_value.encode('utf-8'), hashed_value.encode('utf-8'))
    