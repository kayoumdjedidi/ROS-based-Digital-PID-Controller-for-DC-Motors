import sys
from PyQt6.QtWidgets import QApplication
from motor_model import MotorModel
from full_system import MotorSystem
#from Integration_in_RaspberryPi import main as raspberry_pi_main
from interface_configurable_1 import MainWindow


def main():
    # Plotting motor model relationships
    motor_model = MotorModel()
    gear_speeds = range(5, 16)
    motor_model.plot_relationships(gear_speeds)

    # Controlling the motor using PID
    motor_system = MotorSystem(Kp=1.0, Ki=0.1, Kd=0.05)
    motor_system.plot_motor_control(setpoint=5.0, dt=0.01, time_end=2.0)

    # Running the integration on Raspberry Pi
    #raspberry_pi_main()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
