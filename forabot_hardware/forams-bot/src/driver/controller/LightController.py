from driver.motor.ForamsLight import ForamsLight

class LightController: # Define class for controlling ring light
    def __init__(self,light_dict): # Define constructor that initializes from ForamsLight light dict
        self.neopixel = ForamsLight(light_dict['neopixel']['total_led'], light_dict['neopixel']['board_pin'], light_dict['neopixel']['pixel_order'])

    def lightForam(self, idx): # Turns on light and loops through number of lights per image
        self.neopixel.setLightsBase() # Turn on base light of neopixel  
        for i in range(self.lights_per_img): # Loop through number of lights per image
            j = (self.light_steps*idx) + i # Calc current light step index
            self.neopixel.directionalLight(j) # light up the neopixel in the given direction

    def lightsOff(self): # Turn off neopixel
        self.neopixel.lightsOff()

    def setRunParams(self, lights_per_img, light_steps): # This is how you set the neopixel parameters
        self.lights_per_img = lights_per_img 
        self.light_steps = light_steps
