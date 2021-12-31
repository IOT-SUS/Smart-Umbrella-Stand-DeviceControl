import time
import RPi.GPIO as GPIO

SERVO_PIN = 11

class Servo():
    def __init__(self):
        # Set pin 11 as an output, and set servo1 as pin 11 as PWM
        GPIO.setup(SERVO_PIN, GPIO.OUT)
        self.servo = GPIO.PWM(SERVO_PIN, 50) # Note 11 is pin, 50 = 50Hz pulse
        self.reset()
        
    def reset(self):
        #start PWM running, but with value of 0 (pulse off)
        self.servo.start(0)
        time.sleep(2)

        # Turn back to 90 degrees
        self.open()

        #turn back to 0 degrees
        self.close()

    def open(self):
        # Turn back to 90 degrees
        self.servo.ChangeDutyCycle(7)
        time.sleep(0.5)
        self.servo.ChangeDutyCycle(0)
        time.sleep(1.5)

    def close(self):
        #turn back to 0 degrees
        self.servo.ChangeDutyCycle(2)
        time.sleep(0.5)
        self.servo.ChangeDutyCycle(0)
