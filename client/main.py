from PyQt5.QtWidgets import QApplication

from navigator import Navigator


if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	navigator = Navigator()
	sys.exit(app.exec_())
