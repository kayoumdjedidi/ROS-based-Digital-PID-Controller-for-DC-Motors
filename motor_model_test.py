import matplotlib.pyplot as plt

def calculate_pwm_from_gear_speed_debug(desired_gear_speed):
    # Constants from linear regression recalculated for direct use
    gear_motor_slope = 0.00320
    gear_motor_intercept = 0.4000
    motor_pwm_slope = 36.394
    motor_pwm_intercept = -300.667

    # Calculate motor speed from gear speed using the linear equation
    estimated_motor_speed = (desired_gear_speed - gear_motor_intercept) / gear_motor_slope
    print(f"Estimated Motor Speed: {estimated_motor_speed}")

    # Calculate PWM from motor speed using the linear equation
    estimated_pwm = (estimated_motor_speed - motor_pwm_intercept) / motor_pwm_slope
    print(f"Raw PWM: {estimated_pwm}")

    # Ensure PWM is within the valid range of 0 to 100
    estimated_pwm = max(0, min(estimated_pwm, 100))

    return estimated_motor_speed, estimated_pwm

# Prepare data for plotting
gear_speeds = range(5, 16)  # Expanding the range for a smoother curve
motor_speeds = []
pwms = []

for gear_speed in gear_speeds:
    motor_speed, pwm = calculate_pwm_from_gear_speed_debug(gear_speed)
    motor_speeds.append(motor_speed)
    pwms.append(pwm)

# Plotting
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
