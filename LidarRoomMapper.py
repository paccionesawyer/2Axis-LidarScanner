#!/usr/bin/python3

import time
import math
import smbus
from PCA9685 import PCA9685
import numpy as np

import board
import busio
import adafruit_vl53l0x

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

# Initialize what servo hat ports the servos are on
servoX = 0
servoY = 3

# Set the Constrains established by the gimbal's design
minPosX = 0
maxPosX = 180
minPosY = 80
maxPosY = 82
xSkip = 1
ySkip = 1

xVals = []
yVals = []
zVals = []
radii = []

def angleToServo(angle):
    '''
    Perform a linear translation from an angle (0-180 deg) to the values used to
    decescribe the servo's movement
    '''
    # A linear transformation If your number X falls between A and B, and you would like Y to fall between C and D, you can apply the following linear transform:
    servoVal = (angle - 0)/(180 - 0) * (2500 - 500) + 500
    return servoVal

def getNewPoint(posX, posY):
    '''
    Generate a new point from the distance and the pitch and yaw (convert from spherical to xyz)
    '''
    radius = vl53.range ## Distance in mm
    radii.append(radius)

    azimuth = math.radians(posX)
    elevation = math.radians(180 - maxPosY + posY)

    x = radius * math.sin(elevation) * math.cos(azimuth)
    y = radius * math.sin(elevation) * math.sin(azimuth)
    z = radius * math.cos(elevation)

    xVals.append(x)
    yVals.append(y)
    zVals.append(z)

def plotData():
    '''
    Plot the xyz data 
    '''
    # Change the Size of Graph using
    # Figsize
    fig = plt.figure()
    
    # Generating a 3D sine wave
    ax = plt.axes(projection='3d')

    x = np.asarray(xVals)
    y = np.asarray(yVals)
    z = np.asarray(zVals)

    ax.scatter(x, y, z)

if __name__=='__main__':
    # Initialize the servo hat
    pwm = PCA9685(0x40, debug=False)
    pwm.setPWMFreq(50)

    reverse = False
    for i in range(minPosY,maxPosY,ySkip):
        '''
        Main For Loop moves along the y-axis
        '''
        posY = angleToServo(i) 
        pwm.setServoPulse(servoY,posY)
        if (not reverse):
            '''
            Move along the x-axis
            '''
            for j in range(minPosX,maxPosX,xSkip):
                posX = angleToServo(j)
                pwm.setServoPulse(servoX,posX)
                getNewPoint(posX, posY)
                time.sleep(0.005)
        else :
            for j in range(maxPosX,minPosX,-xSkip):
                posX = angleToServo(j)
                pwm.setServoPulse(servoX,posX)
                getNewPoint(posX, posY)
                time.sleep(0.005)

        reverse = not reverse
        time.sleep(0.01)
        
    plotData()

