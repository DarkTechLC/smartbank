from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox

from data import bank_db, session_manager


class TransferWindow:
	def __init__(self, navigator):
		self._window = uic.loadUi('ui/transfer.ui')
		self._navigator = navigator

		self._amount_value_input = self._window.amount_value_input
		self._destination_account_code_input = self._window.destination_account_code_input

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
		self._confirm_btn.clicked.connect(lambda: self._transfer())

	def _transfer(self):
		amount = self._amount_value_input.text()
		destination_account_code = self._destination_account_code_input.text()

		if not amount:
			QMessageBox.warning(self._window, 'Erro ao transferir', 'Informe o valor da transferência!')
			return

		origin_account = bank_db.get_client_account(session_manager.client.cpf)

		if destination_account_code == origin_account.code:
			QMessageBox.warning(self._window, 'Erro ao transferir', 'Não é permitido transferir para sua conta!')
			return

		if not bank_db.transfer(amount, origin_account.code, destination_account_code):
			QMessageBox.warning(self._window, 'Erro ao transferir', 'Conta de destino inexistente, saldo insuficiente, ou o valor informado foi menor ou igual a zero!')
			return

		self._clear_form()
		QMessageBox.information(self._window, 'Transferência concluída', 'A quantia foi transferida com sucesso!')
		self._navigator.go_to_home_window()

	def _clear_form(self):
		self._amount_value_input.setText('')
		self._destination_account_code_input.setText('')

	def close(self):
		self._window.close()
	