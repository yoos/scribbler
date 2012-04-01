from math import *

# General
serialPort = "/dev/ttyS0"
baudRate = 38400
debug = True

# TX
dataSendInterval = 0.1   # 25 ms interval = 40 Hz. NOTE: This frequency should be LOWER than the microcontroller's control loop frequency!
serHeader = '\xff'

# Hardware configuration
shoulderZero = pi * 0.47   # Zero position of shoulder servo
elbowZero = pi       # Zero position of elbow servo

wristZero = pi * 0.47
wristPen  = 0
wristEraser = pi

upperArmLen = 10.
lowerArmLen = 10.

# Display configuration
origin = [5., 5.]   # Location of display origin.
segmentLen = 2.   # Segment length.
separation = 1.   # Separation between digits.
drawSpeed = 0.2   # Time interval between each drawing step.

numbers = [[[0,0], [0,1], [2,1], [2,0], [0,0]],                        # 0
           [[0,1], [2,1]],                                             # 1
           [[0,0], [0,1], [1,1], [1,0], [2,0], [2,1]],                 # 2
           [[0,0], [0,1], [1,1], [1,0], [1,1], [2,1], [2,0]],          # 3
           [[0,0], [1,0], [1,1], [0,1], [2,1]],                        # 4
           [[0,1], [0,0], [1,0], [1,1], [2,1], [2,0]],                 # 5
           [[0,1], [0,0], [2,0], [2,1], [1,1], [1,0]],                 # 6
           [[1,0], [0,0], [0,1], [2,1]],                               # 7
           [[1,0], [0,0], [0,1], [1,1], [1,0], [2,0], [2,1], [1,1]],   # 8
           [[1,1], [1,0], [0,0], [0,1], [2,1], [2,0]]]                 # 9


