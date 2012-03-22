from math import *

# General
serialPort = "/dev/ttyS0"
baudRate = 76800
debug = True

# TX
dataSendInterval = 0.025   # 25 ms interval = 40 Hz. NOTE: This frequency should be LOWER than the microcontroller's control loop frequency!
serHeader = chr(255)

# Hardware configuration
shoulderZero = pi/2   # Zero position of shoulder servo
elbowZero = 0       # Zero position of elbow servo
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


# RX
newlineSerTag  = '\xde\xad\xbe\xef'
fieldSerTag    = '\xff\xff'
dcmSerTag      = '\xfb'
rotationSerTag = '\xfc'
motorSerTag    = '\xfd'
pidSerTag      = '\xfe'


