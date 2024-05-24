import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QGroupBox, QHBoxLayout, QLineEdit, \
    QPushButton, QMessageBox, QRadioButton
from PyQt6.QtCore import QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from full_system import MotorSystem

# Set white mode configuration
#os.environ['QT_QPA_PLATFORM'] = 'windows:darkmode=0'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #example values

        self.speed_values = [100, 110, 120, 130, 135]
        self.position_values = [50, 60, 45, 55, 65]
        self.index = 0
        self.setWindowTitle("Control panel: ROS based Digital PID Controller for DC-Motors")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.create_settings_groupbox()
        self.create_plot_groupbox()

        self.layout.addWidget(self.settings_groupbox)
        self.layout.addWidget(self.plot_groupbox)


        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)

        self.speed_values = []
        self.position_values = []

        # Initialize attributes
        self.times = []
        self.motor_speeds = []
        self.gear_speeds = []
        self.pwms = []
        self.motor_system = None  # Ensure motor_system is initialized

    def create_settings_groupbox(self):
        self.settings_groupbox = QGroupBox("Control Method:")
        self.settings_layout = QVBoxLayout()

        # Layout for BO and BF selection
        control_method_layout = QHBoxLayout()

        # Radio buttons for control method selection
        self.radio_BO = QRadioButton("Boucle Ouverte")
        self.radio_BF = QRadioButton("Boucle Fermée")
        control_method_layout.addWidget(self.radio_BO)
        control_method_layout.addWidget(self.radio_BF)

        self.radio_BO.toggled.connect(self.update_control_method)
        self.radio_BF.toggled.connect(self.update_control_method)

        self.settings_layout.addLayout(control_method_layout)

        # PID settings
        self.pid_settings_layout = QVBoxLayout()

        # Radio buttons for controller type selection
        self.radio_proportional = QRadioButton("Proportionnel")
        self.radio_pi = QRadioButton("PI")
        self.radio_pid = QRadioButton("PID")
        self.pid_settings_layout.addWidget(self.radio_proportional)
        self.pid_settings_layout.addWidget(self.radio_pi)
        self.pid_settings_layout.addWidget(self.radio_pid)

        # Label and QLineEdit for kr
        self.label_kr = QLabel("Coefficient kr:", self)
        self.edit_kr = QLineEdit(self)
        self.pid_settings_layout.addWidget(self.label_kr)
        self.pid_settings_layout.addWidget(self.edit_kr)

        # Label and QLineEdit for tau_i (added for PI)
        self.label_tau_i = QLabel("Coefficient tau_i:", self)
        self.edit_tau_i = QLineEdit(self)
        self.pid_settings_layout.addWidget(self.label_tau_i)
        self.pid_settings_layout.addWidget(self.edit_tau_i)

        # Label and QLineEdit for tau_d (added for PID)
        self.label_tau_d = QLabel("Coefficient tau_d:", self)
        self.edit_tau_d = QLineEdit(self)
        self.pid_settings_layout.addWidget(self.label_tau_d)
        self.pid_settings_layout.addWidget(self.edit_tau_d)

        self.settings_layout.addLayout(self.pid_settings_layout)

        # Button to apply settings
        self.apply_button = QPushButton("Save Selection")
        self.apply_button.clicked.connect(self.apply_settings)
        self.settings_layout.addWidget(self.apply_button)

        # Additional inputs for consigne de vitesse and position
        self.label_consigne_vitesse = QLabel("Consigne de vitesse:", self)
        self.edit_consigne_vitesse = QLineEdit(self)
        self.settings_layout.addWidget(self.label_consigne_vitesse)
        self.settings_layout.addWidget(self.edit_consigne_vitesse)

        self.label_consigne_position = QLabel("Consigne de position:", self)
        self.edit_consigne_position = QLineEdit(self)
        self.settings_layout.addWidget(self.label_consigne_position)
        self.settings_layout.addWidget(self.edit_consigne_position)

        self.label_consigne_erreur = QLabel("Consigne d'erreur:", self)
        self.edit_consigne_erreur = QLineEdit(self)
        self.settings_layout.addWidget(self.label_consigne_erreur)
        self.settings_layout.addWidget(self.edit_consigne_erreur)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_acquisition)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_acquisition)

        self.settings_layout.addWidget(self.start_button)
        self.settings_layout.addWidget(self.stop_button)

        self.settings_groupbox.setLayout(self.settings_layout)

        self.update_control_method()  # Initialize visibility based on the default selection

    def update_control_method(self):
        if self.radio_BF.isChecked() or self.radio_proportional or self.radio_pi.isChecked() or self.radio_pid.isChecked():
            self.set_pid_settings_visibility(True)
        else:
            self.set_pid_settings_visibility(False)

    def set_pid_settings_visibility(self, visible):
        self.label_kr.setVisible(visible)
        self.edit_kr.setVisible(visible)
        self.label_tau_i.setVisible(visible)
        self.edit_tau_i.setVisible(visible)
        self.label_tau_d.setVisible(visible)
        self.edit_tau_d.setVisible(visible)
        self.radio_proportional.setVisible(visible)
        self.radio_pi.setVisible(visible)
        self.radio_pid.setVisible(visible)

    def create_plot_groupbox(self):
        self.plot_groupbox = QGroupBox("Plots")
        self.plot_layout = QVBoxLayout()

        self.figure, (self.ax_speed, self.ax_position) = plt.subplots(2, 1, figsize=(10, 8))
        self.canvas = FigureCanvas(self.figure)

        self.ax_speed.set_title("Vitesse du moteur")
        self.ax_speed.set_xlabel("Temps (s)")
        self.ax_speed.set_ylabel("Vitesse (RPM)")

        self.ax_position.set_title("Position du moteur")
        self.ax_position.set_xlabel("Temps (s)")
        self.ax_position.set_ylabel("Position (units)")

        self.plot_layout.addWidget(self.canvas)
        self.plot_groupbox.setLayout(self.plot_layout)

        # Add labels for motor parameters under the canvas
        self.label_speed = QLabel("Vitesse du moteur : ", self)
        self.label_position = QLabel("Position du moteur : ", self)

        # Add borders to labels
        self.label_speed.setStyleSheet("border: 1px solid black;")
        self.label_position.setStyleSheet("border: 1px solid black;")

        # Add the labels to the layout after the canvas
        self.plot_layout.addWidget(self.label_speed)
        self.plot_layout.addWidget(self.label_position)

    def apply_settings(self):
        try:
            kr = float(self.edit_kr.text())
            tau_i = float(self.edit_tau_i.text()) if self.edit_tau_i.isVisible() else 0
            tau_d = float(self.edit_tau_d.text()) if self.edit_tau_d.isVisible() else 0

            if self.radio_proportional.isChecked():
                self.update_pid_controller(kr, 0, 0)
            elif self.radio_pi.isChecked():
                self.update_pid_controller(kr, tau_i, 0)
            elif self.radio_pid.isChecked():
                self.update_pid_controller(kr, tau_i, tau_d)

            QMessageBox.information(self, "Settings Applied", "The PID settings have been applied successfully.")
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", f"Invalid input: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def update_pid_controller(self, kp, ki, kd):
        self.motor_system = MotorSystem(Kp=kp, Ki=ki, Kd=kd)

    def start_acquisition(self):
        self.timer.start(1000)  # Update plot every second

        # Example: Show connection status
        QMessageBox.information(self, "Connection Status", "Connected to device.")

        try:
            input_value = self.edit_consigne_vitesse.text()
            print(f"Input value for consigne de vitesse: '{input_value}'")  # Debug print statement

            setpoint = int(input_value)  # Setpoint from user input
            dt = 0.01  # Example time step
            time_end = 10  # Example duration

            if self.motor_system is None:
                raise Exception("MotorSystem is not initialized. Apply settings first.")

            # Ensure control_motor returns four values
            result = self.motor_system.control_motor(setpoint, dt, time_end)
            if len(result) != 4:
                raise ValueError(f"Expected 4 values from control_motor, got {len(result)}")

            self.times, self.motor_speeds, self.gear_speeds, self.pwms = result
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", f"Invalid input for consigne de vitesse: {e}")
            self.timer.stop()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during acquisition: {e}")
            self.timer.stop()

    def stop_acquisition(self):
        try:
            self.timer.stop()
        except Exception as e:
            QMessageBox.warning(self, "Connection Status", "Connection lost.")
            QMessageBox.critical(self, "Error", f"An error occurred while stopping: {e}")

    def update_plot(self):
        try:
            self.ax_speed.clear()
            self.ax_position.clear()

            self.ax_speed.plot(self.times, self.motor_speeds, 'r-')
            self.ax_position.plot(self.times, self.gear_speeds, 'g-')

            self.ax_speed.set_title("Vitesse du moteur")
            self.ax_speed.set_xlabel("Temps (s)")
            self.ax_speed.set_ylabel("Vitesse (RPM)")

            self.ax_position.set_title("Position du moteur")
            self.ax_position.set_xlabel("Temps (s)")
            self.ax_position.set_ylabel("Position (units)")

            for i in range(len(self.speed_values)):
                speed = self.speed_values[i]
                position = self.position_values[i]

                self.label_speed.setText("Vitesse du moteur : {} RPM".format(speed))
                self.label_position.setText("Position du moteur : {} degrés".format(position))

                # Clear previous plots
                self.ax_speed.clear()
                self.ax_position.clear()

                # Update plots
                self.ax_speed.plot(self.speed_values[:i + 1], 'r-')
                self.ax_position.plot(self.position_values[:i + 1], 'g-')
                self.canvas.draw()
                QApplication.processEvents()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while updating the plot: {e}")

'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
'''