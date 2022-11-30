from driver.motor.VibrationMotor import VibrationMotor
import RPi.GPIO as GPIO
import time

class VibrationController:
    def __init__(self,vibration_dict):
        self.enable_pin = vibration_dict['enable_pin']
        self.pulse_length = vibration_dict['pulse_length']
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        self.isolation_vibration1 = VibrationMotor(vibration_dict['isolation_1']['pwm'], vibration_dict['isolation_1']['pin_1'], vibration_dict['isolation_1']['pin_2'])
        self.top_vibration1 = VibrationMotor(vibration_dict['top_1']['pwm'], vibration_dict['top_1']['pin_1'], vibration_dict['top_1']['pin_2'])
        self.imaging_vibration1 = VibrationMotor(vibration_dict['imaging_1']['pwm'], vibration_dict['imaging_1']['pin_1'], vibration_dict['imaging_1']['pin_2'])
        self.isolation_vibration2 = VibrationMotor(vibration_dict['isolation_2']['pwm'], vibration_dict['isolation_2']['pin_1'], vibration_dict['isolation_2']['pin_2'])
        GPIO.output(self.enable_pin, GPIO.HIGH)        

    def stop(self):
        self.isolation_vibration1.stop()
        self.top_vibration1.stop()
        self.imaging_vibration1.stop()
        self.isolation_vibration2.stop()
        GPIO.cleanup()

    def imagingVibrationPulse(self):
        self.imaging_vibration1.on()
        time.sleep(self.pulse_length)
        self.imaging_vibration1.off()

    def isolationVibrationPulse(self, ct=0):
        if ct == 1 or ct == 0:
            self.isolation_vibration1.on()
        if ct == 2 or ct == 0:
            self.isolation_vibration2.on()
        time.sleep(self.pulse_length)
        self.isolation_vibration1.off()
        self.isolation_vibration2.off()

    def topVibrationPulse(self):
        self.top_vibration1.on()
        time.sleep(self.pulse_length)
        self.top_vibration1.off()