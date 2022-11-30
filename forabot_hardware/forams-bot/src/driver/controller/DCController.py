import importlib
import driver.motor
from adafruit_motorkit import MotorKit
import time

class DCController:
    def __init__(self, dict):
        self.hats = []
        self.isolation_suction = None
        self.imaging_suction = None
        self.top_suction = None
        for hat_name in dict.keys():
            hat_addr = dict[hat_name]['Address']
            tmp_hat = MotorKit(address=int(hat_addr,base=16))
            self.hats.append(tmp_hat)
            hat_motors = dict[hat_name]['Motors']
            for motor_desc in hat_motors.keys():
                tmp_motor = getattr(tmp_hat, hat_motors[motor_desc]["Motor Location"])
                module = importlib.import_module("driver.motor."+hat_motors[motor_desc]["Motor Type"])
                tmp_class = getattr(module,hat_motors[motor_desc]["Motor Type"])
                setattr(self, motor_desc, tmp_class(tmp_motor, motor_desc, hat_motors[motor_desc]['Variable Dictionary']))

    def imagingSuctionOn(self):
        self.imaging_suction.on()

    def imagingSuctionOff(self):
        self.imaging_suction.off()

    def isolationSuctionOn(self):
        self.isolation_suction.on()

    def isolationSuctionOff(self):
        self.isolation_suction.off()

    def topSuctionOn(self):
        self.top_suction.on()

    def topSuctionOff(self):
        self.top_suction.off()

    def imagingHandoff(self):
        self.top_suction.on()
        self.imagingSuctionOff()

    def isolationHandoff(self):
        self.top_suction.on()
        self.isolationSuctionOff()

    def dropForam(self):
        self.top_suction.off()
