''' Code slot 2, run on Red Base, uses "Razor" attachment.

This program completes the following missions:
- "M01 Coral Nursery - Coral Buds",
- "M04 Scuba Diver"
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
    await ssl5k.attachment(200, "right", valocity=100)
    await ssl5k.forward(-15, True, assist=True)
    await ssl5k.turn(-90, True)
    await ssl5k.forward(25, True, assist=True)
    await ssl5k.turn(45, True)
    await ssl5k.forward(40, True, assist=True)

runloop.run(main())
