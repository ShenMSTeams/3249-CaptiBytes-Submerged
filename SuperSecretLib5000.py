"""This is an example SuperSecretLib5000.

This SuperSecretLib5000 does stuff.
"""

__version__ = '2.5a'
__author__ = 'Shen FLL Team #3249 - the Captibytes'

import sys
import time
import math
import json

from hub import motion_sensor
from hub import light
from hub import light_matrix

import color
import color_sensor

import motor_pair as mpair


F_CORRECTION_CONST = 0.001  # For forward move: Control by this number for every degree of error.


def assist_light():
    light.color(light.CONNECT, color.YELLOW)


def gyro_light(status: str):
    if status.lower() == "good":
        light.color(light.POWER, color.GREEN)
    if status.lower() == "bad":
        light.color(light.POWER, color.RED)


def light_power_off():
    light.color(light.POWER, color.AZURE)


def reset_gyro():
    motion_sensor.set_yaw_face(motion_sensor.TOP)
    motion_sensor.reset_yaw(0)
    angles = motion_sensor.tilt_angles()
    print("Gyro angles:", angles)


def exit():
    raise SystemExit("Program ended with ssl5k.exit() function.")


def ver():
    print(sys.version)
    print("SuperSecretLib5000 version:", __version__)
    print("Created by:", __author__)


def init(*args, **kwargs):
    ver()

    # Create named arguments so they can be referenced later, even if they have no value.
    drive_l = None
    drive_r = None
    attach_l = None
    attach_r = None
    sensor_l = None
    sensor_r = None
    WHEEL_DIAMETER = None
    TANK_TURN_RADIUS = None

    for i in args:
        if i == 1:
            drive_l = args(0)
        elif i == 2:
            drive_r = args(1)
        elif i == 3:
            attach_l = args(2)
        elif i == 4:
            attach_r = args(3)
        elif i == 5:
            sensor_l = args(4)
        elif i == 6:
            sensor_r = args(5)
        elif i == 7:
            WHEEL_DIAMETER = args(6)
        elif i == 8:
            TANK_TURN_RADIUS = args(7)

    use_json = kwargs.get("use_json", False)

    if use_json:
        try:  # Check init.json file for ports and wheel info, use only if there is no value.
            with open("/flash/init.json", "r") as ij:
                init_config = json.load(ij)
                if drive_l is None:
                    drive_l = init_config["ports"][0]
                if drive_r is None:
                    drive_r = init_config["ports"][1]
                if attach_l is None:
                    attach_l = init_config["ports"][2]
                if attach_r is None:
                    attach_r = init_config["ports"][3]
                if sensor_l is None:
                    sensor_l = init_config["ports"][4]
                if sensor_r is None:
                    sensor_r = init_config["ports"][5]
                if WHEEL_DIAMETER is None:
                    WHEEL_DIAMETER = init_config["wheel_info"]["wheel_diameter"]
                if TANK_TURN_RADIUS is None:
                    TANK_TURN_RADIUS = init_config["wheel_info"]["tank_turn_radius"]
        except ValueError:
            raise ValueError("Failed to read init.json file! Please make sure the file is contains JSON syntax and is structured properly.")
        except OSError:
            raise OSError("Could not find init.json file! Please make sure the file has the correct name and is in the root directory of the bot.")

    try:
        try:
            mpair.unpair(mpair.PAIR_1)
            mpair.unpair(mpair.PAIR_2)
        except RuntimeError:
            print("No pairs found, proceeding with creating pairs...")
        mpair.pair(mpair.PAIR_1, drive_l, drive_r)
        mpair.pair(mpair.PAIR_2, attach_l, attach_r)
    except RuntimeError:
        raise RuntimeError("Failed to create motor pairs! Please make sure the ports used are not part of any other pairs.")
    except ValueError:
        raise ValueError("Failed to create motor pairs! Please make sure the ports passed as motors connect to motors and that all ports are valid.")

    light.color(light.POWER, color.AZURE)
    light_matrix.write("#")
    return drive_l, drive_r, attach_l, attach_r, sensor_l, sensor_r, WHEEL_DIAMETER, TANK_TURN_RADIUS


async def forward(dist: int, stop: bool = False, run_until=None, **kwargs):
    if run_until is None:
        run_until = lambda: False
        limit = False
    else:
        limit = True

    reset_gyro()
    yaw = motion_sensor.tilt_angles()[0]

    degrees = dist*(360.0/(math.pi*init.WHEEL_DIAMETER))

    assist = kwargs.get("assist", False)
    accel = kwargs.get("acceleration", 10000)
    velocity = kwargs.get("velocity", 360)
    if degrees < 0:
        velocity = -1*velocity

    run_time = round((degrees/velocity)*1000.0)
    run_time = abs(run_time)

    print("""\nForward --
    dist= {dist}, stop= {stop}, run_until= {run_until}
    run_time= {run_time}
    velocity= {velocity}
    accel= {accel}
    """.format(dist=dist, stop=stop, run_until=limit, run_time=run_time, velocity=velocity, accel=accel))

    if assist:
        print("Forward: Using gyro to assist movement...")
        assist_light()

        start = time.ticks_ms()
        while True:
            if run_until():
                print("Forward: Stopping due to sensors...")
                break
            now = time.ticks_ms()
            if now-start > run_time:
                print("Forward: Stopping due to time...")
                break

            yaw = motion_sensor.tilt_angles()[0]
            f_correction_factor = yaw*F_CORRECTION_CONST
            correction = velocity*f_correction_factor
            mpair.move_tank(mpair.PAIR_1, int(velocity+correction), int(velocity-correction), acceleration=accel)
            gyro_light("good")

    else:  # (if assist is NOT True):
        print("Forward: Moving without gyro assist...")
        mpair.move_tank(mpair.PAIR_1, velocity, velocity, acceleration=accel)
        start = time.ticks_ms()
        while True:
            if run_until():
                print("Forward: Stopping due to sensors...")
                break
            now = time.ticks_ms()
            if now-start > run_time:
                print("Forward: Stopping due to time...")
                break

    if stop:
        mpair.stop(mpair.PAIR_1)

    light_power_off()


async def turn(theta: int, stop: bool = False, run_until=None, **kwargs):
    if run_until is None:
        run_until = lambda: False
        limit = False
    else:
        limit = True

    dist = (2*math.pi*init.TURN_RADIUS)*(theta/360.0)
    degrees = dist*(360.0/(math.pi*init.WHEEL_DIAMETER))

    velocity = int(kwargs.get("velocity", 360)/2)
    if degrees < 0:
        velocity = -1*velocity

    run_time = round((degrees/velocity)*1000.0)
    run_time = abs(run_time)

    print("""\nTurn --
    theta= {theta}, stop= {stop}, run_until= {run_until}
    kwargs= {kwargs}
    """.format(theta=theta, stop=stop, run_until=limit, kwargs=kwargs.items()))

    mpair.move_tank(mpair.PAIR_1, velocity, -1*velocity)
    start = time.ticks_ms()
    while True:
        if run_until():
            print("Turn: Stopping due to sensors...")
            break
        now = time.ticks_ms()
        if now-start > run_time:
            print("Turn: Stopping due to time...")
            break

    if stop:
        mpair.stop(mpair.PAIR_1)

    light_power_off()


async def attachment(degrees: int, attach_side: str):
    if attach_side.lower() == "left":
        await mpair.move_tank_for_degrees(mpair.PAIR_2, degrees, 360, 0)
    if attach_side.lower() == "right":
        await mpair.move_tank_for_degrees(mpair.PAIR_2, degrees, 0, 360)
    if attach_side.lower() == "both":
        await mpair.move_tank_for_degrees(mpair.PAIR_2, degrees, 360, 360)

    print("""\nAttachment --
    degrees= {degrees}
    attach_side= {attach_side}
    """.format(degrees=degrees, attach_side=attach_side))


async def sensor(sensor_type: str, sensor_side: str, expected: int):
    if sensor_side.lower() == "left":
        sensor_port = init.attach_l
    elif sensor_side.lower() == "right":
        sensor_port = init.attach_r

    if sensor_type.lower() == "color":
        value = color_sensor.color(sensor_port)
        return value == expected
    # We only have color sensors implemented at the moment.
