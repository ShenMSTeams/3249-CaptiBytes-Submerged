import time

from hub import battery_current, battery_voltage
from hub import port
from hub import motion_sensor
import motor
import runloop

current_under_load = 490.3  # Run the bot on full load (all ports duty cycle 10000) and put the battery_current number here.
load_time = round(105/current_under_load*3600) * 1000

ms_start = time.ticks_ms()

gyro = motion_sensor.tilt_angles
accel = motion_sensor.acceleration


async def data_collector():
    '''Gets data:\n
        All Gyro axes, \n
        All accelerometer axes,\n
        Battery current  (mA),\n
        Battery voltage  (mV),\n
        Time since start (ms)'''
    print("-- Beginning testing! --")

    with open("/flash/all_data.csv", "w") as f:
        f.write("GyroYaw,GyroPitch,GyroRoll,AccelX,AccelY,AccelZ,Current,Voltage,Time\n")

    while True:
        with open("/flash/all_data.csv", "a") as f:
            f.write("{gyroyaw},{gyropitch},{gyroroll},{accelx},{accely},{accelz},{current},{voltage},{time_ms}\n"
                    .format(gyroyaw=gyro()[0], gyropitch=gyro()[1], gyroroll=gyro()[2],
                            accelx=accel(False)[0], accely=accel(False)[1], accelz=accel(False)[2],
                            current=battery_current(), voltage=battery_voltage(), time_ms=time.ticks_ms()-ms_start))

        await runloop.sleep_ms(1000)  # Sleep for 1 second


async def run_load():
    while True:
        await load_on()
        await runloop.sleep_ms(load_time)
        await load_off()
        await runloop.sleep_ms(20000)  # Sleep for 20 seconds (20*1000 milliseconds)


async def load_on():
    print("Load turned on  [1]")
    motor.run(port.B, 360)
    motor.run(port.C, 360)
    motor.run(port.D, 360)
    motor.run(port.F, 360)


async def load_off():
    print("Load turned off [0]")
    motor.stop(port.B)
    motor.stop(port.C)
    motor.stop(port.D)
    motor.stop(port.F)

runloop.run(run_load(), data_collector())
