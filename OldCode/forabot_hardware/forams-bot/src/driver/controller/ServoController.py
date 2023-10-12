from driver.motor.LimitedServo import LimitedServo
import time

class ServoController:
    def __init__(self,servo_dict): # Constructor that creates a LimitedServo object for the well and actuator servo
        self.well_servo = LimitedServo(servo_dict['well_servo']['motor_idx'], servo_dict['well_servo']['position_dict'])
        self.actuator_servo = LimitedServo(servo_dict['actuator_servo']['motor_idx'], servo_dict['actuator_servo']['position_dict'])

    def moveWellToIdx(self, well_num): # Method for Moving Well to well Idx
        self.well_servo.turnTo(str(well_num))

    def moveToWell(self): # Method for Moving first arm to imaging well for suction
        self.actuator_servo.turnTo('well_suction')

    def moveToImaging(self): # Method for Moving first arm to imaging 
        self.actuator_servo.turnTo('imgaging_location')

    def moveToImagingPick(self): # Method for Moving first arm for suction in imaging
        self.actuator_servo.turnTo('imaging_suction')

    def moveToIsolationPick(self): # Method for Moving first arm for suction in isolatin
        self.actuator_servo.turnTo('isolation_suction')

    def moveToIsolationIsolationWebcam(self): # Method for Moving arm for isolation webcam position
        self.actuator_servo.turnTo('isolation_webcam')
        time.sleep(0.5)

    def moveToImagingWebcam(self): # Method for Moving arm for imaging webcam
        self.actuator_servo.turnTo('imaging_webcam')
        time.sleep(0.5)
