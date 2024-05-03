class MotorController:
    def __init__(self, Kc, Pc):
        self.Kc = Kc
        self.Pc = Pc
        self.prev_error = 0
        self.integral = 0

    def update(self, setpoint, feedback):
        error = setpoint - feedback
        self.integral += error
        self.integral = max(min(self.integral, 100), -100)  # Anti-windup clamping
        derivative = error - self.prev_error

        # P Controller
        Kp = 0.5 * self.Kc
        p_output = Kp * error

        # PI Controller
        Ki = 0 * self.Kc / self.Pc
        i_output = Ki * self.integral

        # PID Controller
        Kd = 0 * self.Kc * self.Pc
        d_output = Kd * derivative

        output = p_output + i_output + d_output

        # Save error for next iteration
        self.prev_error = error

        return output

def calculate_pwm_from_gear_speed_debug(desired_gear_speed, setpoint):
    # Constants from linear regression recalculated for direct use
    gear_motor_slope = 0.00320
    gear_motor_intercept = 0.4000
    motor_pwm_slope = 36.394
    motor_pwm_intercept = -300.667

    # Calculate motor speed from gear speed using the linear equation
    estimated_motor_speed = (desired_gear_speed - gear_motor_intercept) / gear_motor_slope

    # Instantiate the MotorController with realistically tuned parameters
    controller = MotorController(Kc=1.5, Pc=10.0)  # Adjust Kc and Pc as needed

    # Calculate PWM from motor speed using the PID controller
    estimated_pwm = controller.update(setpoint, estimated_motor_speed)

    # Ensure PWM is within the valid range of 0 to 100
    estimated_pwm = max(0, min(estimated_pwm, 100))

    return estimated_pwm

# Test the function with multiple gear speeds
test_gear_speeds = [5, 10, 15]  # Example gear speeds in RPM
setpoint = 1500  # Example realistic setpoint based on typical motor speed
for gear_speed in test_gear_speeds:
    calculated_pwm = calculate_pwm_from_gear_speed_debug(gear_speed, setpoint)
    print(f"Calculated PWM for Gear Speed {gear_speed} RPM: {calculated_pwm}")
