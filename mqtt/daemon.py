#!/usr/bin/python3
import paho.mqtt.client as mqtt
from parser.Parser import JsonParser
import requests
import logging
import urllib.parse

logging.basicConfig(level=logging.ERROR)


username = "UNINAPOLI"
passwd = "W1SUPER-UNI"
host = "mqtt.3maple.net"
topic = "application/6/#"
apy_key = "7eb1088964ba810f14e7ce7983ca7064"
id = '13'
emoncms_url= "parsec2.unicampania.it/emoncms/input/post.json?node="+id+"&apikey="+apy_key


def on_message(client, userdata, message):
    json_message = message.payload.decode("utf-8")
    logging.debug(json_message)
    parser = JsonParser(json_message)
    parser.parse()
    volume = parser.getCurVolume()
    epoch = parser.getCurTimeStamp()
    url = emoncms_url + "&json={volume:" + str(volume) + "}"
    logging.debug("http://"+url)
    r = requests.get("http://"+url)
    if r.status_code == 200:
        logging.debug("ok")
    else:
        logging.error(r.status_code)


def on_log(client, userdata, level, buf):
    print("log: ", buf)


if __name__ == '__main__':
    client = mqtt.Client()
    client.username_pw_set(username, password=passwd)
    client.on_message = on_message
    #client.on_log = on_log
    client.connect(host)
    logging.debug("connected")
    client.subscribe(topic)
    client.loop_forever()
