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


def forward(speed):
    GPIO.output(StepPinForward, GPIO.HIGH)
    GPIO.output(StepPinBackward, GPIO.LOW)
    motor_pwm.ChangeDutyCycle(speed)

def reverse(x,speed):
    GPIO.output(StepPinBackward, GPIO.LOW)
    print("backwarding running motor")
    PWM.start(speed)
    time.sleep(x)
    GPIO.output(StepPinBackward, GPIO.HIGH)
    PWM.stop()



try:
    while True :
        #print("forward motor")
        forward(100)
        #print("reverse motor")
        #reverse(5,100)
        
except KeyboardInterrupt: 
    GPIO.cleanup()
