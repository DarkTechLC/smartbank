from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox

from data import bank


class LoginWindow:
	'''Janela de login do usuário.

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
		self._window = uic.loadUi('ui/login.ui')
		self._navigator = navigator

		self._cpf_input = self._window.cpf_input
		self._password_input = self._window.password_input

		self._login_submit_btn = self._window.login_submit_btn
		self._register_link_btn = self._window.register_link_btn

		self._load_events()
	
	@property
	def window(self):
		'''Elemento da janela atual.

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
		self._login_submit_btn.clicked.connect(lambda: self._login())
		self._register_link_btn.clicked.connect(self._navigator.go_to_register_window)

	def _login(self):
		'''Define a ação de login com as devidas validações.
		'''
		cpf = self._cpf_input.text()
		password = self._password_input.text()

		if not cpf or not password:
			QMessageBox.warning(self._window, 'Erro ao entrar', 'Preencha todos os campos para entrar!')
			return

		if not bank.login_client(cpf, password):
			QMessageBox.warning(self._window, 'Erro ao cadastrar', 'Credenciais inválidas: CPF e/ou senha incorretos!')
			return
		
		self._clear_form()
		self._navigator.go_to_home_window()

	def _clear_form(self):
		'''Limpa o formulário.
		'''
		self._cpf_input.setText('')
		self._password_input.setText('')

	def close(self):
		'''Fecha a janela atual.
		'''
		self._window.close()
	