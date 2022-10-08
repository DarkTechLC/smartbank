from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox

from data import bank


class RegisterWindow:
	'''Janela de cadastro do usuário.

	Attributes
    ----------
	window : QMainWindow
		Elemento da janela atual

    Methods
    -------
	load_initial_state()
		Carrega o estado inicial da aplicação
	close()
		Fecha a janela atual
	'''

	def __init__(self, navigator):
		'''
		Parameters
        ----------
		navigator : Navigator
			Controlador da navegação da aplicação
		'''
		self._window = uic.loadUi('ui/register.ui')
		self._navigator = navigator

		self._name_input = self._window.name_input
		self._cpf_input = self._window.cpf_input
		self._password_input = self._window.password_input

		self._register_submit_btn = self._window.register_submit_btn
		self._login_link_btn = self._window.login_link_btn

		self._load_events()
	
	@property
	def window(self):
		'''Elemento da janela atual

		Returns
        -------
		QMainWindow
			Instância da janela atual.
		'''
		return self._window

	def load_initial_state(self):
		'''Carrega o estado inicial da aplicação.
		'''
		pass

	def _load_events(self):
		'''Carrega os eventos da aplicação.
		'''
		self._register_submit_btn.clicked.connect(lambda: self._register())
		self._login_link_btn.clicked.connect(self._navigator.go_to_login_window)

	def _register(self):
		'''Define a ação de cadastro do usuário com as devidas validações.
		'''
		name = self._name_input.text()
		cpf = self._cpf_input.text()
		password = self._password_input.text()

		if not name or not cpf or not password:
			QMessageBox.warning(self._window, 'Erro ao cadastrar', 'Preencha todos os campos para cadastrar-se!')
			return

		if not bank.register_client(name, cpf, password):
			QMessageBox.warning(self._window, 'Erro ao cadastrar', 'Esse CPF já está cadastrado!')
			return

		self._clear_form()
		self._navigator.go_to_home_window()

	def _clear_form(self):
		'''Limpa o formulário.
		'''
		self._name_input.setText('')
		self._cpf_input.setText('')
		self._password_input.setText('')

	def close(self):
		'''Fecha a janela atual.
		'''
		self._window.close()
	