import matplotlib.pyplot as plt

class MotorModel:
    def __init__(self, gear_motor_slope=0.00320, gear_motor_intercept=0.4000, motor_pwm_slope=36.394, motor_pwm_intercept=-300.667):
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

    def plot_relationships(self, gear_speeds):
        motor_speeds = []
        pwms = []
        for gear_speed in gear_speeds:
            motor_speed, pwm = self.calculate_pwm_from_gear_speed(gear_speed)
            motor_speeds.append(motor_speed)
            pwms.append(pwm)

        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.plot(gear_speeds, motor_speeds, '-o', label='Motor Speed')
        plt.title('Motor Speed vs. Gear Speed')
        plt.xlabel('Gear Speed (RPM)')
        plt.ylabel('Motor Speed (Encoder Counts)')
        plt.grid(True)
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(gear_speeds, pwms, '-o', color='red', label='PWM')
        plt.title('PWM vs. Gear Speed')
        plt.xlabel('Gear Speed (RPM)')
        plt.ylabel('PWM (%)')
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    motor_model = MotorModel()
    gear_speeds = range(5, 16)
    motor_model.plot_relationships(gear_speeds)
