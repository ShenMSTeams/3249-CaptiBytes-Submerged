''' Code slot 3, run on Red Base, uses "Pythagoras" attachment.

This program completes the following missions:
- "M06 Raise the Mast",
- "M07 Kraken's Treasure"

In addition, it:
1. Attemps to place the scuba diver from "M04 Scuba Diver" on the 
    "M03 Coral Reef" coral reef support.

Purpose of case 1: Earns an extra 20pts if successful.
'''

import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def main():
    ssl5k.reset_gyro()
    await ssl5k.attachment(-5, "left", velocity=-360)
    await ssl5k.forward(22, True, assist=True)
    await ssl5k.turn(-87, True, assist=True)
    await ssl5k.forward(35.5, True)
    await ssl5k.turn(84, True, assist=True)
    await ssl5k.forward(28, True, assist=True, velocity=450)
    await ssl5k.forward(-10.3, True)
    ssl5k.reset_gyro()
    await ssl5k.turn(45, True)
    await ssl5k.forward(-400, True, assist=True, velocity=4000)
    await ssl5k.forward(17, True, assist=True)
    await ssl5k.turn(-54, True, assist=True)
    await ssl5k.forward(15, True, assist=True)
    await ssl5k.attachment(-700, "left", velocity=-45000)
    await ssl5k.turn(122, True, assist=True)
    await ssl5k.forward(80, True)

runloop.run(main())
