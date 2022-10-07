import psycopg2
import sys


class Pyg:
	'''Pyg: Simple Postgres Python ORM

	ORM simples para realizar operações comuns no PostgreSQL.

    Methods
    -------
    close()
		Fecha a conexão com o banco de dados
	'''
	def __init__(self, database, port, user, password, host='localhost'):
		'''
        Parameters
        ----------
        database : str
			Nome do banco de dados
        port : int
			Número da porta onde o banco de dados está executando
        user : str
			Nome do usuário do banco de dados
        password : str
			Senha do usuário do banco de dados
        host : str
			Endereço da máquina onde o banco de dados está executando
        '''
		try:
			self._db = psycopg2.connect(
				host=host,
				port=port,
				database=database,
				user=user,
				password=password,
			)
			self._cursor = self._db.cursor()
		except Exception as error:
			sys.exit(error)

	@property
	def cursor(self):
		return self._cursor

	def close(self):
		'''Fecha a conexão com o banco de dados.

        Returns
        -------
        bool
            Booleano indicando se a conexão foi encerrada.
        '''
		try:
			self._cursor.close()
			self._db.close()
			return True
		except:
			return False
		
	def run_query(self, sql, params=[]):
		'''Executa uma operação no banco de dados.

        Parameters
        ----------
        sql : str
            Um SQL válido
		params : list
			Uma lista de valores que serão inserido no SQL informado
        
        Returns
        -------
        list
            Listagem dos resultados da operação executada.
        None
            Caso não seja possível executar a operação.
        '''
		try:
			self._cursor.execute(sql, params)
			return self._cursor.fetchall()
		except Exception as error:
			print(error)
			return None
		finally:
			self._db.commit()

	def create_table(self, table_name, sql):
		'''Cria uma tabela no bando de dados, caso ela não exista.

        Parameters
        ----------
		table_name: str
			O nome da tabela
        sql : str
            Um SQL válido com os nomes, tipos e referências das colunas da tabela
        '''
		self.run_query(f'''CREATE TABLE IF NOT EXISTS {table_name} (
			{sql}
		);''')

	def insert(self, table_name, data={}):
		'''Executa uma operação de inserção no banco de dados.

        Parameters
        ----------
        table_name : str
            O nome da tabela onde será feita a inserção
		data : dict
			Um dicionário com os valores que serão inseridos na tabela, onde as
			chaves indicam os nomes das colunas.
        
        Returns
        -------
        bool
            Booleano indicando se a inserção foi realizada com sucesso.
        '''
		columns = list(data.keys())
		values = list(data.values())
		value_places = ','.join(('%s ' * len(columns)).split())

		result = self.run_query(f'''INSERT INTO {table_name}
			({','.join(columns)})
			VALUES ({value_places})
			RETURNING id
		;''', values)
		
		return result[0] if bool(result) else result

	def search(self, table_name, query='', attr='*', sql='', limit='', params=[]):
		'''Executa uma operação de busca no banco de dados.

        Parameters
        ----------
        table_name : str
            O nome da tabela onde será feita a busca
		query : Optional[str]
			SQL com as filtragens a serem aplicadas na busca
		attr : Optional[str]
			Colunas que devem ser retornadas na busca, caso não seja especificado,
			todas serão retornadas.
		sql : Optional[str]
			SQL adicional para ser aplicados na busca
		limit : Optional[int]
			Quantidade máxima de resultados retornados na busca
		params : list
			Uma lista de valores que serão inserido no SQL informado
        
        Returns
        -------
        tuple
			A linha da tabela que corresponde a busca
        list[tuple]
			Uma lista contendo as linhas da tabela que correspondem a busca
        '''
		result = self.run_query(f'''SELECT {attr}
			FROM {table_name}
			{query and f'WHERE {query}'}
			{sql}
			{limit and f'LIMIT {limit}'}
		;''', params)
		
		return result[0] if bool(result) and limit == 1 else result

	def update(self, table_name, query, data={}, params=[]):
		'''Executa uma operação de atualização no banco de dados.

        Parameters
        ----------
        table_name : str
            O nome da tabela onde será feita a atualização
		query : Optional[str]
			SQL com as filtragens a serem aplicadas na busca
		data : dict
			Um dicionário com os valores que serão atualizados na tabela, onde
			as chaves indicam os nomes das colunas.
		params : list
			Uma lista de valores que serão inserido no SQL informado
        
        Returns
        -------
        bool
            Booleano indicando se a atualização foi realizada com sucesso.
        '''
		columns = map(lambda column: f'{column}=%s', list(data.keys()))
		values = list(data.values())

		result = self.run_query(f'''UPDATE {table_name}
			SET {','.join(columns)}
			WHERE {query}
			RETURNING id
		;''', values + params)
		
		return result[0] if bool(result) else result

	def delete(self):
		pass
