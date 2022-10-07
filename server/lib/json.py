import json


class Json:
    '''Classe para simplificar o manipulação de JSON.

    Classe que contêm métodos estáticos para transformar tipos do Python em JSON
    e vice-versa, caso sejam válidos.

    Methods
    -------
    parse_from_json(content)
        Transforma um JSON em um tipo do Python, caso seja válido
    parse_to_json(content)
        Transforma um tipo do Python em um JSON, caso seja válido
    '''
    @staticmethod
    def parse_from_json(content):
        '''Transforma um JSON em uma lista ou dicionário do Python, caso seja
        válido.

        Parameters
        ----------
        content : str
            Um conteúdo em formato JSON
        
        Returns
        -------
        Union[dict, list]
            A lista ou dicionário do Python gerado a partir do JSON passado,
            caso seja possível deserializá-lo.
        None
            Caso não seja possível deserializar o conteúdo.
        '''
        try:
            return json.loads(content)
        except:
            return None

    @staticmethod
    def parse_to_json(content):
        '''Transforma uma lista ou dicionário do Python em um JSON, caso seja
        válido.

        Parameters
        ----------
        content : Union[dict, list]
            Um conteúdo em formato de lista ou dicionário do Python
        
        Returns
        -------
        str
            O JSON gerado a partir do conteúdo passado, caso seja possível
            serializá-lo.
        None
            Caso não seja possível serializar o conteúdo.
        '''
        try:
            return json.dumps(content)
        except:
            return None
    