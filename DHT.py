import time
import board
import adafruit_dht
from Adafruit_IO import Client, Feed

dhtDevice = adafruit_dht.DHT11(board.D24)
IO_USERNAME = "Ddoy"
IO_KEY = "aio_yUIJ069dQu9qP80Eie2fpLLZYhD1"

aio = Client(IO_USERNAME, IO_KEY)

temperature_feed = aio.feeds('temperature')
humidity_feed = aio.feeds('humidity')

while True:
	try:
		temperature_c = dhtDevice.temperature
		humidity = dhtDevice.humidity
		print("Temp: {:.1f} C  Humidity: {}%".format(temperature_c, humidity))
		aio.send(temperature_feed.key, str(temperature_c))
		aio.send(humidity_feed.key, str(humidity))
	except RuntimeError as error:
		print(error.args[0])
		time.sleep(1.0)
		continue
	except Exception as error:
		dhtDevice.exit()
		raise error
	except (KeyboardInterrupt, SystemExit):
		raise Exception("Program Closed")
	time.sleep(1.0)

