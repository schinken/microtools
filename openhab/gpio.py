#!/usr/bin/python2

import sys
import time
import logging
import requests
import threading
import Queue
import RPi.GPIO as GPIO
from collections import defaultdict

DEBOUNCE_TIME = 25

mapping = {
    3:  { 'name': 'pc_oven', 'pull_up_down': GPIO.PUD_UP },
    4:  { 'name': 'pc_powersockets', 'pull_up_down': GPIO.PUD_UP }, 
    17: { 'name': 'pc_storage_light', 'pull_up_down': GPIO.PUD_DOWN },
    27: { 'name': 'pc_kitchen_light', 'pull_up_down': GPIO.PUD_DOWN }
}

openhab_url = 'http://openhab:8080/rest/items'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AsyncRestActor(threading.Thread):

    def __init__(self):
        super(AsyncRestActor, self).__init__()
        self.queue = Queue.Queue()

        self.setDaemon(True)
        self.start()

    def toggle(self, item):
        self.queue.put(item)

    def run(self):

        while True:
            item = self.queue.get()
            openhab_device = openhab_url + '/' + item

            try:
                current_state = requests.get(openhab_device + '/state').content

                logger.debug("Current state for %s is %s" % (item, current_state))

                send = 'ON'
                if current_state == 'ON':
                    send = 'OFF'

                logger.info("Switching %s to %s" % (item, send))

                requests.post(openhab_device, data=send, headers={
                    'Content-type': 'text/plain'
                })

                logger.debug("Switched %s" % (item,))


            except Exception as e:
                logger.error(e)


            self.queue.task_done()


rest_actor = AsyncRestActor()

GPIO.setmode(GPIO.BCM)

def get_current_ms():
    return int(round(time.time() * 1000))

debounce = defaultdict(int)

def pin_change(pin):

    entry = mapping[pin]
    state = GPIO.input(pin)
    ms = get_current_ms()

    logger.info("Pin changed triggered on %s (%d) to %d" % (mapping[pin]['name'], pin, state))

    if (entry['pull_up_down'] == GPIO.PUD_UP and state == GPIO.LOW) or \
       (entry['pull_up_down'] == GPIO.PUD_DOWN and state == GPIO.HIGH): 
        debounce[pin] = ms
        logger.debug("Remembering time for pin %d - %d ms" % (pin, ms))

    elif (entry['pull_up_down'] == GPIO.PUD_UP and state == GPIO.HIGH) or \
         (entry['pull_up_down'] == GPIO.PUD_DOWN and state == GPIO.LOW): 

        if not pin in debounce:
            logger.debug("No previous debounce entry present for pin %d" % (pin,))
            return False

        last_ms = debounce[pin]

        # Remove key to avoid false values
	del debounce[pin]

        if ms-last_ms < DEBOUNCE_TIME:
            logger.debug("Time below debounce time. Expected < %d, actual %d ms" % (DEBOUNCE_TIME, ms-last_ms))
            return False

        rest_actor.toggle(mapping[pin]['name'])

for _, pin in enumerate(mapping):
    entry = mapping[pin]

    logger.info("Setting up callback for pin %s (%d)" % (entry['name'], pin))
    GPIO.setup(pin, GPIO.IN, pull_up_down=entry['pull_up_down'])
    GPIO.add_event_detect(pin, GPIO.BOTH, callback=pin_change)


while True:
    time.sleep(1)
