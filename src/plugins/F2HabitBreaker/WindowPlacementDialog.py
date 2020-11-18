from PyQt5.QtWidgets import QDialog, QSizePolicy, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
X = Y = 0

class WindowPlacementDialog(QDialog):
    def __init__(self, parent):
        super(WindowPlacementDialog, self).__init__()
        self.p = parent
        self.leftClick = False
        
        self.tmp =  {
            'name': '',
            'size': {
                'height': 0,
                'width': 0
            },
            'pos': {
                'x': 0,
                'y': 0
            },
            'color': "#000000",
            'opacity': 0.5
        }

        self.setWindowTitle("Add Overlay")
        self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))
        self.resize(100, 100)

        col1 = QVBoxLayout()
        col1.setAlignment(Qt.AlignTop)
        col1.setContentsMargins(0,0,0,0);
        
        b1 = QPushButton("Save")
        b1.clicked.connect(self.recordPosition)
        col1.addWidget(b1)
        
        b2 = QPushButton("Cancel")
        b2.clicked.connect(self.cancel)
        col1.addWidget(b2)

        self.setLayout(col1)

        self.setStyleSheet("\
            QDialog { \
                background-color: #FFF; \
                border: 2px solid #000; \
            }\
            QPushButton { \
                padding: 0px; \
            }\
        ")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setSizeGripEnabled(True)
        self.exec()

    def recordPosition(self):
        self.tmp['size'] = { "height": self.size().height(), "width": self.size().width()}
        self.tmp['pos'] = { "x": self.pos().x(), "y": self.pos().y() }
        self.p.recordPosition(self.tmp)
        self.close()

    def cancel(self):
        self.close()

    def mouseMoveEvent(self, event):
        super(WindowPlacementDialog, self).mouseMoveEvent(event)
        if self.leftClick == True: 
            self.move(event.globalPos().x()-X,event.globalPos().y()-Y) # -8, -30

    def mousePressEvent(self, event):
        super(WindowPlacementDialog, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.leftClick = True
            global X,Y
            X=event.pos().x()
            Y=event.pos().y()

    def mouseReleaseEvent(self, event):
        super(WindowPlacementDialog, self).mouseReleaseEvent(event)
        self.leftClick = False