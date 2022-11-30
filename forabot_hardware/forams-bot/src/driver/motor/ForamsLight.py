import board
import neopixel
import time

class ForamsLight:
    def __init__(self, total_led, board_pin, pixel_order):
        self.total_led = total_led
        self.board_pin = getattr(board, "D" + str(board_pin))
        if pixel_order == 'RGB':
            self.red_tup = (255,0,0)
            self.green_tup = (0,255,0)
            self.blue_tup = (0,0,255)
            self.off_tup = (0,0,0)
        elif pixel_order == 'RGBW':
            self.red_tup = (255,0,0,0)
            self.green_tup = (0,255,0,0)
            self.blue_tup = (0,0,255,0)
            self.off_tup = (0,0,0,0)
        else:
            raise Exception('Configured pixel_order must be either RGB or RGBW')
        self.ring = neopixel.NeoPixel(self.board_pin, self.total_led, auto_write=False, pixel_order=pixel_order)
        self.lightsOff()

    def directionalLight(self, idx):
        self.ring[idx] = self.red_tup
        self.ring[8+idx] = self.green_tup
        self.ring[16+idx] = self.blue_tup
        self.ring.show()
        time.sleep(0.35)

    def setLightsBase(self):
        self.ring.fill(self.off_tup)
        self.ring.show()
        time.sleep(0.1)

    def lightsOff(self):
        self.ring.fill(self.off_tup)
        self.ring.show()
