import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from fluxgateDAQ import fluxgateLJ

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Magnetic Field Measurements")

        button = QPushButton("Measure")
        button.clicked.connect(self.measure)

        self.x = QLabel()
        self.x.setAlignment(Qt.AlignCenter)
        self.x.setFont(QFont("Arial", 18))
        self.x.setText("X: 0.00")

        self.y = QLabel()
        self.y.setAlignment(Qt.AlignCenter)
        self.y.setFont(QFont("Arial", 18))
        self.y.setText("Y: 0.00")

        self.z = QLabel()
        self.z.setAlignment(Qt.AlignCenter)
        self.z.setFont(QFont("Arial", 18))
        self.z.setText("Z: 0.00")

        displayLayout = QHBoxLayout()
        displayLayout.addWidget(self.x)
        displayLayout.addWidget(self.y)
        displayLayout.addWidget(self.z)
        display = QWidget()
        display.setLayout(displayLayout)

        layout = QVBoxLayout()
        layout.addWidget(display)
        layout.addWidget(button)

        widget = QWidget()
        widget.setLayout(layout)

        self.setFixedSize(QSize(600, 400))

        self.setCentralWidget(widget)

        self.fg = fluxgateLJ("fluxgate", csv_log=True)
        self.fg.setup(x=0,y=1,z=2)


    def spacebarPressed(self, event):
        if isinstance(event, QKeyEvent):
            self.measure

    def measure(self):
        dat = self.fg.read_single()

        self.x.setText(f"X: {dat[0]:.2f}")
        self.y.setText(f"Y: {dat[1]:.2f}")
        self.z.setText(f"Z: {dat[2]:.2f}")


app = QApplication(sys.argv)

window = MainWindow()
window.show()
sys.exit(app.exec_())