from driver.motor.PinStepper import PinStepper

class StepperController:
    def __init__(self,pin_dict): # Constructor creates Pinstepper objects for isolation and imaging pin/ servo control
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
    # move the imaging pin to the 'base' position
    def imagingBottom(self): 
        self.imaging_pin.pinMove('base')
    # move the isolation pin to the 'base' position
    def isolationBottom(self):
        self.isolation_pin.pinMove('base')
    # move the focal stepper to the 'base' position
    def focalBottom(self):
        self.focal_stepper.pinMove('base')
    # move the imaging pin to the 'handoff' position
    def imagingHandoff(self):
        self.imaging_pin.pinMove('handoff')
    # move the isolation pin to the 'handoff' position
    def isolationHandoff(self):
        self.isolation_pin.pinMove('handoff')
    # move the isolation pin halfway to the 'handoff' position
    def isolationCheck(self):
        self.isolation_pin.pinMoveHalf('handoff')

    def imageForam(self): # This method takes a picture of the foram
        if self.focal_stepper:
            self.imaging_pin.pinMove('imaging')
            self.focal_stepper.focalPlane(self.start_focal_offset)
        else:
            self.imaging_pin.focalPlane(self.start_focal_offset)

    def stop(self): # This method turns off the stepper motor
        self.imaging_pin.deenergize()
        self.isolation_pin.deenergize()
        if self.focal_stepper: # This line used to have a typo self.focal.stpper
            self.focal_stepper.deenergize()

    def homePins(self): # This is the initial Homing of the pins to their base positions
        self.imaging_pin.home()
        self.imagingBottom()
        self.isolation_pin.home()
        self.isolationBottom()
        if self.focal_stepper:
            self.focal_stepper.home()
            self.focal_stepper.home()
            self.focal_stepper.home()
            self.focalBottom()

    def setFocalOffset(self, start_focal_offset): # This is how you set the paremeter of the focal offset
        self.start_focal_offset = start_focal_offset
