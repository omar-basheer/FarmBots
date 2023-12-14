#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from pybricks.parameters import Port, Stop
from math import pi


RADIUS = 27 
DIAMETER = 53
DISTANCE_BTN_WHEELS = 118

ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
gripper_motor = Motor(Port.D)
drive_base = DriveBase(left_motor, right_motor, DIAMETER, DISTANCE_BTN_WHEELS)

def get_wheel_circumference(radius):
    return 2 * pi * radius

def get_num_degs(distance, radius):
    circumference = get_wheel_circumference(radius=radius)
    return (360 * distance) / circumference

def get_turn_degs(angle, radius, distance_btn_wheels):
    return (angle * distance_btn_wheels) / radius

def get_spin_degs(angle, radius, distance_btn_wheels):
    return (angle * DISTANCE_BTN_WHEELS) / (2 * RADIUS)

def drive_straight(distance, speed):
    num_degs = (distance * 360) / (DIAMETER * pi)

    left_motor.run_angle(speed, num_degs, wait=False)
    right_motor.run_angle(speed, num_degs, wait=False)
    wait(int(abs(num_degs) * 1000 / abs(speed))) 
    drive_base.stop()

def turn_in_place(direction, angle, speed):
    num_degs = (angle * DISTANCE_BTN_WHEELS) / (2 * RADIUS)

    if direction.lower() == 'left':
        left_motor.run_angle(-speed, num_degs, wait=False)
        right_motor.run_angle(speed, num_degs, wait=False)
    elif direction.lower() == 'right':
        left_motor.run_angle(speed, num_degs, wait=False)
        right_motor.run_angle(-speed, num_degs, wait=False)
    wait(int(abs(num_degs) * 1000 / abs(speed))) 
    drive_base.stop()

def close_gripper():
    """
    The function closes the gripper.
    """
    gripper_motor.run_until_stalled(speed=-250, then=Stop.HOLD, duty_limit=50)

def open_gripper():
    """
    The function opens the gripper.
    """
    gripper_motor.run_angle(speed=250, rotation_angle=1080, then=Stop.HOLD, wait=True)


# if __name__ == "__main__":
#     print("main")
#     drive_straight(1000, 100)
#     # turn_in_place('left', 360, 100)