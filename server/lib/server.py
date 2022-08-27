import threading
import socket
import signal
import time


class StoppableThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.daemon = True
		self._stop_event = threading.Event() 

	def stop(self):
		if self.is_alive() == True:
			self._stop_event.set()
			self.join()


class Server(StoppableThread):
	def __init__(self, handler, host='', port=8001):
		StoppableThread.__init__(self)
		self._host = host
		self._port = port
		self._handler = handler
		self._client_threads = []

	def listen(self):
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
		for thread in self._client_threads:
			if thread.is_alive() == True:
				thread.stop()
		self._client_threads = []
	

class SocketHandler(StoppableThread):
	def __init__(self, client_socket, client_address, handler):
		StoppableThread.__init__(self)
		self._client_socket = client_socket
		self._client_address = client_address
		self._handler = handler

	def run(self):
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
	