import time
import RPi.GPIO as GPIO

TRIG = 38
ECHO = 40
ERROR_DISTANCE = 10000

class Sonar():
    def __init__(self):
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)

    def getDistance(self):
        try:
            GPIO.setup(TRIG, GPIO.LOW)
            time.sleep(0.1)

            GPIO.output(TRIG, GPIO.HIGH)
            time.sleep(0.00001)

            GPIO.output(TRIG, GPIO.LOW)

            echo_count = 0 
            while GPIO.input(ECHO) == GPIO.LOW:
                assert echo_count < 1000
                echo_count += 1
                sonarStartTime = time.time()
                
            while GPIO.input(ECHO) == GPIO.HIGH:
                sonarEndTime = time.time()
            
            distance = (sonarEndTime - sonarStartTime) / 58 * 1000000
            
            return True, distance
        except Exception as e:
            return False, ERROR_DISTANCE