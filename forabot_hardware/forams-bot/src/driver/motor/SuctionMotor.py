import time

class SuctionMotor:
    def __init__(self, motor, motor_name, var_dict): # Constructor that initilizes vars
        self.motor_name = motor_name
        for key in var_dict.keys(): # Loop through each key in var_dict and sets corresponding attribute
            setattr(self, key, var_dict[key])
        self.motor = motor # Set value of motor to self.motor
        self.off() # Turn off the motor

    def on(self): # Turn on the motor to the throtller value (-1,1)
        self.motor.throttle = self.throttle

    def off(self): # Turn off the motor
        self.motor.throttle = None
