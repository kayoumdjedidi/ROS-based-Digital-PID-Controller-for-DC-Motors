import sys
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

StepPinForward = 18  # M1 #GPIO24
StepPinBackward = 16  # M2 #GPIO23
PWMPin = 35  # ENA # GPIO19
Enc_A = 36  # GPIO16
test_duration = 10
ppr = 24 # d apres cdc
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
    print("Motor RPM:", motor_speed)
    print("Gear RPM:", gear_speed)

try:
    init()
    while True:
        GPIO.output(StepPinForward, GPIO.LOW)
        GPIO.output(StepPinBackward, GPIO.HIGH)
        motor_pwm.ChangeDutyCycle(100)
        time.sleep(test_duration)
        print("Counter:", counter)
        calculate_speeds()
        counter = 0

except KeyboardInterrupt:
    GPIO.cleanup()
