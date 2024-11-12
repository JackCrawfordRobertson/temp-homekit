import adafruit_dht
import board
import time
import logging
import qrcode
from pyhap.accessory import Accessory
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import CATEGORY_BRIDGE  # or CATEGORY_OTHER
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set up the DHT11 sensor
dht_device = adafruit_dht.DHT11(board.D4)  # Update GPIO pin if needed

class TemperatureHumiditySensor(Accessory):
    category = CATEGORY_BRIDGE  # or CATEGORY_OTHER


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("Initialising Temperature and Humidity sensor accessory")

        # Add separate services for temperature and humidity
        temp_service = self.add_preload_service('TemperatureSensor')
        hum_service = self.add_preload_service('HumiditySensor')
        
        # Get characteristics for temperature
        self.temp_char = temp_service.get_characteristic('CurrentTemperature')
        
        # Get characteristics for humidity
        self.hum_char = hum_service.get_characteristic('CurrentRelativeHumidity')

    def update_sensor_data(self):
        """Read the sensor and update HomeKit values."""
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            if temperature is not None and humidity is not None:
                logger.info(f"Temperature: {temperature}°C, Humidity: {humidity}%")
                self.temp_char.set_value(temperature)
                self.hum_char.set_value(humidity)
            else:
                logger.warning("Temperature or humidity reading is None")

        except RuntimeError as e:
            logger.error(f"Sensor read error: {e}")

    def run(self):
        """Periodically update sensor readings and refresh HomeKit."""
        while True:
            logger.info("Updating sensor data")
            self.update_sensor_data()
            time.sleep(60)  # Update every 60 seconds

def generate_qr_code(pairing_code):
    # Encode the pairing code into a HomeKit-compatible QR code
    qr_code_data = f"X-HM://{pairing_code.replace('-', '')}"
    qr = qrcode.make(qr_code_data)
    qr.show()  # Display the QR code
    qr.save("homekit_qr_code.png")  # Save it as an image file
    logger.info("QR code for HomeKit pairing saved as 'homekit_qr_code.png'")

def main():
    # Log when the server is starting
    logger.info("Starting HomeKit accessory server")
    
    # Set up the pairing code (default format '031-45-154')
    pairing_code = '031-45-154'
    logger.info(f"HomeKit pairing code: {pairing_code}")

    # Generate the QR code for pairing
    generate_qr_code(pairing_code)

    # Initialise the driver with the pairing code (converted to bytes)
    driver = AccessoryDriver(port=51826, pincode=pairing_code.encode())

    # Log accessory setup
    sensor = TemperatureHumiditySensor(driver, 'Room Sensor')
    driver.add_accessory(accessory=sensor)
    logger.info("Added accessory: TemperatureHumiditySensor")

    # Start the driver and log
    try:
        logger.info("Starting the accessory driver")
        driver.start()
    except KeyboardInterrupt:
        driver.stop()
        logger.info("Accessory driver stopped")

if __name__ == '__main__':
    main()
