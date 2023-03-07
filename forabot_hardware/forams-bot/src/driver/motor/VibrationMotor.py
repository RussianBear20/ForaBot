import RPi.GPIO as GPIO

class VibrationMotor:
    def __init__(self, pwm, pin1, pin2): # Constructor initializes vars
        self.pwm = pwm
        self.pin1 = pin1
        self.pin2 = pin2
        self.speed = None
        self.setup()
        self.off() # Turn off vibration motor

    def setup(self): # Method that sets up the GPIO pins and speeds
        GPIO.setup(self.pwm, GPIO.OUT)
        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.setup(self.pin2, GPIO.OUT)
        self.speed = GPIO.PWM(self.pwm, 50)
        self.speed.start(100)

    def on(self): # Turns on the motor 
        GPIO.output(self.pin1, GPIO.HIGH)
        GPIO.output(self.pin2, GPIO.LOW)

    def off(self): # Turns off the motor
        GPIO.output(self.pin1, GPIO.LOW)
        GPIO.output(self.pin2, GPIO.LOW)

    def stop(self): # Stops the PWM object
        self.speed.stop()
