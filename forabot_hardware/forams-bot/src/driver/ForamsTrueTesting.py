import time
from driver.controller import ForamsMotorController, ForamsServoController
import config_setup.ConfigUtility as CU
from driver.ForamsSystem import ForamsSystem

class ForamsTrueTesting(ForamsSystem):
    def __init__(self):
        self.conf_dict = CU.parseFile('/home/pi/Forams/forams-bot/configurations/config_test_1.json')
        self.failure_threshold = 5
        self.image_orientations = 12
        motor_dict, servo_dict = CU.partitionDicts(self.conf_dict)
        self.motor_controller = ForamsMotorController.ForamsMotorController(motor_dict)
        self.servo_controller = ForamsServoController.ForamsServoController(servo_dict)
        self.request_ui_input = '{"end_point":"ui","function":"getNextUserCommand","args":[]}'
        self.request_imaging = '{"end_point":"camera","function":"takeImage","args":{"foram_id":"{0}","orientation_id":"{1}"}}'

    def testIsolation(self):
        self.motor_controller.pickIsolationForam()
        time.sleep(1)
        self.motor_controller.clearIsolation()
        return self.request_ui_input

    def testImaging(self):
        self.motor_controller.pickImagingForam()
        time.sleep(1)
        self.motor_controller.clearImaging()
        return self.request_ui_input

    def testTransferImagingToIsolation(self):
        self.transferImagingToIsolation()
        return self.request_ui_input

    #def testImaging(self):
    #    self.testTransferImagingToIsolation()
    #    self.imageForam()

