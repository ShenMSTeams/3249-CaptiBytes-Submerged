from hub import light, light_matrix, motion_sensor, port

import color
import color_sensor

import motor_pair as mpair

import runloop

import time
import math
import sys

# Some constants used for movement calculations...
WHEEL_DIAMETER = 6.1
TURN_RADIUS = 5
F_CORRECTION_CONST = 0.001  # For forward move: Control by this number for every degree of error.

# Settings...
turn_assist = False
forward_assist = False


def settings_light():
    if turn_assist and forward_assist:
        light.color(light.CONNECT, color.GREEN)
    elif turn_assist:
        light.color(light.CONNECT, color.YELLOW)
    elif forward_assist:
        light.color(light.CONNECT, color.AZURE)


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
    yaw = motion_sensor.tilt_angles()
    print(yaw)


def ver():
    print(sys.version)
    print("ssl5k - ver 2.0-AZURE")
    print("Welcome to SuperSecretLib5000.py!")
    print("Created by FLL Team #3249 - the CaptiBytes")


def init(drive_l, drive_r, attach_l, attach_r, sensor_l, sensor_r):
    x = None
    ver()
    try:
        try:
            mpair.unpair(mpair.PAIR_1)
            mpair.unpair(mpair.PAIR_2)
        except:
            print("No pairs found, creating new motor pairs...")
        mpair.pair(mpair.PAIR_1, drive_l, drive_r)
        mpair.pair(mpair.PAIR_2, attach_l, attach_r)
    except:
        print("Something went wrong! Cannot create motor pairs!")
    light.color(light.POWER, color.AZURE)
    settings_light()
    light_matrix.write("#")
    return x, drive_l, drive_r, attach_l, attach_r, sensor_l, sensor_r


async def forward(dist: int, stop: bool = False, run_until=None,**kwargs):
    if run_until is None:
        run_until = lambda: False
        limit = False
    else:
        limit = True

    reset_gyro()
    yaw = None

    degrees = dist*(360.0/(math.pi*WHEEL_DIAMETER))

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
    """
    .format(dist = dist, stop = stop, run_until = limit, run_time = run_time, velocity = velocity, accel = accel))

    if forward_assist:
        print("Forward: Using gyro to assist movement...")
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
            
    else:  # (if forward_assist is NOT True):
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

    reset_gyro()

    dist = (2*math.pi*TURN_RADIUS)*(theta/360.0)
    degrees = dist*(360.0/(math.pi*WHEEL_DIAMETER))

    velocity = int(kwargs.get("velocity", 360)/2)
    if degrees < 0:
        velocity = -1*velocity

    run_time = round((degrees/velocity)*1000.0)
    run_time = abs(run_time)

    print("""\nTurn --
    theta= {theta}, stop= {stop}, run_until= {run_until}
    kwargs= {kwargs}
    """
    .format(theta = theta, stop = stop, run_until = limit, kwargs = kwargs.items()))

    total_turn = 0.0

    if turn_assist is False:
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

    elif turn_assist:
        mpair.move_tank(mpair.PAIR_1, velocity, -1*velocity)
        start = time.ticks_ms()
        angle_prev = (motion_sensor.tilt_angles()[0])/10.0
        while True:
            if run_until():
                break
            now = time.ticks_ms()
            if now-start > run_time:
                break

            angle_now = (motion_sensor.tilt_angles()[0])/10.0
            if angle_now < 0.0 and angle_prev > 0.0 and theta > 0.0:  # Sign change + -> - (turning right)
                _delta_pos = 180.0 - angle_prev
                _delta_neg = angle_now + 180.0
                delta_turn = _delta_pos + _delta_neg
            elif angle_now > 0.0 and angle_prev < 0.0 and theta < 0.0:
                _delta_neg = -180.0 - angle_prev
                _delta_pos = angle_now + 180.0
                delta_turn = _delta_pos + _delta_neg
            else:
                delta_turn = angle_now - angle_prev

            total_turn += delta_turn

            if abs(total_turn) >= abs(theta):
                break

            angle_prev = angle_now

        print("""\nGyro --
    expected= {theta} degrees
    gyro= {total_turn} degrees
    error= {error} degrees
        """
        .format(theta = theta, total_turn = total_turn, error = total_turn-theta))

    if stop:
        mpair.stop(mpair.PAIR_1)

    light_power_off()


async def attachment(degrees: int, attach_port: str):
    if attach_port.lower() == "left":
        await mpair.move_tank_for_degrees(mpair.PAIR_2, degrees, 360, 0)
    if attach_port.lower() == "right":
        await mpair.move_tank_for_degrees(mpair.PAIR_2, degrees, 0, 360)
    if attach_port.lower() == "both":
        await mpair.move_tank_for_degrees(mpair.PAIR_2, degrees, 360, 360)

    print("""\nAttachment --
    degrees= {degrees}
    attach_port= {attach_port}
    """
        .format(degrees = degrees, attach_port = attach_port))


async def sensor(sensor_type: str, sensor_port: int, expected: int):
    if sensor_type.lower() == "color":
        value = color_sensor.color(sensor_port)
        return value == expected
    # We only have color sensors implemented at the moment.
