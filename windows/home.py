from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidgetItem

from data import bank, session_manager


class HomeWindow:
	def __init__(self, navigator):
		self._window = uic.loadUi('ui/home.ui')
		self._navigator = navigator

		self._account_code_label = self._window.account_code_label
		self._welcome_label = self._window.welcome_label
		self._balance_value_label = self._window.balance_value_label

		self._logout_btn = self._window.logout_btn
		self._withdraw_btn = self._window.withdraw_btn
		self._deposit_btn = self._window.deposit_btn
		self._transfer_btn = self._window.transfer_btn

		self._update_history_btn = self._window.update_history_btn
		self._history_table = self._window.history_table

		self._load_events()
	
	@property
	def window(self):
		return self._window
	
	def load_initial_state(self):
		account = bank.get_client_account(session_manager.current_client_id)

		self._account_code_label.setText(f'Conta: {account.code}')
		self._welcome_label.setText(f'Olá, {session_manager.client.name}!')
		self._balance_value_label.setText(account.balance_fmt)
		self._load_history_table()

	def _load_events(self):
		self._withdraw_btn.clicked.connect(self._navigator.go_to_withdraw_window)
		self._deposit_btn.clicked.connect(self._navigator.go_to_deposit_window)
		self._transfer_btn.clicked.connect(self._navigator.go_to_transfer_window)
		self._update_history_btn.clicked.connect(lambda: self._load_history_table())
		self._logout_btn.clicked.connect(lambda: self._logout())

	def _load_history_table(self):
		self._clear_history_table()
		history = bank.get_client_history(session_manager.current_client_id)

		for log in reversed(history):
			row_position = self._history_table.rowCount()
			self._history_table.insertRow(row_position)
			self._history_table.setItem(row_position, 0, QTableWidgetItem(log.type))
			self._history_table.setItem(row_position, 1, QTableWidgetItem(log.timestamp.strftime('%d/%m/%Y %H:%M:%S')))
			self._history_table.setItem(row_position, 2, QTableWidgetItem(log.message))
		
		self._history_table.resizeColumnsToContents()
		self._history_table.resizeRowsToContents()
	
	def _clear_history_table(self):
		self._history_table.setRowCount(0)

	def _logout(self):
		session_manager.logout()
		self._navigator.go_to_login_window()

	def close(self):
		self._window.close()
	