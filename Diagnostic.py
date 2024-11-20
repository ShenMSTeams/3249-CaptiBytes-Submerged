'''
IDEAS:

Stream output to a file?

add runloop.sleep_ms(1) in between everything in the main function (async io is mad)
'''

from hub import light_matrix, motion_sensor, port
import motor_pair
import motor
import runloop

import hub

import random
import math
import sys

print(sys.version)

error = []

d = 5.5 # Diameter of one wheel
r = 8   # Radius of turning (using one wheel)

async def turn(pivot_on:str,theta:int,stop:bool=False,**kwargs):
    '''Turn bot by a number of degrees.

    - `pivot_on: str:` The wheel that the bot will pivot on.
    - `theta: int:` The angle that the bot will turn.
    - `stop: bool:` Controls whether or not motors will be issued a stop command at the end of the function.
    - `**kwargs: dict[str, Unknown]:` Allows the user to pass acceleration/deceleration arguments optionally.

    Examples:
    ```
        turn("left",90)# Pivot by 90° on the left wheel
        turn("left",-90)# Pivot back by 90° on the left wheel
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

    global error
    global pivot
    pivot = pivot_on

    motion_sensor.reset_yaw(0)

async def main():
    for i in range(100):
        randtheta = random.randint(-179,180)
        print(i)
        print("This theta:", randtheta)
        await turn("left",randtheta)
        error.append(["i:{i}, theta:{thistheta}, yaw:{yaw}, wheel:{pivot}, error:{degree_error}"
        .format(i=i,thistheta=randtheta,yaw=motion_sensor.tilt_angles()[0],pivot=pivot,degree_error=(motion_sensor.tilt_angles()[0]-randtheta*10)/10)])
        print(error)
        print("---")
        motion_sensor.reset_yaw(0)

    error.append("\nNEXT\n")

    for i in range(100):
        randtheta = random.randint(-180,180)
        print(i)
        print("This theta:", randtheta)
        await turn("right",randtheta)
        error.append(["i:{i}, theta:{thistheta}, yaw:{yaw}, wheel:{pivot}, error:{degree_error}"
        .format(i=i,thistheta=randtheta,yaw=motion_sensor.tilt_angles()[0],pivot=pivot,degree_error=(motion_sensor.tilt_angles()[0]-randtheta*10)/10)])
        for row in error:
            print("row\n")
        print("---")

    original_stdout = sys.stdout
    
    with open('diagnostic_op.txt','w') as f:
        sys.stdout = f
        for row in error:
            print(','.join(row))
        
        sys.stdout = original_stdout

runloop.run(main())

