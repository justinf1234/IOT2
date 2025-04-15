# AWS general configuration
AWS_PORT = 8883
AWS_HOST = 'anly5ghm643s-ats.iot.us-east-1.amazonaws.com' 
AWS_ROOT_CA = 'certs/aws_root.pem'
AWS_CLIENT_CERT = 'certs/aws_client.crt'
AWS_PRIVATE_KEY = 'certs/aws_private.key'

################## Subscribe / Publish client #################
CLIENT_ID = 'fromPi'  
TOPIC = 'justin/device/raspberry/data' 
OFFLINE_QUEUE_SIZE = -1
DRAINING_FREQ = 2
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5
