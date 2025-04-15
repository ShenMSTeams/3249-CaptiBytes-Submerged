''' This code completes the following missions:
- "M15 - Latch Research Vessel",
- "M15 - Research Vessel Cargo",
- "M08 - Artificial Habitat"

This code can score a total of 30 pts.
'''

import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def main():
    await ssl5k.attachment(30, "left", velocity=-1000)
    await ssl5k.turn(-15, True)
    await ssl5k.forward(80, True, velocity=1600, assist=True)
    await ssl5k.turn(200, True, velocity=1000)
    await ssl5k.forward(190,True,velocity=1440)
    await ssl5k.forward(-3, True)
    await ssl5k.attachment(-500, "left",velocity=500)
    await ssl5k.forward(-30, True)
    await ssl5k.attachment(300, "left", velocity=-360)
    await ssl5k.turn(-60, True, assist=True)
    await ssl5k.forward(39, True, velocity=720)
    await ssl5k.turn(95, True)
    await ssl5k.forward(100, True, velocity=720)

runloop.run(main())