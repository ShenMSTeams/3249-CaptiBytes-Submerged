from hub import light_matrix, motion_sensor, port
import motor_pair
import motor
import runloop

import math
import sys

print(sys.version)

# Some constants for calculations
d = 5.5    # Diameter of one wheel
r = 8      # Radius of turning (using one wheel)

# Takes distance in centimeters (cm), and stop (whether or not to stop moving after the instruction)
async def forward(dist:float,stop:bool=False,**kwargs):
    '''Move bot forwards by a number of centimeters.

    - `dist: float:` The distance in centimeters
    - `stop: bool:` Controls whether or not motors will be issued a stop command at the end of the function.
    - `**kwargs: dict[str, Unknown]:` Allows the user to pass acceleration/deceleration arguments optionally.

    Examples:
    ```
        forward(46)      # Move forwards 46 centimeters
        forward(-23)     # Move backwards
        forward(11,True) # Move forwards and stop at the end
    ```
    '''
    degrees = dist*(360.0/(math.pi*d))
    
    velocity = kwargs.get("velocity",360)
    if (degrees < 0):
        velocity = -1*velocity

    time = round((degrees/velocity)*1000)
    time = abs(time)

    print('FORWARD: degrees:{degrees},time:{time}, velocity:{velocity}'.format(degrees=degrees,time=time,velocity=velocity)) #Debug

    motor_pair.move(motor_pair.PAIR_1,0,velocity=velocity,**kwargs)
    await runloop.sleep_ms(time)

    if (stop == True):
        motor_pair.stop(motor_pair.PAIR_1)

# Takes angle of turn (theta), wheel (which wheel to turn with), and stop (whether or not to stop moving after the instruction)
async def turn(pivot_on:str,theta:int,stop:bool=False,**kwargs):
    '''Turn bot by a number of degrees.

    - `pivot_on: str:` The wheel that the bot will pivot on.
    - `theta: int:` The angle that the bot will turn.
    - `stop: bool:` Controls whether or not motors will be issued a stop command at the end of the function.
    - `**kwargs: dict[str, Unknown]:` Allows the user to pass acceleration/deceleration arguments optionally.

    Examples:
    ```
        turn("left",90)   # Pivot by 90° on the left wheel
        turn("left",-90)  # Pivot back by 90° on the left wheel
        turn("right",180) # Pivot by 180° on the right wheel 
    ```
    '''
    
    motion_sensor.reset_yaw(0)
    dist = (2*math.pi*r)*(theta/360.0)
    degrees = dist*(360.0/(math.pi*d))

    velocity = kwargs.get("velocity",360)
    if (degrees < 0):
        velocity = -1*velocity

    print('TURN: wheel:{pivot_on}, degrees:{degrees}, dist:{dist}, velocity:{velocity}'.format(pivot_on=pivot_on,degrees=degrees,dist=dist,velocity=velocity)) #Debug

    if (pivot_on == "right"):
        motor.stop(port.F,stop=1)
        motor.run(port.C,velocity,**kwargs)
        if (theta > 0):
            while (motion_sensor.tilt_angles()[0] < theta*10):
                await runloop.sleep_ms(1)
        elif (theta < 0):
            while (motion_sensor.tilt_angles()[0] > theta*10):
                await runloop.sleep_ms(1)

    elif (pivot_on == "left"):
        motor.stop(port.C,stop=1)
        motor.run(port.F,velocity,**kwargs)
        if (theta > 0):
            while (motion_sensor.tilt_angles()[0] < theta*10):
                await runloop.sleep_ms(1)
        elif (theta < 0):
            while (motion_sensor.tilt_angles()[0] > theta*10):
                await runloop.sleep_ms(1)

    if (stop == True):
        motor.stop(port.C)
        motor.stop(port.F)

    print('TURN ERROR:', theta*10, ' ', motion_sensor.tilt_angles()[0], ' ', (motion_sensor.tilt_angles()[0]-theta*10)/10)
    motion_sensor.reset_yaw(0)

# Example of what you could do using this code:
async def main():
    print("Hello World! -=- Welcome to the SuperSecretCode API")
    motor_pair.pair(motor_pair.PAIR_1,port.C,port.F)
    await turn("left",90)
    await turn("left",-90)
    await forward(20,True)
    await forward(-20)
    await turn("right",-90)
    await turn("right",90,True)

runloop.run(main())

