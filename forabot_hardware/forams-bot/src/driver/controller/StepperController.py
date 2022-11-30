from driver.motor.PinStepper import PinStepper

class StepperController:
    def __init__(self,pin_dict):
        self.isolation_pin = PinStepper(pin_dict['isolation_pin']['serial_num'], pin_dict['isolation_pin']['position_dict'])
        self.imaging_pin = PinStepper(pin_dict['imaging_pin']['serial_num'], pin_dict['imaging_pin']['position_dict'])
        self.focal_stepper = None
        if 'focal_stepper' in pin_dict:
            self.focal_stepper = PinStepper(pin_dict['focal_stepper']['serial_num'], pin_dict['focal_stepper']['position_dict'])
        self.start_focal_offset = 0

    def setFocalPlane(self, focal_plane):
        if self.focal_stepper:
            self.imaging_pin.pinMove('imaging')
            self.focal_stepper.focalPlane(focal_plane+self.start_focal_offset)
        else:
            self.imaging_pin.focalPlane(focal_plane+self.start_focal_offset)

    def imagingBottom(self):
        self.imaging_pin.pinMove('base')

    def isolationBottom(self):
        self.isolation_pin.pinMove('base')

    def focalBottom(self):
        self.focal_stepper.pinMove('base')

    def imagingHandoff(self):
        self.imaging_pin.pinMove('handoff')

    def isolationHandoff(self):
        self.isolation_pin.pinMove('handoff')

    def isolationCheck(self):
        self.isolation_pin.pinMoveHalf('handoff')

    def imageForam(self):
        if self.focal_stepper:
            self.imaging_pin.pinMove('imaging')
            self.focal_stepper.focalPlane(self.start_focal_offset)
        else:
            self.imaging_pin.focalPlane(self.start_focal_offset)

    def stop(self):
        self.imaging_pin.deenergize()
        self.isolation_pin.deenergize()
        if self.focal_stpper:
            self.focal_stepper.deenergize()

    def homePins(self):
        self.imaging_pin.home()
        self.imagingBottom()
        self.isolation_pin.home()
        self.isolationBottom()
        if self.focal_stepper:
            self.focal_stepper.home()
            self.focal_stepper.home()
            self.focal_stepper.home()
            self.focalBottom()

    def setFocalOffset(self, start_focal_offset):
        self.start_focal_offset = start_focal_offset
