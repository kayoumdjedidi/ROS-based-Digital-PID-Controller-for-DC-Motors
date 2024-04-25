import RPi.GPIO as GPIO
import time

counter = 0
Enc_A = 27                                                                                        
test_duration = 10
ppr = 24
reduction_ratio = 226

StepPinForward = 11  # M3
StepPinBackward = 15  # M4
PWMPin = 33  # ENB
sleeptime = 1
""" 
input 11.7v
counter 17062 tours equivalent a: 4265.5 rpm
RPM du reducteur:18.873893805309734 """

def init():
    print ("Rotary Encoder Test Program")
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Enc_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(Enc_A, GPIO.RISING, callback=rotation_decode)

    GPIO.setup(StepPinForward, GPIO.OUT)
    GPIO.setup(StepPinBackward, GPIO.OUT)
    GPIO.setup(PWMPin, GPIO.OUT)

    return


def rotation_decode(channel):
    global counter 

    if (Enc_A) :
        counter += 1

def forward(x,speed):
    GPIO.output(StepPinForward, GPIO.HIGH)
    print ("forwarding running  motor")
    PWM.start(speed)
    time.sleep(x)
    GPIO.output(StepPinForward, GPIO.LOW)
    PWM.stop()

def reverse(x,speed):
    GPIO.output(StepPinBackward, GPIO.HIGH)
    print("backwarding running motor")
    PWM.start(speed)
    time.sleep(x)
    GPIO.output(StepPinBackward, GPIO.LOW)
    PWM.stop()
        

try:
    init()
    while True :
        print("forward motor")
        forward(5)
        print("reverse motor")
        reverse(5)
        print("Stopping motor")
        PWM = GPIO.PWMPin(33, 1)
        time.sleep(test_duration)
        print("counter",counter)
        motor_speed= ((counter / ppr) / test_duration) * 60
        gear_speed= motor_speed / reduction_ratio
        print(motor_speed)
        print(gear_speed)
        counter = 0
except KeyboardInterrupt: 
    GPIO.cleanup()


    