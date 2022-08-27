from datetime import datetime
from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidgetItem

from data import bank


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
		client = bank.get_client()
		balance = f"R$ {float(client['account']['balance']):.2f}".replace('.', ',')

		self._account_code_label.setText(f"Conta: {client['account']['code']}")
		self._welcome_label.setText(f"Olá, {client['name']}!")
		self._balance_value_label.setText(balance)
		self._load_history_table()

	def _load_events(self):
		self._withdraw_btn.clicked.connect(self._navigator.go_to_withdraw_window)
		self._deposit_btn.clicked.connect(self._navigator.go_to_deposit_window)
		self._transfer_btn.clicked.connect(self._navigator.go_to_transfer_window)
		self._update_history_btn.clicked.connect(lambda: self.load_initial_state())
		self._logout_btn.clicked.connect(lambda: self._logout())

	def _load_history_table(self):
		self._clear_history_table()
		history = bank.get_client_history()

		for log in reversed(history):
			date_time = datetime.fromisoformat(log['timestamp']).strftime('%d/%m/%Y %H:%M:%S')
			row_position = self._history_table.rowCount()

			self._history_table.insertRow(row_position)
			self._history_table.setItem(row_position, 0, QTableWidgetItem(log['type']))
			self._history_table.setItem(row_position, 1, QTableWidgetItem(date_time))
			self._history_table.setItem(row_position, 2, QTableWidgetItem(log['message']))
		
		self._history_table.resizeColumnsToContents()
		self._history_table.resizeRowsToContents()
	
	def _clear_history_table(self):
		self._history_table.setRowCount(0)

	def _logout(self):
		bank.logout_client()
		self._navigator.go_to_login_window()

	def close(self):
		self._window.close()
	