from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox

from data import session_manager


class LoginWindow:
	def __init__(self, navigator):
		self._window = uic.loadUi('ui/login.ui')
		self._navigator = navigator

		self._cpf_input = self._window.cpf_input
		self._password_input = self._window.password_input

		self._login_submit_btn = self._window.login_submit_btn
		self._register_link_btn = self._window.register_link_btn

		self._load_events()
	
	@property
	def window(self):
		return self._window

	def load_initial_state(self):
		pass

	def _load_events(self):
		self._login_submit_btn.clicked.connect(lambda: self._login())
		self._register_link_btn.clicked.connect(self._navigator.go_to_register_window)

	def _login(self):
		cpf = self._cpf_input.text()
		password = self._password_input.text()

		if not cpf or not password:
			QMessageBox.warning(self._window, 'Erro ao entrar', 'Preencha todos os campos para entrar!')
			return

		if not session_manager.login(cpf, password):
			QMessageBox.warning(self._window, 'Erro ao cadastrar', 'Credenciais inválidas: CPF e/ou senha incorretos!')
			return
		
		self._clear_form()
		self._navigator.go_to_home_window()

	def _clear_form(self):
		self._cpf_input.setText('')
		self._password_input.setText('')

	def close(self):
		self._window.close()
	