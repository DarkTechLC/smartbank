from PyQt5.QtWidgets import QMainWindow, QStackedLayout

from windows import *
from data import bank


class Navigator(QMainWindow):
	'''Classe que implementa toda a lógica de navegação entre as telas da
	aplicação.

	Methods
    -------
	add_window(window_controller_constructor)
		Adiciona uma nova janela na pilha de navegação
	go_to_window(window_id, private=False)
		Navega para uma janela uma determinada janela com base no ID
	go_back()
		Navega para a janela anterior
	go_to_login_window()
		Navega para a janela de login
	go_to_register_window()
		Navega para a janela de cadastro
	go_to_home_window()
		Navega para a janela principal
	go_to_withdraw_window()
		Navega para a janela de saque
	go_to_deposit_window()
		Navega para a janela de depósito
	go_to_transfer_window()
		Navega para a janela de transferência
	'''
	def __init__(self):
		super(Navigator, self).__init__()
		self.setObjectName('navigator')
		self._nav_stack = QStackedLayout()
		self._window_controllers = []
		self._last_window_id = self._nav_stack.currentIndex()

		self.add_window(LoginWindow)
		self.add_window(RegisterWindow)
		self.add_window(HomeWindow)
		self.add_window(WithdrawWindow)
		self.add_window(DepositWindow)
		self.add_window(TransferWindow)

	def add_window(self, window_controller_constructor):
		'''Adiciona uma nova janela na pilha de navegação.

		Parameters
        ----------
		window_controller_constructor : Window
			Classe construtora da janela
		'''
		window_controller = window_controller_constructor(self)
		self._window_controllers.append(window_controller)
		self._nav_stack.addWidget(window_controller.window)

	def go_to_window(self, window_id, private=False):
		'''Navega para uma janela uma determinada janela com base no ID.

		Caso a janela seja privada, o usuário deve estar autenticado, caso
		contrário será direcionado para a página de login.

		Parameters
        ----------
		window_id : int
			ID da janela que se deseja navegar
		private : bool
			Indica se a janela é privada ou não.
		'''
		if len(self._window_controllers) <= 0 or 0 > window_id >= len(self._window_controllers):
			return

		if private and not bank.session.has_session:
			self.go_to_login_window()
			return
		
		self._last_window_id = self._nav_stack.currentIndex()
		self._window_controllers[window_id].load_initial_state()
		self._nav_stack.setCurrentIndex(window_id)

	def go_back(self):
		'''Navega para a janela anterior.
		'''
		self.go_to_window(self._last_window_id)

	def go_to_login_window(self):
		'''Navega para a janela de login.
		'''
		self.go_to_window(0)

	def go_to_register_window(self):
		'''Navega para a janela de cadastro.
		'''
		self.go_to_window(1)

	def go_to_home_window(self):
		'''Navega para a janela principal.
		'''
		self.go_to_window(2, True)

	def go_to_withdraw_window(self):
		'''Navega para a janela de saque.
		'''
		self.go_to_window(3, True)

	def go_to_deposit_window(self):
		'''Navega para a janela de depósito.
		'''
		self.go_to_window(4, True)

	def go_to_transfer_window(self):
		'''Navega para a janela de transferência.
		'''
		self.go_to_window(5, True)
