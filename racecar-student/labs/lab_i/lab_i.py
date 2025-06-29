"""
MIT BWSI Autonomous RACECAR
MIT License
racecar-neo-prereq-labs

File Name: lab_i.py

Title: Lab I - Wall Follower

Author: [PLACEHOLDER] << [Write your name or team name here]

Purpose: This script provides the RACECAR with the ability to autonomously follow a wall.
The script should handle wall following for the right wall, the left wall, both walls, and
be flexible enough to handle very narrow and very wide walls as well.

Expected Outcome: When the user runs the script, the RACECAR should be fully autonomous
and drive without the assistance of the user. The RACECAR drives according to the following
rules:
- The RACECAR detects a wall using the LIDAR sensor a certain distance and angle away.
- Ideally, the RACECAR should be a set distance away from a wall, or if two walls are detected,
should be in the center of the walls.
- The RACECAR may have different states depending on if it sees only a right wall, only a 
left wall, or both walls.
- Both speed and angle parameters are variable and recalculated every frame. The speed and angle
values are sent once at the end of the update() function.

Note: This file consists of bare-bones skeleton code, which is the bare minimum to run a 
Python file in the RACECAR sim. Less help will be provided from here on out, since you've made
it this far. Good luck, and remember to contact an instructor if you have any questions!

Environment: Test your code using the level "Neo Labs > Lab I: Wall Follower".
Use the "TAB" key to advance from checkpoint to checkpoint to practice each section before
running through the race in "race mode" to do the full course. Lowest time wins!
"""

########################################################################################
# Imports
########################################################################################

import sys

# If this file is nested inside a folder in the labs folder, the relative path should
# be [1, ../../library] instead.
sys.path.insert(0, '../library')
import racecar_core

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# Declare any global variables here
global speed
global angle
global target_distance
global kp

########################################################################################
# Functions
########################################################################################

# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    global speed
    global angle
    global target_distance
    global kp

    speed = 0.0
    angle = 0.0
    target_distance = 0.5  # meters
    kp = 2.0  # Proportional gain for angle control

    rc.drive.stop()
    rc.set_update_slow_time(0.5)

    print(">> Lab I - Wall Follower\n")
    print("Controls:")
    print("   RACECAR will autonomously follow walls.")


# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    global speed
    global angle

    lidar_distances = rc.lidar.get_distances()

    # Get distances to the right and left walls
    right_distance = rc_utils.get_lidar_closest_point(lidar_distances, (270 - 10, 270 + 10))
    left_distance = rc_utils.get_lidar_closest_point(lidar_distances, (90 - 10, 90 + 10))

    # Default speed
    speed = 0.5

    # State machine for wall following
    if right_distance > 0 and left_distance > 0:
        # Both walls detected, try to stay in the middle
        error = left_distance - right_distance
        angle = kp * error
    elif right_distance > 0:
        # Only right wall detected, follow it
        error = target_distance - right_distance
        angle = -kp * error  # Negative to turn away from the wall if too close
    elif left_distance > 0:
        # Only left wall detected, follow it
        error = target_distance - left_distance
        angle = kp * error  # Positive to turn away from the wall if too close
    else:
        # No walls detected, drive straight
        angle = 0.0
        speed = 0.5 # Keep moving forward to find a wall

    # Clamp angle to valid range [-1, 1]
    angle = max(-1.0, min(1.0, angle))

    rc.drive.set_speed_angle(speed, angle)


# [FUNCTION] update_slow() is similar to update() but is called once per second by
# default. It is especially useful for printing debug messages, since printing a 
# message every frame in update is computationally expensive and creates clutter
def update_slow():
    lidar_distances = rc.lidar.get_distances()
    right_distance = rc_utils.get_lidar_closest_point(lidar_distances, (270 - 10, 270 + 10))
    left_distance = rc_utils.get_lidar_closest_point(lidar_distances, (90 - 10, 90 + 10))
    print(f"Right distance: {right_distance:.2f}m, Left distance: {left_distance:.2f}m, Angle: {angle:.2f}")


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
