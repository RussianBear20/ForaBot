import importlib 
import driver.motor # Import motor module from driver folder
from adafruit_motorkit import MotorKit
import time

class DCController: 
    def __init__(self, dict): # Define constructor for DCController 
        self.hats = [] # Initialize variables 
        self.isolation_suction = None
        self.imaging_suction = None
        self.top_suction = None
        for hat_name in dict.keys():  # Loop through keys of input dictionary
            hat_addr = dict[hat_name]['Address'] # extract address of current hat from dict
            tmp_hat = MotorKit(address=int(hat_addr,base=16)) # Create a new MotorKit object at addresss
            self.hats.append(tmp_hat) # Adds the new object to the hats attribute
            hat_motors = dict[hat_name]['Motors'] # Extract motor object for current hat
            for motor_desc in hat_motors.keys(): # Loop through keys of the motors dict
                tmp_motor = getattr(tmp_hat, hat_motors[motor_desc]["Motor Location"]) # Get motor object with given location
                module = importlib.import_module("driver.motor."+hat_motors[motor_desc]["Motor Type"]) # Import the module for the current motor type
                tmp_class = getattr(module,hat_motors[motor_desc]["Motor Type"]) # Get the class for the current motor type
                setattr(self, motor_desc, tmp_class(tmp_motor, motor_desc, hat_motors[motor_desc]['Variable Dictionary'])) # Create a new instance of the motor class with the prior info

    def imagingSuctionOn(self): # Define method to turn on imagingSuction
        self.imaging_suction.on()

    def imagingSuctionOff(self): # Define method to turn off imagingSuction
        self.imaging_suction.off()

    def isolationSuctionOn(self): # Define method to turn on isolation Suction
        self.isolation_suction.on()

    def isolationSuctionOff(self): # Define method to turn off isolation Suction
        self.isolation_suction.off()

    def topSuctionOn(self): # Define method to turn on top Suction
        self.top_suction.on()

    def topSuctionOff(self): # Define method to turn off top Suction
        self.top_suction.off()

    def imagingHandoff(self): # Define method to turn on Suction
        self.top_suction.on()
        self.imagingSuctionOff()

    def isolationHandoff(self): # Define method to turn on suction of top vaccuum
        self.top_suction.on()
        self.isolationSuctionOff()

    def dropForam(self): # Define method to turn off suction
        self.top_suction.off()
