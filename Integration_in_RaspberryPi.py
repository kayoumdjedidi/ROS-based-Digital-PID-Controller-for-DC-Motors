import sys
import time
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import numpy as np
from full_system import MotorSystem


class RaspberryPiMotorController:
    def __init__(self, step_pin_forward, step_pin_backward, pwm_pin, encoder_pin, ppr, reduction_ratio):
        self.step_pin_forward = step_pin_forward
        self.step_pin_backward = step_pin_backward
        self.pwm_pin = pwm_pin
        self.encoder_pin = encoder_pin
        self.ppr = ppr
        self.reduction_ratio = reduction_ratio
        self.counter = 0
        self.motor_pwm = None
        self.init_gpio()

    def init_gpio(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.step_pin_forward, GPIO.OUT)
        GPIO.setup(self.step_pin_backward, GPIO.OUT)
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        self.motor_pwm = GPIO.PWM(self.pwm_pin, 5000)
        self.motor_pwm.start(0)
        GPIO.setup(self.encoder_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.encoder_pin, GPIO.RISING, callback=self.rotation_decode)

    def rotation_decode(self, channel):
        self.counter += 1

    def calculate_speeds(self, duration):
        motor_speed = ((self.counter / self.ppr) / duration) * 60  # Motor speed in RPM
        gear_speed = motor_speed / self.reduction_ratio  # Gear speed in RPM
        return motor_speed, gear_speed

    def get_speeds(self, motor_system, setpoint, dt, time_end):
        times = np.arange(0, time_end, dt)
        motor_speeds = []
        gear_speeds = []
        pwms = []

        for t in times:
            time.sleep(dt)
            motor_speed, _ = self.calculate_speeds(dt)
            motor_speeds.append(motor_speed)

            control_signal = motor_system.pid.update(setpoint, motor_speed, dt)
            control_pwm = max(0, min(control_signal, 100))
            pwms.append(control_pwm)

            self.motor_pwm.ChangeDutyCycle(control_pwm)

            _, gear_speed = self.calculate_speeds(dt)
            gear_speeds.append(gear_speed)

        return times, motor_speeds, gear_speeds, pwms

    def plot_speeds(self, times, motor_speeds, gear_speeds, pwms):
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))

        ax1.plot(times, motor_speeds, label='Motor Speed', color='blue')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Motor Speed (RPM)')
        ax1.set_title('Motor Speed over Time')
        ax1.grid(True)

        ax2.plot(times, gear_speeds, label='Gear Speed', color='green')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Gear Speed (RPM)')
        ax2.set_title('Gear Speed over Time')
        ax2.grid(True)

        ax3.plot(times, pwms, label='PWM', color='red')
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('PWM (%)')
        ax3.set_title('PWM over Time')
        ax3.grid(True)

        plt.tight_layout()
        plt.show()

    def cleanup(self):
        GPIO.cleanup()


def main():
    try:
        controller = RaspberryPiMotorController(
            step_pin_forward=18,
            step_pin_backward=16,
            pwm_pin=35,
            encoder_pin=36,
            ppr=24,
            reduction_ratio=226
        )
        motor_system = MotorSystem(Kp=1.0, Ki=0.1, Kd=0.05)
        setpoint = 5.0  # Desired gear speed in RPM
        dt = 0.01  # Time step for control loop
        time_end = 10  # Total time for simulation in seconds

        times, motor_speeds, gear_speeds, pwms = controller.get_speeds(motor_system, setpoint, dt, time_end)
        controller.plot_speeds(times, motor_speeds, gear_speeds, pwms)

    except KeyboardInterrupt:
        controller.cleanup()
    finally:
        controller.cleanup()


if __name__ == "__main__":
    main()
