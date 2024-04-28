class Config():
    ENV = 'development'
    SECRET_KEY = 'SUPER SECRETO'
    MQTT_BROKER_URL = 'c1efe023.ala.dedicated.aws.emqxcloud.com'
    MQTT_BROKER_PORT = 1883
    MQTT_USERNAME = 'mqttpy'  # Set this item when you need to verify username and password
    MQTT_PASSWORD = 'public'  # Set this item when you need to verify username and password
    MQTT_KEEPALIVE = 60  # Set KeepAlive time in seconds
    MQTT_TLS_ENABLED = False # If your server supports TLS, set it True