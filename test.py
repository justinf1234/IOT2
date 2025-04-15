import time
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import config
from w1thermsensor import W1ThermSensor
from gpiozero import Button

# Setup GPIO pin and sensor
button_pin = 17
sensor = W1ThermSensor()
button = Button(button_pin)

# Configure MQTT Client
myMQTTClient = AWSIoTMQTTClient(config.CLIENT_ID)
myMQTTClient.configureEndpoint(config.AWS_HOST, config.AWS_PORT)
myMQTTClient.configureCredentials(config.AWS_ROOT_CA, config.AWS_PRIVATE_KEY, config.AWS_CLIENT_CERT)
myMQTTClient.configureConnectDisconnectTimeout(config.CONN_DISCONN_TIMEOUT)
myMQTTClient.configureMQTTOperationTimeout(config.MQTT_OPER_TIMEOUT)

# Connect to AWS IoT Core
try:
    myMQTTClient.connect()
    print("AWS connection succeeded")
except Exception as e:
    print(f"Connection failed: {e}")
    exit(1)

# Define topic for MQTT
topic = config.TOPIC

# Callback function to handle incoming messages
def customCallback(client, userdata, message):
    print("Received a new message:")
    print(message.payload)
    print("from topic:")
    print(message.topic)
    print("--------------\n\n")

# Subscribe to the topic
myMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)  # Let subscription settle

# Main loop
try:
    while True:
        # Get temperature from the DS18B20 sensor
        temperature = sensor.get_temperature()
        print(f"Temperature: {temperature}°C")

        # Get button status (1 for pressed, 0 for not pressed)
        button_status = 1 if button.is_pressed else 0
        print(f"Button Status: {button_status}")

        # Create payload as a JSON object
        payload = json.dumps({
            "temperature": temperature,
            "button_status": button_status
        })

        # Publish payload to the topic
        myMQTTClient.publish(topic, payload, 1)
        print(f"Published to topic {topic}: {payload}")

        # Wait for next iteration
        time.sleep(10)

except KeyboardInterrupt:
    print("Program interrupted by user. Exiting...")
finally:
    # Cleanup and disconnect from AWS IoT Core
    myMQTTClient.disconnect()
    print("Cleaned up and disconnected.")
