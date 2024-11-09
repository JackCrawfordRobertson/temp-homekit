import adafruit_dht
import board
import time

# Set up the DHT11 sensor on the GPIO pin you used
# Update 'D4' to your specific pin if different
dht_device = adafruit_dht.DHT11(board.D4)  # GPIO4 as Data pin; replace if using another GPIO

while True:
    try:
        # Read temperature and humidity
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        
        # Print the results
        if temperature is not None and humidity is not None:
            print(f"Temperature: {temperature}°C, Humidity: {humidity}%")
        
    except RuntimeError as error:
        # Handle occasional read errors from the DHT11
        print(error.args[0])
    
    # Wait before reading again
    time.sleep(2)
