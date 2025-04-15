import time
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import config
from w1thermsensor import W1ThermSensor
import RPi.GPIO as GPIO

# Initialize the button and sensor
button_pin = 17  # GPIO pin for the button (adjust as necessary)
sensor = W1ThermSensor()

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button input with pull-up

# MQTT setup
myMQTTClient = AWSIoTMQTTClient(config.CLIENT_ID)
myMQTTClient.configureEndpoint(config.AWS_HOST, config.AWS_PORT)
myMQTTClient.configureCredentials(config.AWS_ROOT_CA, config.AWS_PRIVATE_KEY, config.AWS_CLIENT_CERT)
myMQTTClient.configureConnectDisconnectTimeout(config.CONN_DISCONN_TIMEOUT)
myMQTTClient.configureMQTTOperationTimeout(config.MQTT_OPER_TIMEOUT)

# Connect to AWS IoT
try:
    myMQTTClient.connect()
    print("AWS connection succeeded")
except Exception as e:
    print(f"Connection failed: {e}")
    exit(1)

# Define the topic to publish data
topic = config.TOPIC

# User-defined callback function
def customCallback(client, userdata, message):
    print("Received a new message:")
    print(message.payload)
    print("from topic:")
    print(message.topic)
    print("--------------\n\n")

# Subscribe to the topic
myMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)

# main loop to collect data and publish to AWS IoT
try:
    while True:
        # read the temperature from the ds18b20 sensor
        temperature = sensor.get_temperature()
        print(f"Temperature: {temperature}°C")

        # read button state
        button_state = GPIO.input(button_pin)
        button_status = 1 if button_state == GPIO.LOW else 0  # 1 if pressed, 0 if released
        print(f"Button Status: {button_status}")

        # create a json payload
        payload = json.dumps({
            "temperature": temperature,
            "button_status": button_status
        })

        # publish to AWS IoT
        myMQTTClient.publish(topic, payload, 1)
        print(f"Published to topic {topic}: {payload}")

        # wait 10 sec before the next reading
        time.sleep(10)

# stop the program on keyboard interrupt
except KeyboardInterrupt:
    print("Program interrupted by user. Exiting...")
finally:
    # disconnect everything
    GPIO.cleanup()
    myMQTTClient.disconnect()
    print("Cleaned up and disconnected.")
