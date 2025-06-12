"""
UI to interface with the fluxgateLJ class to take measurements of the magnetic field
Rylan Stutters
June 2025

Requires install of the following:
    PyQt5 python package
"""

import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from fluxgateDAQ import fluxgateLJ

class MainWindow(QMainWindow):
    """Magnetic field measurement UI main window

    Attributes:
        x (QLabel): B_x readout
        y (QLabel): B_y readout
        z (QLabel): B_z readout
        fg (fluxgateLJ): fluxgate being read
    """
    def __init__(self):
        """Initialize window

        """
        super().__init__()

        self.setWindowTitle("Magnetic Field Measurements")

        # button to take input to measure
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

        # horizontal layout of the magnetic field readouts
        displayLayout = QHBoxLayout()
        displayLayout.addWidget(self.x)
        displayLayout.addWidget(self.y)
        displayLayout.addWidget(self.z)
        display = QWidget()
        display.setLayout(displayLayout)

        # vertical layout with readouts above measure button
        layout = QVBoxLayout()
        layout.addWidget(display)
        layout.addWidget(button)

        # assign full layout to central widget
        widget = QWidget()
        widget.setLayout(layout)

        self.setFixedSize(QSize(600, 400))

        self.setCentralWidget(widget)

        # initialize fg
        self.fg = fluxgateLJ(csv_log=True, increment=1)
        self.fg.setup(x=0,y=1,z=2)


    def spacebarPressed(self, event):
        """Trigger measurement if spacebar pressed

        """
        if isinstance(event, QKeyEvent):
            self.measure

    def measure(self):
        """Take measuremetn

        """
        dat = self.fg.read_single()

        self.x.setText(f"X: {dat[0]:.2f}")
        self.y.setText(f"Y: {dat[1]:.2f}")
        self.z.setText(f"Z: {dat[2]:.2f}")


# start application
app = QApplication(sys.argv)

# open window
window = MainWindow()
window.show()
sys.exit(app.exec_())