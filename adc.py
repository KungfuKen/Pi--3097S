import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)
# create an analog input channel on pin 1
chan1 = AnalogIn(mcp, MCP.P1)

def button_callback(channel):
    print("Button was pushed!")

GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(24,GPIO.RISING,callback=button_callback)
GPIO.setwarnings(False)

print('Raw ADC Value Thermistor: ', chan0.value)
print('ADC Voltage: ' + str(chan0.voltage) + 'V')
while True:
	print('Raw ADC Value LDR: ', chan1.value)
	print('ADC Voltage: ' + str(chan1.voltage*40) + 'lux')

message = input("Press enter to quit\n\n")

GPIO.cleanup()
