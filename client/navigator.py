from PyQt5.QtWidgets import QMainWindow, QStackedLayout

from windows import *
from data import bank


class Navigator(QMainWindow):
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
		window_controller = window_controller_constructor(self)
		self._window_controllers.append(window_controller)
		self._nav_stack.addWidget(window_controller.window)

	def go_to_window(self, window_id, private=False):
		if len(self._window_controllers) <= 0 or 0 > window_id >= len(self._window_controllers):
			return

		if private and not bank.session.has_session:
			self.go_to_login_window()
			return
		
		self._last_window_id = self._nav_stack.currentIndex()
		self._window_controllers[window_id].load_initial_state()
		self._nav_stack.setCurrentIndex(window_id)

	def go_back(self):
		self.go_to_window(self._last_window_id)

	def go_to_login_window(self):
		self.go_to_window(0)

	def go_to_register_window(self):
		self.go_to_window(1)

	def go_to_home_window(self):
		self.go_to_window(2, True)

	def go_to_withdraw_window(self):
		self.go_to_window(3, True)

	def go_to_deposit_window(self):
		self.go_to_window(4, True)

	def go_to_transfer_window(self):
		self.go_to_window(5, True)
