import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLabel, QCheckBox
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QSize, QPoint
from support.Logger import Logger
from support.Config import Config


class LogDialog(QMainWindow):
	def __init__(self):
		super(LogDialog, self).__init__()
		self.setWindowTitle("Log")
		self.resize(800, 600)

		self.log = Logger()

		col1 = QVBoxLayout()
		
		self.logToFile = QCheckBox("Log to file")
		if Config().log_to_file:
			self.logToFile.setCheckState(2)
		self.logToFile.stateChanged.connect(self.logToFileChanged)
		col1.addWidget(self.logToFile)

		col1.addWidget(QLabel("Logs are stored in " + os.path.abspath(self.log.filename)))
		self.logDisplay = QTextEdit()
		self.logDisplay.setReadOnly(True)
		self.logDisplay.setText("\n".join(self.log.messages))
		col1.addWidget(self.logDisplay)
		
		widget = QWidget()
		widget.setLayout(col1)
		self.setCentralWidget(widget)

		self.log.attach(self, 'update')

		if Config().log_size != None:
			self.resize(QSize(Config().log_size['width'], Config().log_size['height']))
		if Config().log_pos != None:
			self.move(QPoint(Config().log_pos['x'], Config().log_pos['y']))

		self.show()

	def update(self, message):
		self.logDisplay.moveCursor(QTextCursor.End)
		self.logDisplay.insertPlainText("\n" + message)
		self.logDisplay.moveCursor(QTextCursor.End)

	def closeEvent(self, event):
		Config().log_size = { "height": self.size().height(), "width": self.size().width()}
		Config().log_pos = { "x": self.pos().x(), "y": self.pos().y() }
		Config().save()

	def logToFileChanged(self):
		cfg = Config()
		cfg.log_to_file = self.logToFile.isChecked()
		cfg.save()
		if cfg.log_to_file:
			self.log.dump()