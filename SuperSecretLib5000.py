""" SuperSecretLib5000.py

Author: FLL Team 3249 - the Captibytes
Created for: LEGO SPIKE 3 Robots

Description:
This library provides functions to more efficiently program LEGO SPIKE 3 robots.
It includes features for motor control, sensor integration, and other
robotics-related functionalities to assist in FIRST LEGO League (FLL) challenges.

Usage:
Import this library into your LEGO SPIKE 3 Python program to access its functions.

Example:
    import SuperSecretLib5000 as ssl5k
    ssl5k.some_function()

NOTE:
This library was created and is maintained by the FLL Captibytes team and is
not officially supported by LEGO.
"""

__version__ = '2.7'
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
import distance_sensor
import force_sensor

import motor_pair as mpair

# For forward move: Correction factor to adjust for yaw error.
CORRECTION_CONST = 0.001


def assist_light():
    """ Turn on the assist light (yellow) to indicate that gyro-based movement is active. """
    light.color(light.CONNECT, color.YELLOW)


def reset_gyro():
    """ Reset the robot's gyroscope to ensure proper. """
    motion_sensor.set_yaw_face(motion_sensor.TOP)
    motion_sensor.reset_yaw(0)
    angles = motion_sensor.tilt_angles()
    print("Gyro angles:", angles)


def exit():
    """ Stop the current program and exit to menu. """
    raise SystemExit("Program ended with ssl5k.exit() function.")


def ver():
    """ Print the Python and SuperSecretLib5000 version information. """
    print(sys.version)
    print("SuperSecretLib5000 version:", __version__)
    print("Created by:", __author__)


# Dictionary for storing robot configuration settings.
_config = dict(
    drive_l = None,
    drive_r = None,
    attach_l = None,
    attach_r = None,
    sensor_l = None,
    sensor_r = None,
    WHEEL_DIAMETER = None,
    TURN_RADIUS = None,
)


def init(**kwargs):
    """ Sets up the robot configuration, including ports and wheel info.

    Parameters:
    - kwargs

    Accepted kwargs arguments:
    - Ports (drive train, attachment, sensors)
    - Wheel diameter (CM)
    - Turn radius (Tank) (CM)
    """

    ver()  # Print version info at initialization.

    for key in _config.keys():
        _config[key] = kwargs.get(key)

    use_json = kwargs.get("use_json", False)

    config_error = False
    errors = []

    def _process_cfg(key, cfg_item_f):
        """ Process configuration settings, handling missing values. """
        global config_error
        try:
            _val = kwargs.get(key)
            if _val is None:
                _val = cfg_item_f()
            _config[key] = _val
        except Exception:
            config_error = True
            errors.append(key)

    if config_error:
        raise ValueError(f'missing config keys: {errors}')

    # Load configuration from JSON file if requested.
    if use_json:
        try:
            with open("/flash/init.json", "r") as ij:
                init_config = json.load(ij)
                _process_cfg('drive_l', lambda: init_config['ports'][0])
                _process_cfg('drive_r', lambda: init_config['ports'][1])
                _process_cfg('attach_l', lambda: init_config['ports'][2])
                _process_cfg('attach_r', lambda: init_config['ports'][3])
                _process_cfg('sensor_l', lambda: init_config['ports'][4])
                _process_cfg('sensor_r', lambda: init_config['ports'][5])
                _process_cfg('WHEEL_DIAMETER', lambda: init_config['wheel_info']['wheel_diameter'])
                _process_cfg('TURN_RADIUS', lambda: init_config['wheel_info']['turn_radius'])

                if config_error:
                    raise ValueError("Missing config keys: {errors}"
                                     .format(errors=errors))

        except ValueError:
            raise ValueError("Failed to read init.json file! "
                             "Please make sure the file contains proper JSON "
                             " syntax and is structured correctly.")
        except OSError:
            raise OSError("Could not find init.json file! "
                          "Please make sure the file has the correct name and"
                          " is in the root directory of the bot.")

    # Attempt to unpair and re-pair motors.
    try:
        try:
            mpair.unpair(mpair.PAIR_1)
            mpair.unpair(mpair.PAIR_2)
        except RuntimeError:
            print("No pairs found, proceeding with creating pairs...")

        # Create motor pairs based on configuration settings.
        mpair.pair(mpair.PAIR_1, _config['drive_l'], _config['drive_r'])
        mpair.pair(mpair.PAIR_2, _config['attach_l'], _config['attach_r'])

    except RuntimeError:
        raise RuntimeError("Failed to create motor pairs! "
                           "Please make sure the ports used are not part of"
                           " any other pairs.")
    except ValueError:
        raise ValueError("Failed to create motor pairs! "
                         "Please make sure the ports passed as motors connect"
                         " to motors and that all ports are valid.")

    # Indicate successful initialization.
    light.color(light.POWER, color.AZURE)
    light_matrix.write("#")

    # Return all configuration settings.
    return (_config['drive_l'], _config['drive_r'],
            _config['attach_l'], _config['attach_r'],
            _config['sensor_l'], _config['sensor_r'],
            _config['WHEEL_DIAMETER'], _config['TURN_RADIUS'])


async def forward(dist: int, stop: bool = False, run_until=None, **kwargs):
    """ Move the bot forwards a specified distance in centimeters.

    Parameters:
    - dist: Distance to move in centimeters
    - stop: True/False whether or not to stop at the end.
    - run_until: Callable that is checked for a True/False value. If true,
                 stop the motors. (If stop = True.)
    - kwargs: Other options such as velocity, acceleration or assist mode.

    Signature:
    `forward(dist: int, stop: bool = False, run_until=None, **kwargs)`
    """

    # If run_until is not specified, set it to False.
    if run_until is None:
        run_until = lambda: False
        limit = False
    else:
        limit = True

    # For forward move: Value is changed depending on if:
    # the bot is moving backwards (-1) or forwards (1)
    # first, assume the bot is moving forwards.
    correction_mult = 1

    reset_gyro()
    yaw = motion_sensor.tilt_angles()[0]

    degrees = dist*(360.0/(math.pi*_config['WHEEL_DIAMETER']))

    # Read additional parameters.
    assist = kwargs.get("assist", False)
    accel = kwargs.get("acceleration", 10000)
    velocity = kwargs.get("velocity", 360)
    if degrees < 0:
        velocity = -1*velocity
        correction_mult = -1

    run_time = round((degrees/velocity)*1000.0)
    run_time = abs(run_time)

    print("""\nForward --
    dist= {dist}, stop= {stop}, run_until= {run_until}
    run_time= {run_time}
    velocity= {velocity}
    accel= {accel}
    f_mult= {mult}
    """.format(dist=dist, stop=stop, run_until=limit, run_time=run_time,
               velocity=velocity, accel=accel, mult=correction_mult))

    if assist:
        print("Forward: Using gyro to assist movement...")
        assist_light()

        start = time.ticks_ms()
        while True:
            if run_until():
                print("Forward: Stopping due to sensors...")
                print("Stopped on: {run_until}\n"
                      .format(run_until=run_until()))
                break
            now = time.ticks_ms()
            if now-start > run_time:
                print("Forward: Stopping due to time...")
                print("Stopped on: {current_time}\n"
                      .format(current_time=now-start))
                break

            yaw = motion_sensor.tilt_angles()[0]
            correction_factor = yaw*CORRECTION_CONST
            correction = velocity*correction_factor
            mpair.move_tank(mpair.PAIR_1,
                            int(velocity+correction*correction_mult),
                            int(velocity-correction*correction_mult),
                            acceleration=accel)

    else:  # (if assist is NOT True):
        print("Forward: Moving without gyro assist...")
        mpair.move_tank(mpair.PAIR_1, velocity, velocity, acceleration=accel)
        start = time.ticks_ms()
        while True:
            if run_until():
                print("Forward: Stopping due to sensors...")
                print("Stopped on: {run_until}\n"
                      .format(run_until=run_until()))
                break
            now = time.ticks_ms()
            if now-start > run_time:
                print("Forward: Stopping due to time...")
                print("Stopped on: {current_time}\n"
                      .format(current_time=now-start))
                break

    if stop:
        mpair.stop(mpair.PAIR_1)


async def turn(theta: int, stop: bool = False, run_until=None, **kwargs):
    """ Turn the bot a specified number of degrees left or right.

    Parameters:
    - theta: Degrees to turn the bot. Left is negative and right is positive.
    - stop: True/False value whether or not to stop at the end.
    - run_until: Callable that is checked for a True/False value.
                 If true, stop motors. (If stop = True.)
    - kwargs: Optional parameter for specifying velocity.

    Signature:
    `turn(theta: int, stop: bool = False, run_until=None, **kwargs)`
    """

    # Same as forward move: if run_until is not specified, set it to False.
    if run_until is None:
        run_until = lambda: False
        limit = False
    else:
        limit = True

    dist = (2*math.pi*_config['TURN_RADIUS'])*(theta/360.0)
    degrees = dist*(360.0/(math.pi*_config['WHEEL_DIAMETER']))

    # Read velocity parameter.
    velocity = int(kwargs.get("velocity", 360)/2)
    if degrees < 0:
        velocity = -1*velocity

    run_time = round((degrees/velocity)*1000.0)
    run_time = abs(run_time)

    print("""\nTurn --
    theta= {theta}, stop= {stop}, run_until= {run_until}
    run_time= {run_time}
    velocity= {velocity}
    """.format(theta=theta, stop=stop, run_until=limit, run_time=run_time,
               velocity=velocity))

    mpair.move_tank(mpair.PAIR_1, velocity, -1*velocity)
    start = time.ticks_ms()
    while True:
        if run_until():
            print("Turn: Stopping due to sensors...")
            print("Stopped on: {run_until}\n"
                  .format(run_until=run_until()))
            break
        now = time.ticks_ms()
        if now-start > run_time:
            print("Turn: Stopping due to time...")
            print("Stopped on: {current_time}\n"
                  .format(current_time=now-start))
            break

    if stop:
        mpair.stop(mpair.PAIR_1)


async def attachment(degrees: int, attach_side: str):
    """ Turn attachment motor(s) a number of degrees.

    Parameters:
    - degrees: Degrees to turn the attachment motor(s).
    - attach_side: Attachment motor(s) to move. (left/right/both)

    Signature:
    `attachment(degrees: int, attach_side: str)`

    NOTE: Attachment motor side is determined in the order they are listed
    in the config. If you listed the right attachment motor before the left one,
    you would have to write "left" to use the right attachment motor.
    """

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


def sensor(sensor_type: str, sensor_side: str):
    """ Reads a sensor value and compares it to the expected value.

    Parameters:
    - sensor_type (str): Type of the sensor ('color', 'distance', 'force').
    - sensor_side (str): Side of the robot where the sensor is located ('left' or 'right').
    - expected (int): Expected sensor value to compare against.

    Returns:
    - bool: True if the sensor value matches the expected, False otherwise.

    Signature:
    `sensor(sensor_type: str, sensor_side: str, expected: int)`

    NOTE: Sensor side is determined in the order they are listed
    in the config. If you listed the right sensor before the left one,
    you would have to write "left" to read the right sensor.
    """

    # Select sensor based on side.
    if sensor_side.lower() == "left":
        sensor_port = _config['sensor_l']
    elif sensor_side.lower() == "right":
        sensor_port = _config['sensor_r']

    # Read and compare sensor value to the expected.
    if sensor_type.lower() == "color":
        value = color_sensor.color(sensor_port)
    elif sensor_type.lower() == "distance":
        value = distance_sensor.distance(sensor_port)
    elif sensor_type.lower() == "force":
        value = force_sensor.force(sensor_port)

    else:
        raise ValueError(f"Unsupported sensor type: {sensor_type}")

    return value
