# Import required libraries
import sys
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

StepPinForward=18 #M1 #GPIO24
StepPinBackward=16 #M2 #GPIO23
PWMPin=35 #ENA # GPIO19
sleeptime=1

GPIO.setup(StepPinForward, GPIO.OUT)
GPIO.setup(StepPinBackward, GPIO.OUT)
GPIO.setup(PWMPin, GPIO.OUT)
motor_pwm =GPIO.PWM(PWMPin, 5000)
motor_pwm.start(0)


try:
    while True :
        GPIO.output(StepPinForward, GPIO.LOW)
        GPIO.output(StepPinBackward, GPIO.HIGH)
        motor_pwm.ChangeDutyCycle(100)
        
        
except KeyboardInterrupt: 
    GPIO.cleanup()
