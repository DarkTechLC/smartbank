from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox

from data import bank_db, session_manager


class DepositWindow:
	def __init__(self, navigator):
		self._window = uic.loadUi('ui/deposit.ui')
		self._navigator = navigator

		self._amount_value_input = self._window.amount_value_input

		self._back_btn = self._window.back_btn
		self._confirm_btn = self._window.confirm_btn

		self._load_events()
	
	@property
	def window(self):
		return self._window

	def load_initial_state(self):
		pass

	def _load_events(self):
		self._back_btn.clicked.connect(self._navigator.go_back)
		self._confirm_btn.clicked.connect(lambda: self._deposit())

	def _deposit(self):
		amount = self._amount_value_input.text()

		if not amount:
			QMessageBox.warning(self._window, 'Erro ao depositar', 'Informe o valor do depósito!')
			return

		account = bank_db.get_client_account(session_manager.client.cpf)

		if not bank_db.deposit(amount, account.code):
			QMessageBox.warning(self._window, 'Erro ao depositar', 'O valor do depósito não pode ser menor ou igual a zero!')
			return

		self._clear_form()
		QMessageBox.information(self._window, 'Depósito concluído', 'A quantia foi depositada com sucesso!')
		self._navigator.go_to_home_window()

	def _clear_form(self):
		self._amount_value_input.setText('')

	def close(self):
		self._window.close()
	