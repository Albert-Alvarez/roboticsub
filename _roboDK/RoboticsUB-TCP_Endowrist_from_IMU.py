"""
********************************************************************************
RoboticsUB-TCP_Endowrist_from_IMU.py - Control based on a IMU.
Copyright (C) 2020  Albert Álvarez-Carulla
Repository: https://github.com/Albert-Alvarez/roboticsub-imu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
********************************************************************************
"""

import serial
import time
import math

# RoboDK API: import the robolink library (bridge with RoboDK)
from robolink import *
# Robot toolbox: import the robodk library (robotics toolbox)
from robodk import *

# ------------------------------------------------------------------------------
# Connection
# ------------------------------------------------------------------------------

# Establish the connection on a specific port (COM3)
arduino = serial.Serial('COM3', 115200, timeout=1)

# Lets bring some time to the system to stablish the connetction
time.sleep(2)

# Establish a link with the simulator
RDK = Robolink()

# ------------------------------------------------------------------------------
# Simulator setup
# ------------------------------------------------------------------------------

# Retrieve all items (object in the robodk tree)
# Define the "robot" variable with our robot (UR5e)
robot = RDK.Item ('UR5e')

# Define the "tcp" variable with the TCP of Endowrist needle
tcp_tool = RDK.Item('TCP_Endowrist')

# Performs a quick check to validate items defined
if robot.Valid():
    print('Robot selected: ' + robot.Name())
if tcp_tool.Valid():
    print('Tool selected: ' + tcp_tool.Name())

# Robot Flange with respect to UR5e base Frame
print ('Robot POSE is: ' + repr(robot.Pose()))
# Tool frame with respect to Robot Flange
print ('Robot POSE is: ' + repr(robot.PoseTool()))
# Tool frame with respect to Tool frame
print ('TCP pose is: ' + repr(tcp_tool.Pose()))

# ------------------------------------------------------------------------------
# Reference frame is fixed to TCP
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Data comunication
# ------------------------------------------------------------------------------

try:
    while True:

        # Requesting data to Ardino (command A)
        arduino.write(b'A')

        # Storing received data
        roll_str = arduino.readline().strip()
        pitch_str = arduino.readline().strip()
        yaw_str = arduino.readline().strip()

        print(roll_str, pitch_str, yaw_str)

        # Convert variable values from string to float
        roll = float(roll_str)
        pitch = float(pitch_str)
        yaw = float(yaw_str)

        # Print the integer value of roll, pitch and yaw angles in degrees
        #print('The R,P,Y angles (in degrees) from the MPU movements are: ')
        #print('roll  (x-forward (north)): ' + str(roll))
        #print('pitch (y-right (east): ' + str(pitch))
        #print('yaw   (z-down (down)): ' + str(yaw) + '\n')

        # Convert from degrees to radians R,P,Y angles
        R = math.radians(roll)
        P = math.radians(pitch)
        W = math.radians(yaw)
        X=0
        Y=-60
        Z=320
        
        # Calculate the POSE matrix (UR)
        
        #print ('The POSE matrix is: ' + repr(pose_matrix))

        # Define the Endowrist TCP POSE in the first suture point (1st point)
        # by first point matrix POSE:
        tcp_tool_pose = tcp_tool.setPoseTool(pose_matrix)
        print ('Tool TCP pose is: ' + repr([R,P,Y]) + '\n')

except KeyboardInterrupt:
    print("Communication stopped.")
    pass

# ------------------------------------------------------------------------------
# Disconnect Arduino
# ------------------------------------------------------------------------------
print("Disconnecting Arduino...")
arduino.close()
