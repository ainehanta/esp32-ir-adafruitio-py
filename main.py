import time
import os
import ujson as json

import machine
from umqtt.simple import MQTTClient
import IRaeha

ir_tx = IRaeha.Transmitter(pin=25)

def sub_cb(topic, msg):
    print((topic, msg))
    action = json.loads(msg)
    if action['type'] == 'ceiling-sw':
	    ir_tx.send([0x34, 0x4A, 0x90, 0x0C, 0x9C])
	    time.sleep(1)

def main():
    c = MQTTClient("ユーザー名", "io.adafruit.com", user="ユーザー名", password="アクセスキー", ssl=True)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(b"ユーザー名/feeds/フィード名")

    def check_msg():
        try:
            c.check_msg()
        except OSError:
            print("ENOENT")
            machine.reset()

    epoch = 0
    prev_epoch = 0
    while True:
        epoch = time.time()
        if epoch != prev_epoch:
            if epoch % 1 == 0:
                check_msg()
        prev_epoch = epoch

if __name__ == "__main__":
    main()
