import time
from rpi_ws281x import PixelStrip, Color

LED_COUNT = 8
LED_PIN = 18
LED_FREQ_HZ = 800000  
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0  

left_line = [0,1,2,3]
right_line = [4,5,6,7]

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def led_control(state):
	print(state)
	if state :
		print(state)
		current_left = Color(0,255,0)
		current_right = Color(0,0,0)
	else:
		print(state)
		current_left = Color(255,0,0)
		current_right = Color(255,0,0)

	for i in range(strip.numPixels()):
		if i in left_line:
			strip.setPixelColor(i, current_left)
		elif i in right_line:
			strip.setPixelColor(i, current_right)
		
	strip.show()
