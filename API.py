import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import adafruit_dht
from Adafruit_IO import Client, Feed

class SetUp:
	def __init__(self, dhtDevice, IO_USERNAME, IO_KEY, aio):
		self.dhtDevice = dhtDevice
		self.IO_USERNAME = IO_USERNAME
		self.IO_KEY = IO_KEY
		self.aio = aio

class SetFeed:
	def __init__(self, temperature_feed, humidity_feed, light_feed):
		self.temperature_feed = temperature_feed
		self.humidity_feed = humidity_feed
		self.light_feed = light_feed

class ReadAndSend:
	def __init__(self):
		pass

	def readAndSend(self):
		newSetUp = SetUp(adafruit_dht.DHT11(board.D24), "Ddoy", "aio_OqZD42C9OM09r2wiYNAVoyK1K9yC", Client("Ddoy", "aio_OqZD42C9OM09r2wiYNAVoyK1K9yC"))
		newFeed = SetFeed(newSetUp.aio.feeds('temperature'), newSetUp.aio.feeds('humidity'), newSetUp.aio.feeds('light'))
		spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
		cs = digitalio.DigitalInOut(board.D22)
		mcp = MCP.MCP3008(spi, cs)
		chan1 = AnalogIn(mcp, MCP.P1)
		while True:
			try:
				temperature = newSetUp.dhtDevice.temperature
				humidity = newSetUp.dhtDevice.humidity
				light = chan1.voltage*40
				print("Light level: " + str(light) + " lux")
				print("Temp: {:.1f} C  Humidity: {}%".format(temperature, humidity))
				newSetUp.aio.send(newFeed.temperature_feed.key, str(temperature))
				newSetUp.aio.send(newFeed.humidity_feed.key, str(humidity))
				newSetUp.aio.send(newFeed.light_feed.key, str(light))
			except RuntimeError as error:
				print(error.args[0])
				time.sleep(0.5)
				continue
			except Exception as error:
				raise error
			except (KeyboardInterrupt, SystemExit):
				interrupt()
			time.sleep(0.5)

	def exceptionError(self):
		raise error
	def interrupt(self):
		raise Exception("Program Closed")

newRead = ReadAndSend()
newRead.readAndSend()

