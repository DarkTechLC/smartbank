import random
import socket
import json

HOST = 'localhost'
PORT = 8001

server_address = (HOST, PORT)

def test(data={}):
	try:		
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect(server_address)

		client_socket.send(json.dumps(data).encode())

		raw_data = client_socket.recv(1024).decode()
		data = json.loads(raw_data)
		print(data)
		print()
		return data
	except Exception as error:
		print(error)
		return None
	finally:
		client_socket.close()


if __name__ == '__main__':
	cpf = random.randint(10000000000, 99999999999)
	data = test({'action': 'register_client', 'name': 'Pedro', 'cpf': cpf, 'password': '123'})

	if data and 'token' in data:
		test({'action': 'get_client', 'token': data['token']})
		test({'action': 'deposit', 'token': data['token'], 'amount': 1000})
		test({'action': 'withdraw', 'token': data['token'], 'amount': 500})
		test({'action': 'transfer', 'token': data['token'], 'amount': 200, 'destination_acc_code': '0046'})
		test({'action': 'get_client_history', 'token': data['token']})
