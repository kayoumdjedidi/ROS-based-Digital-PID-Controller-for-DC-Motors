import matplotlib.pyplot as plt
import numpy as np
from Controller_PID import PIDController


class MotorSystem:
    def __init__(self, Kp, Ki, Kd, gear_motor_slope=0.00320, gear_motor_intercept=0.4000, motor_pwm_slope=36.394,
                 motor_pwm_intercept=-300.667):
        self.pid = PIDController(Kp, Ki, Kd)
        self.gear_motor_slope = gear_motor_slope
        self.gear_motor_intercept = gear_motor_intercept
        self.motor_pwm_slope = motor_pwm_slope
        self.motor_pwm_intercept = motor_pwm_intercept

    def calculate_pwm_from_gear_speed(self, desired_gear_speed):
        estimated_motor_speed = (desired_gear_speed - self.gear_motor_intercept) / self.gear_motor_slope
        print(f"Estimated Motor Speed: {estimated_motor_speed}")
        estimated_pwm = (estimated_motor_speed - self.motor_pwm_intercept) / self.motor_pwm_slope
        print(f"Raw PWM: {estimated_pwm}")
        estimated_pwm = max(0, min(estimated_pwm, 100))
        return estimated_motor_speed, estimated_pwm

    def control_motor(self, setpoint, dt, time_end):
        times = np.arange(0, time_end, dt)
        motor_speeds = []
        gear_speeds = []
        pwms = []

        for t in times:
            motor_speed, pwm = self.calculate_pwm_from_gear_speed(setpoint)
            motor_speeds.append(motor_speed)
            control_signal = self.pid.update(setpoint, motor_speed, dt)
            control_pwm = max(0, min(control_signal, 100))
            pwms.append(control_pwm)
            gear_speeds.append(motor_speed * self.gear_motor_slope + self.gear_motor_intercept)

        return times, motor_speeds, gear_speeds, pwms

    def plot_motor_control(self, setpoint, dt, time_end):
        times, motor_speeds, gear_speeds, pwms = self.control_motor(setpoint, dt, time_end)
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.plot(times, motor_speeds, '-o', label='Motor Speed')
        plt.title('Motor Speed vs. Time')
        plt.xlabel('Time (s)')
        plt.ylabel('Motor Speed (Encoder Counts)')
        plt.grid(True)
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(times, pwms, '-o', color='red', label='PWM')
        plt.title('PWM vs. Time')
        plt.xlabel('Time (s)')
        plt.ylabel('PWM (%)')
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    motor_system = MotorSystem(Kp=1.0, Ki=0.1, Kd=0.05)
    motor_system.plot_motor_control(setpoint=5.0, dt=0.01, time_end=2.0)
