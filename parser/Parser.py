import json
import base64
import logging
import struct
import time


class JsonParser:
    message = None
    hex_data = None

    def __init__(self, json_message):
        self.message = json_message

    def parse(self):
        json_obj = json.loads(self.message)
        if "data" in json_obj.keys():
            lora_payload = json_obj["data"]
            logging.debug(lora_payload)
            self.hex_data = self.getLoraBytes(lora_payload)

    @staticmethod         
    def getLoraBytes(lora_payload):        
            hex_data = base64.b64decode(lora_payload)
            hex_str = ''
            for i in range(len(hex_data)):
                hex_str+=hex(hex_data[i])
            logging.debug(hex_str)
            return hex_data

    def getCurEpoch(self):
        if self.hex_data is None:
            self.parse()
        epoch = struct.unpack('<I', self.hex_data[1:5])
        return epoch[0]

    def getCurTimeStamp(self):
        if self.hex_data is None:
            self.parse()
        epoch = struct.unpack('<I', self.hex_data[1:5])
        datetime = time.strftime('%Y-%m-%dT%H:%M:%S %Z', time.localtime(epoch[0]))
        logging.debug(datetime)
        return datetime

    def getStatus(self):
        if self.hex_data is None:
            self.parse()
        status = hex(self.hex_data[5])
        logging.debug(status)
        return status

    def getCurVolume(self):
        if self.hex_data is None:
            self.parse()
        current_volume = struct.unpack('<I', self.hex_data[6:10])
        logging.debug(current_volume)
        return current_volume[0]


if __name__ == '__main__':
    message = '{"applicationID":"6","applicationName":"W1-TEST","deviceName":"W1-special",' \
              '"devEUI":"00070900004fd599","rxInfo":[{"gatewayID":"313532354a006800",' \
              '"uplinkID":"2a61d10f-a5e0-47f0-b605-c37bbda6a9b8","name":"Wap-LoRa-WiFi","rssi":-99,' \
              '"loRaSNR":9.75,"location":{"latitude":0,"longitude":0,"altitude":0}}],' \
              '"txInfo":{"frequency":868100000,"dr":5},"adr":true,"fCnt":21824,"fPort":100,' \
              '"data":"AddrKF8AxwEAAAAABCAAAAAAAACQCeQDBIAFAAFIAAeAAwAABAABAADAAFQAAEAAAAAA"}'
    parser = JsonParser(message)
    print(parser.getCurTimeStamp())
    print(parser.getCurVolume())
