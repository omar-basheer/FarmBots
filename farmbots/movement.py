#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from pybricks.parameters import Port
from math import pi

RADIUS = 27 
DIAMETER = 54
DISTANCE_BTN_WHEELS = 122

ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
# drive_base = DriveBase(left_motor=left_motor, right_motor=right_motor, wheel_diameter=DIAMETER, axle_track=DISTANCE_BTN_WHEELS)
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



# Helper functions



# Movement functions


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

# def spin(direction, angle, speed):
#     num_degs = get_spin_degs(angle=angle, radius=RADIUS, distance_btn_wheels=DISTANCE_BTN_WHEELS)
#     if direction.lower() == 'left':
#         drive_base.drive(speed, -speed)
#     elif direction.lower() == 'right':
#         drive_base.drive(-speed, speed)
#     wait(num_degs * 1000 / speed)
#     drive_base.stop()


"""
@team: 9
@authors: Cyril Kujar, Abigail Animah Owusu, and Omar Basheer
@date: November 19, 23.
"""

# # Importing requirement modules and classes from the ev3dev2 library.
# from ev3dev2.motor import LargeMotor, MoveTank, OUTPUT_B, OUTPUT_C
# from ev3dev2.sound import Sound
# from math import pi

# # Instanstiating objects of the Sound, LargeMotor, and MoveTank classes
# microphone = Sound()
# right_motor = LargeMotor(OUTPUT_B)
# left_motor = LargeMotor(OUTPUT_C)
# drive_base = MoveTank(OUTPUT_C, OUTPUT_B)

# # Instantiation of constants
# RADIUS = 2.7 
# DISTANCE_BTN_WHEELS = 11.7

# # Setting the volume of the microphone to 100%. 
# # This means that any sound played through the microphone will be played at the maximum volume.
# microphone.set_volume(100)

# # HELPER FUNCTIONS
# def get_wheel_circumference(radius):
#     """
#     The function calculates the circumference of a wheel given its radius.
    
#     :param radius: The radius is the distance from the center of a circle to any point on its
#     circumference
#     :return: the circumference of a wheel given its radius.
#     """
#     circumference = (2 * pi * radius)
#     return circumference

# def get_num_degs(distance, radius):
#     """
#     The function calculates the number of degrees a wheel needs to rotate to travel a given distance.
    
#     :param distance: The distance is the length of the path traveled by the wheel in any unit of measurement (e.g. centimenters, meters, kilometers, miles)
#     :param radius: The radius is the distance from the center of the wheel to the outer edge
#     :return: the number of degrees that correspond to a given distance traveled along the circumference
#     of a wheel with a given radius.
#     """
#     circumference = get_wheel_circumference(radius=radius)
#     num_degs = (360 * distance) / circumference
#     return num_degs

# def get_turn_degs(angle, radius, distance_btn_wheels):
#     """
#     The function calculates the number of degrees a robot's wheels need to turn to achieve a desired angle of rotation.
    
#     :param angle: The angle is the desired turning angle in degrees
#     :param radius: The radius is the distance from the center of the circle to the outer edge. It is typically measured in units such as centimeters or inches
#     :param distance_btn_wheels: The distance between the wheels of a robot
#     :return: the number of degrees that the wheels need to turn in order to achieve the desired angle of
#     rotation.
#     """
#     num_degs = (angle * distance_btn_wheels) / radius
#     return num_degs

# def get_spin_degs(angle, radius, distance_btn_wheels):
#     """
#     The function calculates the number of degrees a robot's wheels need to spin to achieve a desired
#     angle of rotation.
    
#     :param angle: The angle through which the wheels are rotated (in degrees)
#     :param radius: The radius is the distance from the center of the wheel to the point where the tire
#     makes contact with the ground
#     :param distance_btn_wheels: The distance between the wheels of a robot (base radius)
#     :return: the number of degrees that the wheels will spin based on the given angle, radius, and
#     distance between the wheels.
#     """
#     num_degs = (angle * (distance_btn_wheels / 2)) / radius
#     return num_degs

# # Queestion 1
# def drive_straight(distance, speed):
#     """
#     The function "drive_straight" uses the "get_num_degs" function to calculate the number of degrees the robot needs to drive forwards, and then uses the "on_for_degrees" method to make the robot drives straight for a given distance at a specified speed.
    
#     :param distance: The distance parameter represents the distance you want the robot to drive straight
#     in a straight line. It is measured in any unit of length, such as centimeters or inches
#     :param speed: The speed parameter represents the desired speed at which the robot should drive
#     straight. It is typically measured in units such as centimeters per second or degrees per second
#     """
#     num_degs = get_num_degs(distance=distance, radius=RADIUS)
#     drive_base.on_for_degrees(left_speed=speed, right_speed=speed, degrees=num_degs, brake=True, block=True)

# def reverse(distance, speed):
#     """
#     The function "reverse" uses the "get_num_degs" function to calculate the number of degrees the robot
#     needs to drive backwards, and then uses the "on_for_degrees" method to make the robot drive
#     backwards for that distance at the given speed.
    
#     :param distance: The distance parameter represents the distance that the robot needs to travel in a
#     straight line. It is typically measured in units such as centimeters or inches
#     :param speed: The speed parameter represents the speed at which the robot should move. It determines
#     how fast the robot's wheels will rotate
#     """
#     num_degs = get_num_degs(distance=distance, radius=RADIUS)
#     drive_base.on_for_degrees(left_speed=-speed, right_speed=-speed, degrees=num_degs, brake=True, block=True)

# def turn(direction, angle, speed):
#     """
#     The function "turn" takes in a direction, angle, and speed, and then calculates the number of
#     degrees to turn the motors based on the given angle, radius, and distance between wheels, and then
#     turns the motors accordingly.
    
#     :param direction: The direction parameter specifies the direction in which the robot should turn. It
#     can be either 'right' or 'left'
#     :param angle: The angle parameter represents the angle at which the robot should turn. It is the
#     amount of rotation in degrees that the robot should make
#     :param speed: The "speed" parameter represents the speed at which the motors should turn. It
#     determines how fast the robot will rotate
#     """
#     num_degs = get_turn_degs(angle=angle, radius=RADIUS, distance_btn_wheels=DISTANCE_BTN_WHEELS)
#     if direction.lower() == 'right':
#         left_motor.on_for_degrees(speed=speed, degrees=num_degs)
#     elif direction.lower() == 'left':
#         right_motor.on_for_degrees(speed=speed, degrees=num_degs)
#     else:
#         microphone.speak(text="Unknown Direction")

# def spin(direction, angle, speed):
#     """
#     This method spins the robot in the specified direction (left or right) by the given
#     angle and speed.
    
#     :param direction: The direction parameter specifies the direction in which the robot should spin. It can be either 'left' or 'right'
#     :param angle: The angle parameter represents the angle at which the robot should spin. It is used to
#     calculate the number of degrees the robot's wheels should rotate in order to achieve the desired spin
#     :param speed: The "speed" parameter in the "spin_left" function represents the speed at which the robot should spin. It determines how fast the wheels should rotate during the spin
#     """
#     num_degs = get_spin_degs(angle=angle, radius=RADIUS, distance_btn_wheels=DISTANCE_BTN_WHEELS)
#     if direction.lower() == 'left':
#         drive_base.on_for_degrees(left_speed=-speed, right_speed=speed, degrees=num_degs, brake=True, block=True)
#     elif direction.lower() == 'right':
#         drive_base.on_for_degrees(left_speed=speed, right_speed=-speed, degrees=num_degs, brake=True, block=True)
#     else:
#         microphone.speak(text="Unknown Direction")

if __name__ == "__main__":
    # spin('right', 90, 70)
    turn_in_place('left', 90, 100)
    # drive_straight(500, 100)

