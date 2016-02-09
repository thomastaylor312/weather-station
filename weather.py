#!/usr/bin/python3
import sys
import time
import threading
from sense_hat import SenseHat
from evdev import InputDevice, list_devices, ecodes

sense = SenseHat()

# Make sure we can find the joystick
found = False;
devices = [InputDevice(fn) for fn in list_devices()]
for dev in devices:
    if dev.name == 'Raspberry Pi Sense HAT Joystick':
        found = True;
        break

if not(found):
    print('Raspberry Pi Sense HAT Joystick not found. Aborting ...')
    sys.exit()

# Function to display the cool rainbow effect
def display_rainbow(stopper):
    # Clear things to start
    sense.clear()
    pixels = [
        [255, 0, 0], [255, 0, 0], [255, 87, 0], [255, 196, 0], [205, 255, 0], [95, 255, 0], [0, 255, 13], [0, 255, 122],
        [255, 0, 0], [255, 96, 0], [255, 205, 0], [196, 255, 0], [87, 255, 0], [0, 255, 22], [0, 255, 131], [0, 255, 240],
        [255, 105, 0], [255, 214, 0], [187, 255, 0], [78, 255, 0], [0, 255, 30], [0, 255, 140], [0, 255, 248], [0, 152, 255],
        [255, 223, 0], [178, 255, 0], [70, 255, 0], [0, 255, 40], [0, 255, 148], [0, 253, 255], [0, 144, 255], [0, 34, 255],
        [170, 255, 0], [61, 255, 0], [0, 255, 48], [0, 255, 157], [0, 243, 255], [0, 134, 255], [0, 26, 255], [83, 0, 255],
        [52, 255, 0], [0, 255, 57], [0, 255, 166], [0, 235, 255], [0, 126, 255], [0, 17, 255], [92, 0, 255], [201, 0, 255],
        [0, 255, 66], [0, 255, 174], [0, 226, 255], [0, 117, 255], [0, 8, 255], [100, 0, 255], [210, 0, 255], [255, 0, 192],
        [0, 255, 183], [0, 217, 255], [0, 109, 255], [0, 0, 255], [110, 0, 255], [218, 0, 255], [255, 0, 183], [255, 0, 74]
    ]

    def next_colour(pix):
        r = pix[0]
        g = pix[1]
        b = pix[2]

        if (r == 255 and g < 255 and b == 0):
            g += 1

        if (g == 255 and r > 0 and b == 0):
            r -= 1

        if (g == 255 and b < 255 and r == 0):
            b += 1

        if (b == 255 and g > 0 and r == 0):
            g -= 1

        if (b == 255 and r < 255 and g == 0):
            r += 1

        if (r == 255 and b > 0 and g == 0):
            b -= 1

        pix[0] = r
        pix[1] = g
        pix[2] = b

    while not stopper.is_set():
        for pix in pixels:
            next_colour(pix)

        sense.set_pixels(pixels)
        stopper.wait(2/1000.0)
        pass

# Function for getting temperature
def display_temperature(stopper):
    sense.clear()
    while not stopper.is_set():
        sense.show_message('%.2f' % sense.get_temperature(), .1, (0, 0, 255))
        stopper.wait(5)
        pass

# Function for getting pressure
def display_pressure(stopper):
    sense.clear()
    while not stopper.is_set():
        sense.show_message('%.2f' % sense.get_pressure(), .1, (0, 0, 255))
        stopper.wait(5)
        pass

# Function for getting humidity
def display_humidity(stopper):
    sense.clear()
    while not stopper.is_set():
        sense.show_message('%.2f' % sense.get_humidity(), .1, (0, 0, 255))
        stopper.wait(5)
        pass
    
actions = [
    lambda x: threading.Thread(target=display_rainbow, args=(x,)),
    lambda x: threading.Thread(target=display_temperature, args=(x,)),
    lambda x: threading.Thread(target=display_pressure, args=(x,)),
    lambda x: threading.Thread(target=display_humidity, args=(x,))
]

# Main event loop
try:
    current_item = 0
    # Start on the default
    current_stopper = threading.Event()
    current_thread = actions[0](current_stopper)
    current_thread.start()
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY and event.value == 1:
            was_triggered = False
            if event.code == ecodes.KEY_DOWN:
                # Go to the thing before
                if current_item == 0:
                    current_item = len(actions) - 1
                else:
                    current_item -= 1
                was_triggered = True
            elif event.code == ecodes.KEY_UP:
                # Go to the next thing
                if current_item == len(actions) - 1:
                    current_item = 0
                else:
                    current_item += 1
                was_triggered = True
            # Take care of stopping the old thread and starting a new one
            if was_triggered:
                current_stopper.set()
                current_thread.join()
                current_stopper = threading.Event()
                current_thread = actions[current_item](current_stopper)
                current_thread.start()
except KeyboardInterrupt:
    current_stopper.set()
    current_thread.join()
    sense.clear()
    sys.exit()