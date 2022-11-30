from driver.motor.LimitedServo import LimitedServo
import time

class ServoController:
    def __init__(self,servo_dict):
        self.well_servo = LimitedServo(servo_dict['well_servo']['motor_idx'], servo_dict['well_servo']['position_dict'])
        self.actuator_servo = LimitedServo(servo_dict['actuator_servo']['motor_idx'], servo_dict['actuator_servo']['position_dict'])

    def moveWellToIdx(self, well_num):
        self.well_servo.turnTo(str(well_num))

    def moveToWell(self):
        self.actuator_servo.turnTo('well_suction')

    def moveToImaging(self):
        self.actuator_servo.turnTo('imgaging_location')

    def moveToImagingPick(self):
        self.actuator_servo.turnTo('imaging_suction')

    def moveToIsolationPick(self):
        self.actuator_servo.turnTo('isolation_suction')

    def moveToIsolationIsolationWebcam(self):
        self.actuator_servo.turnTo('isolation_webcam')
        time.sleep(0.5)

    def moveToImagingWebcam(self):
        self.actuator_servo.turnTo('imaging_webcam')
        time.sleep(0.5)
