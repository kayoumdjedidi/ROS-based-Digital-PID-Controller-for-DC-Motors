import sys
import time
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt

GPIO.setmode(GPIO.BOARD)

StepPinForward = 18  # M1 #GPIO24
StepPinBackward = 16  # M2 #GPIO23
PWMPin = 35  # ENA # GPIO19
Enc_A = 36  # GPIO16
test_duration = 10
ppr = 24  # d apres cdc
reduction_ratio = 226

counter = 0

GPIO.setup(StepPinForward, GPIO.OUT)
GPIO.setup(StepPinBackward, GPIO.OUT)
GPIO.setup(PWMPin, GPIO.OUT)
motor_pwm = GPIO.PWM(PWMPin, 5000)
motor_pwm.start(0)

def init():
    print("Rotary Encoder Test Program")
    GPIO.setup(Enc_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(Enc_A, GPIO.RISING, callback=rotation_decode)
    return

def rotation_decode(channel):
    global counter
    counter += 1

def calculate_speeds():
    motor_speed = ((counter / ppr) / test_duration) * 60
    gear_speed = motor_speed / reduction_ratio
    return motor_speed, gear_speed

def get_speeds(pwm_value):
    motor_speed_list = []
    gear_speed_list = []
    for _ in range(test_duration):
        time.sleep(1)
        motor_speed, gear_speed = calculate_speeds()
        motor_speed_list.append(motor_speed)
        gear_speed_list.append(gear_speed)
    return motor_speed_list, gear_speed_list

def plot_speeds(motor_speed_list, gear_speed_list):
    time_values = range(1, test_duration + 1)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    ax1.plot(time_values, motor_speed_list, label='Motor Speed', color='blue')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Speed (RPM)')
    ax1.set_title('Motor Speed over Time')
    ax1.grid(True)
    
    ax2.plot(time_values, gear_speed_list, label='Gear Speed', color='green')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Speed (RPM)')
    ax2.set_title('Gear Speed over Time')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()

try:
    init()
    pwm_value = 100  # Default PWM value
    motor_speed_list, gear_speed_list = get_speeds(pwm_value)
    plot_speeds(motor_speed_list, gear_speed_list)

except KeyboardInterrupt:
    GPIO.cleanup()
