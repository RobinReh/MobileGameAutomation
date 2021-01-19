from ppadb.client import Client
from PIL import Image
import numpy
import time

debug = False
debugPath = False
platformY = 810
targetColor = {'red': 247, 'green': 27, 'blue': 27}
berryY = 838
red = [{'red': 225, 'green': 14, 'blue': 12},
       {'red': 241, 'green': 51, 'blue': 49}]
client = Client(host='127.0.0.1', port=5037)
# print(client.version())

foundDevices = client.devices()


if len(foundDevices) == 0:
    print('Unable to find device')
    quit()

device = foundDevices[0]
# device.shell('input touchscreen swipe 500 0 500 1000 1000')
while True:
    screen = device.screencap()
    with open("screen.png", "wb") as pic:
        pic.write(screen)

    image = Image.open('screen.png')
    image = numpy.array(image, dtype=numpy.uint8)
    platformRow = [list(i[:3]) for i in image[platformY]]

    if debug:
        print(platformRow)

    path = []
    foundStart = False
    firstBlack = False
    for i, pixel in enumerate(platformRow):
        r, g, b = [int(i) for i in pixel]

        if not firstBlack and (r+g+b) == 0:
            firstBlack = True
            if debugPath:
                print('Found black')

        if not foundStart and firstBlack and (r+g+b) != 0:
            path.append(i-10)
            foundStart = True
            if debugPath:
                print('Added black')

        if r == targetColor['red'] and g == targetColor['green'] and b == targetColor['blue']:
            path.append(i+10)
            if debugPath:
                print('Added red')
            break

    distance = path[1] - path[0]
    pushTime = ((path[1] - path[0])/0.66375)-25
    device.shell(f'input touchscreen swipe 300 300 300 300 {int(pushTime)}')
    if debug:
        print('Distance:', distance)
    print('Start:', path[0], 'End:', path[1])
    time.sleep(3)
