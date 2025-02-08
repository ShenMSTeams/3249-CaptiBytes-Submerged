from hub import light_matrix, motion_sensor, port
import color
import color_sensor
import motor_pair
import motor
import runloop


import time
import math
import sys


def ssl5k_ver():
    print(sys.version)
    print("Welcome to SuperSecretLib5000!")
    print("ssl5k ver 1.3.CHAMPS")


# Constants used in calculations
d = 6.1# Diameter of a single wheel (OLD)
r = 5# Pivot Radius (OLD)


async def forward(dist:float,stop:bool=False,run_until=None,**kwargs):
    '''Move bot forwards by a number of centimeters.


    - `dist: float:` The distance in centimeters
    - `stop: bool:` Controls whether or not motors will be issued a stop command at the end of the function.
    - `**kwargs: dict[str, Unknown]:` Allows the user to pass velocity and acceleration/deceleration arguments optionally.


    Examples:
    ```
        forward(46)    # Move forwards 46 centimeters
        forward(-23)    # Move backwards
        forward(11,True) # Move forwards and stop at the end
    ```
    '''
    if run_until is None:
        run_until = lambda: False


    degrees = dist*(360.0/(math.pi*d))


    acceleration = kwargs.get("acceleration", False)
    velocity = kwargs.get("velocity",360)
    if (degrees < 0):
        velocity = -1*velocity


    run_time = round((degrees/velocity)*1000.0)
    run_time = abs(run_time)


    print("dist:{dist}, degrees:{degrees}, velocity:{velocity}, time:{time}"
    .format(dist=dist,degrees=degrees,velocity=velocity,time=time))


    motor_pair.move(motor_pair.PAIR_1,0,velocity=velocity,acceleration=acceleration)
    start = time.ticks_ms()
    while True:
        if run_until():
            break
        now = time.ticks_ms()
        if now-start > run_time:
            break


    if (stop == True):
        motor_pair.stop(motor_pair.PAIR_1)


async def turn(theta:int,stop:bool=False,run_until=None,**kwargs):
    '''Turn bot by a number of degrees.


    - `theta: int:` The angle that the bot will turn.
    - `stop: bool:` Controls whether or not motors will be issued a stop command at the end of the function.
    - `**kwargs: dict[str, Unknown]:` Allows the user to pass velocity and acceleration/deceleration arguments optionally.


    Examples:
    ```
        ssl5k.turn(90)    # Turn 90° right.
        ssl5k.turn(-90)    # Turn 90° left.
        ssl5k.turn(180,True) # Turn 180° right and stop at the end.
    ```
    '''
    if run_until is None:
        run_until = lambda: False


    motion_sensor.reset_yaw(0)


    dist = (2*math.pi*r)*(theta/360.0) # r is now 5.5
    degrees = dist*(360.0/(math.pi*d))


    velocity = int(kwargs.get("velocity",360)/2) # Half velocity for tank movement.
    if (degrees < 0):
        velocity = -1*velocity


    run_time = round((degrees/velocity)*1000)
    run_time = abs(run_time) # Ensures that time is greater than 0


    print("""DEBUG:
    -[INPUT]- theta: {theta}, velocity: {velocity}, stop: {stop}
    -[OUTPUT]- dist: {dist}, degrees: {degrees}, time: {time}"""
    .format(theta=theta, velocity=velocity, stop=stop, dist=dist, degrees=degrees, time=time))


    motor_pair.move_tank(motor_pair.PAIR_1,velocity,-1*velocity)
    start = time.ticks_ms()
    while True:
        if run_until():
            break
        now = time.ticks_ms()
        if now-start > run_time:
            break


    if (stop == True):
        motor_pair.stop(motor_pair.PAIR_1)


    yaw = -1*motion_sensor.tilt_angles()[0]
    print("TURN INFO: theta: {theta}, yaw: {yaw}, error: {error}"
    .format(theta=theta,yaw=yaw,error=yaw-theta))


async def attachment(degrees:int,attach_port:str):
    '''Run attachment motor for a number of degrees.


    - `degrees: int:` Number of degrees to run the motor for.
    - `attach_port: str:` Attachment motor to run. Left/Right/Both


    Examples:
    ```
        attachment(30,"both")
        attachment(360,"left")
        attachment(-360,"right")
    ```
    '''


    if attach_port == "left" :
        await motor_pair.move_tank_for_degrees(motor_pair.PAIR_2,degrees,360,0)
    if attach_port == "right":
        await motor_pair.move_tank_for_degrees(motor_pair.PAIR_2,degrees,0,360)
    if attach_port == "both" :
        await motor_pair.move_tank_for_degrees(motor_pair.PAIR_2,degrees,360,360)


    print("Attachment: {degrees}, {attach_port}".format(degrees=degrees,attach_port=attach_port))


async def sensor(sensor_type:str,sensor_port:int,expected:int):
    '''Checks for an expected value until the value is met.


    - `sensor_type: str:` The type of sensor used. Color/Distance/Force/etc.
    - `sensor_port: str:` Sensor to detect with. Left/Right/Both
    - `expected_value: int:` The value you are checking for.


    Examples:
    ```
        black = sensor("color","both",0) # black will be 'False' until the color sensors see black
        yellow = sensor("color","left",7) # yellow will be 'False' until the left color sensor sees yellow
    ```
    '''
   
    if sensor_type.lower() == "color":
        value = color_sensor.color(sensor_port)
        return value == expected
    # We only have color sensors implemented at the moment..


# Setup function to automatically create motor pairs:
def init(drive_left,drive_right,attach_left,attach_right,sensor_left,sensor_right):
    ssl5k_ver()
    motor_pair.pair(motor_pair.PAIR_1,drive_left,drive_right)
    motor_pair.pair(motor_pair.PAIR_2,attach_left,attach_right)
    return drive_left,drive_right,attach_left,attach_right,sensor_left,sensor_right


async def test(testid: str):
    if (__name__ == "__main__"):
        if (testid == "turns"):
            ports = init(port.C,port.F,port.B,port.D,port.A,port.E)
            print("Left wheel: {0}, Right wheel: {1}, Left attachment motor: {2}, Right attachment motor: {3}, Left sensor: {4}, Right Sensor: {5}"
            .format(ports[0],ports[1],ports[2],ports[3],ports[4],ports[5]))
            await attachment(-360,"right")
            _run_until = lambda: sensor("color",ports[4],0)
            await forward(50,True,run_until=_run_until)
            #await turn(90,True)
            #await turn(-90,True)
            #await turn(180,True)
            #await turn(-180,True)
            #await turn(360,True)
            #await turn(-360,True)


runloop.run(test('turns'))
