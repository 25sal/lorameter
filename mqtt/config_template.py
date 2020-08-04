import logging
logging.basicConfig(level=logging.DEBUG)
# username and password omitted for security reasons
username = ""
passwd = ""
# this is the mqtt host (default port 1883 is used)
broker = "mqtt.3maple.net"
# this is the topic to subscribe
topic = "application/6/#"
# this is the emoncms apikey write
api_key = ""
# this is the emoncms nodeid
id = '13'
# this is the emoncms host
emoncms_host = "parsec2.unicampania.it"