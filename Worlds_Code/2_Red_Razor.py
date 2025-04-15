''' This code completes the following missions:
- "M01 - Flip Coral Nursery Buds",
- "M04 - Grab Scuba Diver"

This code can score up to 40 pts.
'''

import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def main():
    await ssl5k.forward(30, True, assist=True)
    await ssl5k.turn(-90, True)
    await ssl5k.forward(47, True, assist=True)
    await ssl5k.turn(-83, True)
    await ssl5k.forward(15, True, assist=True)
    await ssl5k.attachment(200, "right")
    await ssl5k.forward(-15, True, assist=True)
    await ssl5k.turn(-90, True)
    await ssl5k.forward(25, True, assist=True)
    await ssl5k.turn(45, True)
    await ssl5k.forward(40, True, assist=True)

runloop.run(main())