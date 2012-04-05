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

# Cartesian coordinates in [X, Y], points in number grid in [row, col].
coordinates = [[[[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]]],
               [[[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]]],
               [[[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]]],
               [[[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]]]]
angles      = [[[[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]]],
               [[[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]]],
               [[[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]]],
               [[[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]], [[0., 0.], [0., 0.]]]]

desiredAngles = [0, 0, 0]   # Desired shoulder, elbow, and wrist angles, as bytes.


def positionToAngles(position):
    angles = [0., 0.]

    # Calculate servo angles (in radians) necessary to reach the coordinate point.
    c = sqrt(position[0]**2 + position[1]**2)

    # Calculate elbow angle, then calculate shoulder angle depending on elbow angle.
    angles[1] = cfg.elbowZero - acos(((cfg.upperArmLen**2 + cfg.lowerArmLen**2) - c**2)/(2 * cfg.upperArmLen * cfg.lowerArmLen))
    angles[0] = cfg.shoulderZero - asin(cfg.lowerArmLen/c * sin(angles[1])) + atan(position[1]/position[0])

    return angles

def setupAngles():
    global coordinates, angles
    for d in range(4):
        for row in range(3):
            for col in range(2):
                # Calculate coordinates.
                coordinates[d][row][col][1] = cfg.origin[0] + (d+col)*cfg.segmentLen + (d+d/2)*cfg.separation
                coordinates[d][row][col][0] = cfg.origin[1] + row*cfg.segmentLen

                try:
                    angles[d][row][col] = positionToAngles(coordinates[d][row][col])
                except ValueError as e:
                    print("Error:", e)

                print("Values for", d, row, col, ":", coordinates[d][row][col], angles[d][row][col])


# Convert angles of [0.0, pi] to [0, 0x3fff] so we can send them over serial as
# bytes.
def angle2byte(angle):
    twoBytes = int(angle * 0x3fff/pi)
    return chr(twoBytes & 0x7f) + chr(twoBytes >> 7)


# =============================================================================
# Drawing functions.
# =============================================================================
def zero():
    global desiredAngles
    desiredAngles[0] = cfg.shoulderZero + 1.6
    desiredAngles[2] = cfg.wristZero

    desiredAngles[1] = cfg.elbowZero - 0.1
    transmit(1)

    desiredAngles[1] = cfg.elbowZero
    transmit(1)

    time.sleep(cfg.zeroDelay)   # Wait until pen is in cap.

    transmit(0)

# Move arm to position with stepsize defined in config file. If wristPos ==
# wristZero, stepsize == 0.
def moveToPoint(position, wristPos):
    global desiredAngles
    desiredAngles[2] = wristPos

    if wristPos == cfg.wristZero:
        desiredAngles[:2] = positionToAngles(position)
        transmit(1)


def drawDigit(position, digit):
    global desiredAngles
    desiredAngles[2] = cfg.wristZero   # Start with wrist in zero position.
    desiredAngles[:2] = angles[position][cfg.numbers[digit][0][0]][cfg.numbers[digit][0][1]]
    transmit(1)
    desiredAngles[2] = cfg.wristPen
    transmit(1)

    for point in cfg.numbers[digit]:
        desiredAngles[:2] = angles[position][point[0]][point[1]]
        transmit(1)
        time.sleep(cfg.drawSpeed)
        if cfg.debug:
            print("Writing", digit, "at position", position, ". Servo angles:", desiredAngles, "  Sending bytes:", angle2byte(desiredAngles[0]), angle2byte(desiredAngles[1]), angle2byte(desiredAngles[2]))


# =============================================================================
# Communicate.
# =============================================================================
def transmit(power):
    global desiredAngles
    serWrite(cfg.serHeader +
             angle2byte(desiredAngles[0]) +
             angle2byte(desiredAngles[1]) +
             angle2byte(desiredAngles[2]) +
             chr(power))
    time.sleep(cfg.drawDelay)

# Serial write.
def serWrite(myStr):
    global ser
    try:
        for i in range(len(myStr)):
            ser.write(myStr[i])
    except NameError:
        print("serWrite NameError!")
    except:
        print("[GS] Unable to send data. Check connection.")
        # TODO: Comm should do something to ensure safety when it loses connection.


# =============================================================================
# Try to initialize a serial connection. If serialPort is defined, try
# opening that. If it is not defined, loop through a range of integers
# starting from 0 and try to connect to /dev/ttyUSBX where X is the
# integer. In either case, process dies if serial port cannot be opened.
#
# TODO: This needs to be made more concise.
# =============================================================================
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
            self.times += 1
            time.sleep(cfg.drawDelay)


###############################################################################

if __name__ == "__main__":
    initSerial()

    setupAngles()

    zero()

    #drawDigit(0, 1)
    #drawDigit(1, 5)
    #drawDigit(2, 5)

    while True:
        coordInput = raw_input("Coordinates:")

        if coordInput == 'x':
            break
        elif coordInput == 'z':
            zero()
        elif coordInput == 'w':
            desiredAngles[2] = cfg.wristZero
            transmit(1)
        elif coordInput == '955':
            drawDigit(0, 9)
            drawDigit(1, 5)
            drawDigit(2, 5)
        elif coordInput == 't':
            for d in range(4):
                for row in range(3):
                    for col in range(2):
                        desiredAngles[2] = cfg.wristPen
                        desiredAngles[:2] = angles[d][row][col]
                        transmit(1)
                        print("Position:", d, "Servo angles:", desiredAngles, "  Sending bytes:", angle2byte(desiredAngles[0]), angle2byte(desiredAngles[1]), angle2byte(desiredAngles[2]))
        else:
            coordProcessed = [0., 0.]
            for i in range(len(coordInput.split())):
                coordProcessed[i] = float(coordInput.split()[i])
            print coordProcessed

            moveToPoint(coordProcessed, cfg.wristZero)

    desiredAngles[2] = cfg.wristZero
    zero()

    #transmit(0)

    #tx = ScribblerTX()
    #tx.start()

    ## Stop the while loops.
    #tx.running = False

    ## Wait for threads to finish jobs.
    #tx.join()


