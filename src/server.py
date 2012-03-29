#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import serial
import threading
from threading import Timer, Thread
from signal import signal, SIGINT
import time
from math import *

import config as cfg


#coordinates = [[[[0., 0.]] * 2] * 3] * 4
#angles      = [[[[0., 0.]] * 2] * 3] * 4

coordinates = [[[[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]]],
               [[[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]]],
               [[[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]]],
               [[[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]]]]
angles      = [[[[0., 0., 0.], [0., 0., 0.]], [[0., 0., 0.], [0., 0., 0.]], [[0., 0., 0.], [0., 0., 0.]]],
               [[[0., 0., 0.], [0., 0., 0.]], [[0., 0., 0.], [0., 0., 0.]], [[0., 0., 0.], [0., 0., 0.]]],
               [[[0., 0., 0.], [0., 0., 0.]], [[0., 0., 0.], [0., 0., 0.]], [[0., 0., 0.], [0., 0., 0.]]],
               [[[0., 0., 0.], [0., 0., 0.]], [[0., 0., 0.], [0., 0., 0.]], [[0., 0., 0.], [0., 0., 0.]]]]

desiredAngles = [0, 0, 0]   # Desired shoulder, elbow, and wrist angles, as bytes.


def setupAngles():
    for d in range(4):
        for i in range(3):
            for j in range(2):
                # Calculate coordinates.
                coordinates[d][i][j][0] = cfg.origin[0] + (d+j)*cfg.segmentLen + (d+d/2)*cfg.separation
                coordinates[d][i][j][1] = cfg.origin[1] + i*cfg.segmentLen

                # Calculate servo angles (in degrees) necessary to reach the coordinate point.
                c = sqrt(coordinates[d][i][j][0]**2 + coordinates[d][i][j][1]**2)
                try:
                    angles[d][i][j][1] = cfg.elbowZero + acos(((cfg.upperArmLen**2 + cfg.lowerArmLen**2) - c**2)/(2 * cfg.upperArmLen * cfg.lowerArmLen))
                    angles[d][i][j][0] = cfg.shoulderZero + asin(cfg.lowerArmLen/c * sin(angles[d][i][j][1])) + atan(coordinates[d][i][j][1]/coordinates[d][i][j][0]) - pi/2
                except ValueError as e:
                    print("Error:", e)

                # Convert to degrees
                #angles[d][i][j][0] *= 180/pi
                #angles[d][i][j][1] *= 180/pi

                print("Values for", d, i, j, ":", coordinates[d][i][j], c, angles[d][i][j])


# Convert angles of [0.0, pi] to [0, 250] so we can send them over serial as
# bytes.
def angle2byte(angle):
    twoBytes = int(angle * 0x3fff/pi)
    return chr(twoBytes & 0x7f) + chr(twoBytes >> 7)


# =============================================================================
# Drawing functions.
# =============================================================================
def draw(position, digit):
    global desiredAngles
    for point in cfg.numbers[digit]:
        angles[position][point[0]][point[1]][2] = 0
        desiredAngles = angles[position][point[0]][point[1]]
        transmit()
        time.sleep(cfg.drawSpeed)
        if cfg.debug:
            print("Writing", digit, "at position", position, ". Servo angles:", desiredAngles, "  Sending bytes:", angle2byte(desiredAngles[0]), angle2byte(desiredAngles[1]), angle2byte(desiredAngles[2]))


# =============================================================================
# Communicate.
# =============================================================================
def transmit():
    global desiredAngles
    serWrite(cfg.serHeader +
             angle2byte(desiredAngles[0]) +
             angle2byte(desiredAngles[1]) +
             angle2byte(desiredAngles[2]))

# Serial write.
def serWrite(myStr):
    global ser
    try:
        for i in range(len(myStr)):
            ser.write(myStr[i])
    except NameError:
        print("asdfasdfasdf")
    except:
        print("[GS] Unable to send data. Check connection.")
        # TODO: Comm should do something to ensure safety when it loses connection.


def initSerial():
    global ser
    try:
        ser = serial.Serial(cfg.serialPort, cfg.baudRate, timeout=0)
    except serial.SerialException:
        print("[GS] Unable to open specified serial port! Exiting...")
        #exit(1)
    except AttributeError:
        for i in range(4):
            try:
                ser = serial.Serial("/dev/ttyUSB"+str(i), cfg.baudRate, timeout=0)
                print("[GS] Opened serial port at /dev/ttyUSB%d." % i)
                break
            except serial.SerialException:
                print("[GS] No serial at /dev/ttyUSB%d." % i)
                if i == 3:
                    print("[GS] No serial found. Giving up!")
                    exit(1)


class ScribblerTX(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.times = 0
    def run(self):
        while self.running:
            transmit()
            self.times += 1
            time.sleep(cfg.dataSendInterval)


###############################################################################

if __name__ == "__main__":
    # =========================================================================
    # Try to initialize a serial connection. If serialPort is defined, try
    # opening that. If it is not defined, loop through a range of integers
    # starting from 0 and try to connect to /dev/ttyUSBX where X is the
    # integer. In either case, process dies if serial port cannot be opened.
    #
    # TODO: This needs to be made more concise.
    # =========================================================================
    initSerial()

    setupAngles()

    draw(0, 9)
    draw(1, 5)
    draw(2, 5)

    tx = ScribblerTX()
    tx.start()

    # Stop the while loops.
    tx.running = False

    # Wait for threads to finish jobs.
    tx.join()


