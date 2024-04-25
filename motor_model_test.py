def calculate_pwm_from_gear_speed_debug(desired_gear_speed):
    # Constants from linear regression recalculated for direct use
    gear_motor_slope = 0.00320
    gear_motor_intercept = 0.4000
    motor_pwm_slope = 36.394
    motor_pwm_intercept = -300.667

    # Calculate motor speed from gear speed using the linear equation
    estimated_motor_speed = (
        desired_gear_speed - gear_motor_intercept
    ) / gear_motor_slope
    print(f"Estimated Motor Speed: {estimated_motor_speed}")

    # Calculate PWM from motor speed using the linear equation
    estimated_pwm = (estimated_motor_speed - motor_pwm_intercept) / motor_pwm_slope
    print(f"Raw PWM: {estimated_pwm}")

    # Ensure PWM is within the valid range of 0 to 100
    estimated_pwm = max(0, min(estimated_pwm, 100))

    return estimated_pwm


# Test the function with multiple gear speeds
test_gear_speeds = [5, 10, 15]  # Example gear speeds in RPM
for gear_speed in test_gear_speeds:
    calculated_pwm = calculate_pwm_from_gear_speed_debug(gear_speed)
    print(f"Calculated PWM for Gear Speed {gear_speed} RPM: {calculated_pwm}")
