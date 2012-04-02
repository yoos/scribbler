from math import *

# General
serialPort = "/dev/ttyS0"
baudRate = 38400
debug = True

# TX
drawDelay = 0.4   # Time in seconds to wait for the arm to reach new drawing position.
zeroDelay = 1.0   # Time in seconds to wait for the arm to reach zero position (and power off).
serHeader = '\xff'

# Hardware configuration
shoulderZero = pi * 0.47   # Zero position of shoulder servo
elbowZero = pi       # Zero position of elbow servo

wristZero = pi * 0.45
wristPen  = 0.05
wristEraser = pi

upperArmLen = 6.25
lowerArmLen = 7.0

# Display configuration
origin = [3., 2.]   # Location of display origin.
segmentLen = 1.   # Segment length.
separation = 0.5   # Separation between digits.
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


