from driver.ForamsTrueTesting import ForamsTrueTesting
import time

class Test:

    def __init__(self):
        self.test_obj = ForamsTrueTesting()

    '''
    Section is for stepper pins.
    '''
    def imagingPinUp(self, steps, sleep, move_style):
        '''
        Moves the imaging pin up given number of steps a the defined sleep speed.
        Inputs:
        steps:  total number of steps (or microsteps) to take
        sleep: Float describing the number of seconds to sleep
        move_style: Either "single", "double", "interleave", or "microsteps". If microsteps, uses the number of microsteps in the configutation file.
        '''
        self.__movePin(self.test_obj.motor_controller.imaging_pin, steps, sleep, move_style, "up")

    def imagingPinDown(self, steps, sleep, move_style):
        '''
        Moves the imaging pin down given number of steps a the defined sleep speed.
        Inputs:
        steps:  total number of steps (or microsteps) to take
        sleep: Float describing the number of seconds to sleep
        move_style: Either "single", "double", "interleave", or "microsteps". If microsteps, uses the number of microsteps in the configutation file.
        '''
        self.__movePin(self.test_obj.motor_controller.imaging_pin, steps, sleep, move_style, "down")

    def isolationPinUp(self, steps, sleep, move_style):
        '''
        Moves the isolation pin up given number of steps a the defined sleep speed.
        Inputs:
        steps:  total number of steps (or microsteps) to take
        sleep: Float describing the number of seconds to sleep
        move_style: Either "single", "double", "interleave", or "microsteps". If microsteps, uses the number of microsteps in the configutation file.
        '''
        self.__movePin(self.test_obj.motor_controller.isolation_pin, steps, sleep, move_style, "up")

    def isolationPinDown(self, steps, sleep, move_style):
        '''
        Moves the isolation pin down given number of steps a the defined sleep speed.
        Inputs:
        steps:  total number of steps (or microsteps) to take
        sleep: Float describing the number of seconds to sleep
        move_style: Either "single", "double", "interleave", or "microsteps". If microsteps, uses the number of microsteps in the configutation file.
        '''
        self.__movePin(self.test_obj.motor_controller.isolation_pin, steps, sleep, move_style, "down")

    def __movePin(self, pin, steps, sleep, move_style_str, move_dir_str):
        pin.movePinTesting(self, move_dir_str, move_style_str, num_steps, sleep_time)


    '''
    Section is for servo motors
    '''
    def moveBoomToAngle(self, angle):
        '''
        Moves the boom to the given angle.
        Input:
        angle: Float in between 0 and 180 (or max servo range)
        '''
        self.test_obj.servo_controller.actuator_servo.setAngle(angle)

    def moveWellToAngle(self, angle):
        '''
        Moves the well to the given angle.
        Input:
        angle: Float in between 0 and 180 (or max servo range)
        '''
        self.test_obj.servo_controller.well_servo.setAngle(angle)



    '''
    Section is for suction motors
    '''
    def setIsolationSuctionThrottle(self, throttle):
        '''
        Sets the throttle to given value.
        Input:
        throttle: Float in (0,1] corresponding to (minimum speed, maximum speed] or None for PWM off
        '''
        self.test_obj.motor_controller.isolation_suction.setThrottle(throttle)

    def setImagingSuctionThrottle(self, throttle):
        '''
        Sets the throttle to given value.
        Input:
        throttle: Float in (0,1] corresponding to (minimum speed, maximum speed] or None for PWM off
        '''
        self.test_obj.motor_controller.imaging_suction.setThrottle(throttle)

    def setTopSuctionThrottle(self, throttle):
        '''
        Sets the throttle to given value.
        Input:
        throttle: Float in (0,1] corresponding to (minimum speed, maximum speed] or None for PWM off
        '''
        self.test_obj.motor_controller.top_suction.setThrottle(throttle)


    '''
    Section is for led ring
    '''
    def setLEDValue(self, led_idx, rgb_value):
        '''
        Sets a given led to a specific value
        Input:
        led_idx: value 0 to 23 for ring with 24 led
        rgb_value: intensity of the r,g,b, channels as a tuple (0,0,0) to (255,255,255)
        '''
        self.test_obj.servo_controller.neopixel.setLight(led_idx, rgb_value)


    '''
    Section is for vibration motors
    '''
    def setIsolationVibrationThrottle(self, throttle):
        '''
        Sets the throttle to given value.
        Input:
        throttle: Float in (0,1] corresponding to (minimum speed, maximum speed] or None for PWM off
        '''
        self.test_obj.motor_controller.isolation_vibration.setThrottle(throttle)

    def setImagingVibrationThrottle(self, throttle):
        '''
        Sets the throttle to given value.
        Input:
        throttle: Float in (0,1] corresponding to (minimum speed, maximum speed] or None for PWM off
        '''
        self.test_obj.motor_controller.imaging_vibration.setThrottle(throttle)
