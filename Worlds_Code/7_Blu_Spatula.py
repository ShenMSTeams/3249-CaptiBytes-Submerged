''' This code completes the following missions:
- "M11 - Sonar Discovery",
- "M13 - Change Shipping Lanes"

This code can score up to 50 pts.
'''

import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def main():
    await ssl5k.forward(10,True,assist=True)
    await ssl5k.turn(-37,True)
    await ssl5k.forward(58,True, assist=True)
    await ssl5k.attachment(200,"left", velocity=360)
    await ssl5k.attachment(-900,"left", velocity=-360)
    await ssl5k.attachment(200,"left", velocity=630)
    await ssl5k.forward(-10, True)
    await ssl5k.turn(-25,True)
    await ssl5k.attachment(-200,"right", velocity=630)
    await ssl5k.forward(-8, True)
    ssl5k.attachment(-230,"right", velocity=-630)
    await ssl5k.attachment(800,"right", velocity=-1500)
    await ssl5k.turn(-20, True)
    await ssl5k.attachment(200,"right", velocity=-1500)
    await ssl5k.forward(20,True, velocity=-6600)
    await ssl5k.turn(50, True)
    await ssl5k.forward(-50, velocity=700)

runloop.run(main())