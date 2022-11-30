from driver.motor.ForamsLight import ForamsLight

class LightController:
    def __init__(self,light_dict):
        self.neopixel = ForamsLight(light_dict['neopixel']['total_led'], light_dict['neopixel']['board_pin'], light_dict['neopixel']['pixel_order'])

    def lightForam(self, idx):
        self.neopixel.setLightsBase()
        for i in range(self.lights_per_img):
            j = (self.light_steps*idx) + i
            self.neopixel.directionalLight(j)

    def lightsOff(self):
        self.neopixel.lightsOff()

    def setRunParams(self, lights_per_img, light_steps):
        self.lights_per_img = lights_per_img
        self.light_steps = light_steps
