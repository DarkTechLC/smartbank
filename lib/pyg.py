import psycopg2
import sys


class Pyg:
	'''
		Pyg: Simple Postgres Python ORM
	'''
	def __init__(self, database, port, user, password, host='localhost'):
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
		try:
			self._cursor.close()
			self._db.close()
			return True
		except:
			return False
		
	def run_query(self, sql, params=[]):
		try:
			self._cursor.execute(sql, params)
			return self._cursor.fetchall()
		except Exception as error:
			print(error)
			return None
		finally:
			self._db.commit()

	def create_table(self, table_name, sql):
		self.run_query(f'''CREATE TABLE IF NOT EXISTS {table_name} (
			{sql}
		);''')

	def insert(self, table_name, data={}):
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
		result = self.run_query(f'''SELECT {attr}
			FROM {table_name}
			{query and f'WHERE {query}'}
			{sql}
			{limit and f'LIMIT {limit}'}
		;''', params)
		
		return result[0] if bool(result) and limit == 1 else result

	def update(self, table_name, query, data={}, params=[]):
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
