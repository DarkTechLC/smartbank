from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox

from data import bank


class WithdrawWindow:
	'''Janela de saque bancário.

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
		self._window = uic.loadUi('ui/withdraw.ui')
		self._navigator = navigator

		self._amount_value_input = self._window.amount_value_input

		self._back_btn = self._window.back_btn
		self._confirm_btn = self._window.confirm_btn

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
		self._back_btn.clicked.connect(self._navigator.go_back)
		self._confirm_btn.clicked.connect(lambda: self._withdraw())

	def _withdraw(self):
		'''Define a ação de saque com as devidas validações.
		'''
		amount = self._amount_value_input.text()

		if not amount:
			QMessageBox.warning(self._window, 'Erro ao sacar', 'Informe o valor do saque!')
			return

		if not bank.withdraw(amount):
			QMessageBox.warning(self._window, 'Erro ao sacar', 'Saldo insuficiente, ou o valor informado foi menor ou igual a zero!')
			return

		self._clear_form()
		QMessageBox.information(self._window, 'Saque concluído', 'A quantia foi sacada com sucesso!')
		self._navigator.go_to_home_window()

	def _clear_form(self):
		'''Limpa o formulário.
		'''
		self._amount_value_input.setText('')

	def close(self):
		'''Fecha a janela atual.
		'''
		self._window.close()
	