import time
import board
import adafruit_dht
from Adafruit_IO import Client, Feed

class SetUp:
	def __init__(self, dhtDevice, IO_USERNAME, IO_KEY, aio):
		self.dhtDevice = dhtDevice
		self.IO_USERNAME = IO_USERNAME
		self.IO_KEY = IO_KEY
		self.aio = aio

class SetFeed:
	def __init__(self, temperature_feed, humidity_feed):
		self.temperature_feed = temperature_feed
		self.humidity_feed = humidity_feed

class ReadAndSend:
	def __init__(self):
		pass

	def readAndSend(self):
		newSetUp = SetUp(adafruit_dht.DHT11(board.D24), "Ddoy", "aio_AXLV57Ynf0Qw5HZ0Vk1dGNSxrJp2", Client("Ddoy", "aio_AXLV57Ynf0Qw5HZ0Vk1dGNSxrJp2"))
		newFeed = SetFeed(newSetUp.aio.feeds('temperature'), newSetUp.aio.feeds('humidity'))
		while True:
			try:
				temperature = newSetUp.dhtDevice.temperature
				humidity = newSetUp.dhtDevice.humidity
				print("Temp: {:.1f} C  Humidity: {}%".format(temperature, humidity))
				newSetUp.aio.send(newFeed.temperature_feed.key, str(temperature))
				newSetUp.aio.send(newFeed.humidity_feed.key, str(humidity))
			except RuntimeError as error:
				print(error.args[0])
				time.sleep(1.0)
				continue
			except Exception as error:
				exceptionError()
			except (KeyboardInterrupt, SystemExit):
				interrupt()
			time.sleep(1.0)

	def exceptionError(self):
		dhtDevice.exit()
		raise error
	def interrupt(self):
		raise Exception("Program Closed")

newRead = ReadAndSend()
newRead.readAndSend()
