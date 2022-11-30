import time

class SuctionMotor:
    def __init__(self, motor, motor_name, var_dict):
        self.motor_name = motor_name
        for key in var_dict.keys():
            setattr(self, key, var_dict[key])
        self.motor = motor
        self.off()

    def on(self):
        self.motor.throttle = self.throttle

    def off(self):
        self.motor.throttle = None
