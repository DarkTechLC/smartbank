from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox

from data import bank, session_manager


class RegisterWindow:
	def __init__(self, navigator):
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
		return self._window

	def load_initial_state(self):
		pass

	def _load_events(self):
		self._register_submit_btn.clicked.connect(lambda: self._register())
		self._login_link_btn.clicked.connect(self._navigator.go_to_login_window)

	def _register(self):
		name = self._name_input.text()
		cpf = self._cpf_input.text()
		password = self._password_input.text()

		if not name or not cpf or not password:
			QMessageBox.warning(self._window, 'Erro ao cadastrar', 'Preencha todos os campos para cadastrar-se!')
			return

		if not bank.register_client(name, cpf, password):
			QMessageBox.warning(self._window, 'Erro ao cadastrar', 'Esse CPF já está cadastrado!')
			return

		session_manager.login(cpf, password)
		self._clear_form()
		self._navigator.go_to_home_window()

	def _clear_form(self):
		self._name_input.setText('')
		self._cpf_input.setText('')
		self._password_input.setText('')

	def close(self):
		self._window.close()
	