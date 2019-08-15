import RPi.GPIO as GPIO
from time import sleep

Motor1A = 22
Motor1B = 23
Motor1E = 25
Motor2A = 19
Motor2B = 26
Motor2E = 13

GPIO.setmode(GPIO.BCM) 
GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)
GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor2E, GPIO.OUT)
pwm = GPIO.PWM(13, 100)

def forward():

    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1E, GPIO.HIGH)
    sleep(5)
    GPIO.output(Motor1E, GPIO.LOW)
 
def turn():
    pwm.start(50)
    GPIO.output(Motor2A, GPIO.HIGH)
    GPIO.output(Motor2B, GPIO.LOW)
    GPIO.output(Motor2E, GPIO.HIGH)
    sleep(2)
    pwm.stop()
    GPIO.output(Motor2E, GPIO.LOW)
 
def backward():

    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor1E, GPIO.HIGH)
    sleep(5)
    GPIO.output(Motor1E, GPIO.LOW)
    
def turn2():
    pwm.start(50)
    GPIO.output(Motor2A, GPIO.LOW)
    GPIO.output(Motor2B, GPIO.HIGH)
    GPIO.output(Motor2E, GPIO.HIGH)
    sleep(2)
    pwm.stop()
    GPIO.output(Motor2E, GPIO.LOW)


def end():

    GPIO.cleanup()


if __name__ == '__main__' :

        try:

                forward()
                sleep(2)
                turn()
                sleep(2)
                forward()

        except KeyboardInterrupt:

                print("Keyboard Interrupt")

        finally:

                end()
