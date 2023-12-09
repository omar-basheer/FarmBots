from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from pybricks.parameters import Port
from math import pi

RADIUS = 27 
DIAMETER = 54
DISTANCE_BTN_WHEELS = 117

ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
# drive_base = DriveBase(left_motor=left_motor, right_motor=right_motor, wheel_diameter=DIAMETER, axle_track=DISTANCE_BTN_WHEELS)
drive_base = DriveBase(left_motor, right_motor, DIAMETER, DISTANCE_BTN_WHEELS)


# Helper functions
def get_wheel_circumference(radius):
    return 2 * pi * radius

def get_num_degs(distance, radius):
    circumference = get_wheel_circumference(radius=radius)
    return (360 * distance) / circumference

def get_turn_degs(angle, radius, distance_btn_wheels):
    return (angle * distance_btn_wheels) / radius

def get_spin_degs(angle, radius, distance_btn_wheels):
    return (angle * (distance_btn_wheels / 2)) / radius

# Movement functions
def drive_straight(distance, speed):
    num_degs = get_num_degs(distance=distance, radius=RADIUS)
    drive_base.drive(speed, 0)
    wait(num_degs * 1000 / speed)
    drive_base.stop()

def reverse(distance, speed):
    num_degs = get_num_degs(distance=distance, radius=RADIUS)
    drive_base.drive(-speed, 0)
    wait(num_degs * 1000 / abs(speed))
    drive_base.stop()

def turn(direction, angle, speed):
    num_degs = get_turn_degs(angle=angle, radius=RADIUS, distance_btn_wheels=DISTANCE_BTN_WHEELS)
    if direction.lower() == 'right':
        left_motor.run_angle(speed=speed, rotation_angle=num_degs)
    elif direction.lower() == 'left':
        right_motor.run_angle(speed=speed, rotation_angle=num_degs)

def spin(direction, angle, speed):
    num_degs = get_spin_degs(angle=angle, radius=RADIUS, distance_btn_wheels=DISTANCE_BTN_WHEELS)
    if direction.lower() == 'left':
        drive_base.drive(-speed, speed)
    elif direction.lower() == 'right':
        drive_base.drive(speed, -speed)
    wait(num_degs * 1000 / speed)
    drive_base.stop()
