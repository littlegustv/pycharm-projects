__author__ = 'littlegustv'

import ImageGrab
import os
import time

def screenGrab():
    box = (700,100,1200,800)
    im = ImageGrab.grab()
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')

def main():
    screenGrab()

if __name__ == '__main__':
    main()