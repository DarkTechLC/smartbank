import threading
import socket
import signal
import time


class StoppableThread(threading.Thread):
	'''Classe base para criação de threads que podem ser paradas.

    Methods
    -------
    stop()
		Finaliza a thread
	'''
	def __init__(self):
		threading.Thread.__init__(self)
		self.daemon = True
		self._stop_event = threading.Event() 

	def stop(self):
		'''Finaliza a thread caso ela esteja ativa.
		'''
		if self.is_alive() == True:
			self._stop_event.set()
			self.join()


class Server(StoppableThread):
	'''Classe para criação do servidor responsável por aceitar as conexões e
	gerenciá-las.

    Methods
    -------
	listen():
		Inicializa a thread do servidor para que seja possível aceitar
		as conexões dos clientes e processar as solicitações.
	run()
		Cria e configura o servidor para aceitar as conexões dos clientes e
		passar a execução delas para uma nova thread processar as requisições.
    stop_threads()
		Finaliza todas as threads referentes as conexões dos clientes
	'''
	def __init__(self, handler, host='', port=8001):
		'''
        Parameters
        ----------
        handler : AppController
			Classe controladora que processa as requisições do usuário
        host : str
			Endereço em que o servidor irá esperar conexões (por padrão receberá
			de todos).
        port : int
			Porta em que o servidor será executado (por padrão é a 8001)
        '''
		StoppableThread.__init__(self)
		self._host = host
		self._port = port
		self._handler = handler
		self._client_threads = []

	def listen(self):
		'''Inicializa a thread do servidor para que seja possível aceitar
		as conexões dos clientes e processar as solicitações.
		'''
		self.start()

		def handle_exit():
			self.stop()

		while True:
			try:
				time.sleep(0.1)
			except KeyboardInterrupt:
				break
		
		signal.signal(signal.SIGTERM, handle_exit)
		signal.signal(signal.SIGINT, handle_exit)
	
	def run(self):
		'''Cria e configura o servidor para aceitar as conexões dos clientes e
		passar a execução delas para uma nova thread processar as requisições.
		'''
		try:
			self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self._server_socket.bind((self._host, self._port))
			self._server_socket.listen()
			print(f'=> Server listening at port {self._port}...\n')
		except socket.error:
			interval = 10
			print(f'=> Address already in use. Retrying in {interval} seconds...\n')
			time.sleep(interval)
			self.run()
	
		while self._stop_event.is_set() == False:
			try:
				client_socket, client_address = self._server_socket.accept()
				print(f'=> Socket connected: {client_address[0]}:{client_address[1]}')
				
				client_thread = SocketHandler(client_socket, client_address, self._handler)
				self._client_threads.append(client_thread)
				client_thread.start()
			except socket.timeout:
				print('=> Socket connection timeout')

				for thread in self._client_threads:
					if thread.is_alive() == False:
						self._client_threads.remove(thread)
		self.stop_threads()
		self._server_socket.close()

	def stop_threads(self):
		'''Finaliza todas as threads referentes as conexões dos clientes.
		'''
		for thread in self._client_threads:
			if thread.is_alive() == True:
				thread.stop()
		self._client_threads = []
	

class SocketHandler(StoppableThread):
	'''Classe responsável por tratar as requisições do clientes e injetar os
	dados recebidos e a função de resposta para serem processadas pelo controlador.
	Cada instância gera uma nova thread no servidor.

	Methods
    -------
	run()
		Recebe as requisições do cliente, decodifica e injeta os dados
		recebidos e a função de resposta para serem processadas pelo controlador.
	'''
	def __init__(self, client_socket, client_address, handler):
		'''
        Parameters
        ----------
        client_socket : socket
			Socket que indica a conexão do cliente
        client_address : tuple
			Tupla contendo o endereço e a porta do socket cliente
        handler : AppController
			Classe controladora que processa as requisições do usuário
        '''
		StoppableThread.__init__(self)
		self._client_socket = client_socket
		self._client_address = client_address
		self._handler = handler

	def run(self):
		'''Recebe as requisições do cliente, decodifica e injeta os dados
		recebidos e a função de resposta para serem processadas pelo controlador.
		'''
		while self._stop_event.is_set() == False:     
			try:
				data = self._client_socket.recv(1024).decode()
				
				if len(data) > 0:
					response = lambda message: self._client_socket.send(message.encode())
					self._handler(data, response)
				else:
					self._stop_event.set()
			except:
				self._stop_event.set()
		self._client_socket.close()
	