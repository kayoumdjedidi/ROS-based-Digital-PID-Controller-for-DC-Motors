import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QGroupBox, QHBoxLayout, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QRadioButton, QVBoxLayout, QWidget, QGroupBox, QHBoxLayout

# Set white  mode configuration
# To disable dark mode, use 'darkmode=0' instead of 'darkmode=1'
os.environ['QT_QPA_PLATFORM'] = 'windows:darkmode=0'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Acquisition de données en temps réel")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Group box for control method selection
        self.control_group_box = QGroupBox("Méthode de contrôle:", self)
        self.control_layout = QVBoxLayout()
        self.control_group_box.setLayout(self.control_layout)

        self.radio_proportional = QRadioButton("Proportionnel", self)
        self.radio_pi = QRadioButton("PI", self)
        self.radio_pid = QRadioButton("PID", self)
        self.radio_proportional.setChecked(True)  # Default selection

        self.control_layout.addWidget(self.radio_proportional)
        self.control_layout.addWidget(self.radio_pi)
        self.control_layout.addWidget(self.radio_pid)

        # Group box for tuning approach selection
        self.tuning_group_box = QGroupBox("Approche d'ajustement:", self)
        self.tuning_layout = QVBoxLayout()
        self.tuning_group_box.setLayout(self.tuning_layout)

        self.radio_ziegler_nichols = QRadioButton("Ziegler-Nichols", self)
        self.radio_continuous_pid = QRadioButton("Continuous PID Transposition", self)
        self.radio_ziegler_nichols.setChecked(True)  # Default selection

        self.tuning_layout.addWidget(self.radio_ziegler_nichols)
        self.tuning_layout.addWidget(self.radio_continuous_pid)

        # Labels for motor parameters
        self.label_speed = QLabel("Vitesse du moteur : ", self)
        self.label_position = QLabel("Position du moteur : ", self)

        # Add borders to labels
        self.label_speed.setStyleSheet("border: 1px solid black;")
        self.label_position.setStyleSheet("border: 1px solid black;")

        self.layout.addWidget(self.label_speed)
        self.layout.addWidget(self.label_position)

        # Add group boxes to main layout
        self.layout.addWidget(self.control_group_box)
        self.layout.addWidget(self.tuning_group_box)

        # Add input fields for setting speed and position setpoints
        self.add_setpoint_fields()

        # Add buttons for starting and stopping experiments
        self.add_experiment_buttons()

        # Example data for motor parameters
        self.speed_values = [100, 110, 120, 130, 135]
        self.position_values = [50, 60, 45, 55, 65]
        self.index = 0

        # Timer for updating data
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)

        # Matplotlib figure and canvas
        self.figure = plt.figure(facecolor='#f0f0f0')  # Light gray background for the figure
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # Line plots for motor parameters
        self.ax_speed = self.figure.add_subplot(211)
        self.ax_position = self.figure.add_subplot(212)

        # Set background color for each axis
        self.ax_speed.set_facecolor('#f0f0f0')  # Light gray
        self.ax_position.set_facecolor('#f0f0f0')  # Light gray

        # Apply gradient background
        self.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #ffffff, stop: 1 #dddddd);")

    def add_setpoint_fields(self):
        setpoint_layout = QVBoxLayout()

        speed_setpoint_label = QLabel("Consigne de vitesse:", self)
        self.speed_setpoint_edit = QLineEdit(self)

        position_setpoint_label = QLabel("Consigne de position:", self)
        self.position_setpoint_edit = QLineEdit(self)

        setpoint_layout.addWidget(speed_setpoint_label)
        setpoint_layout.addWidget(self.speed_setpoint_edit)
        setpoint_layout.addWidget(position_setpoint_label)
        setpoint_layout.addWidget(self.position_setpoint_edit)

        self.layout.addLayout(setpoint_layout)

    def add_experiment_buttons(self):
        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_experiment)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_experiment)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        self.layout.addLayout(button_layout)

    def start_experiment(self):
        self.timer.start(1000)

        # Example: Show connection status
        QMessageBox.information(self, "Connection Status", "Connected to device.")

    def stop_experiment(self):
        self.timer.stop()

        # Example: Show connection status
        QMessageBox.warning(self, "Connection Status", "Connection lost.")

    def update_data(self):
        # Loop through the values for continuous updating
        for i in range(len(self.speed_values)):
            speed = self.speed_values[i]
            position = self.position_values[i]

            self.label_speed.setText("Vitesse du moteur : {} RPM".format(speed))
            self.label_position.setText("Position du moteur : {} degrés".format(position))

            # Clear previous plots
            self.ax_speed.clear()
            self.ax_position.clear()

            # Update plots
            self.ax_speed.plot(self.speed_values[:i+1], 'r-')
            self.ax_position.plot(self.position_values[:i+1], 'g-')

            self.canvas.draw()
            QApplication.processEvents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
