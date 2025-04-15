''' This code completes the following missions:
- "M08 - Artificial Habitat"

This code can score up to 40 pts.
'''

import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def main():
    await ssl5k.turn(3)
    await ssl5k.forward(46.7, True, assist=True)
    await ssl5k.attachment(620, "right", velocity=-4000)
    await ssl5k.forward(-5, True)
    await ssl5k.attachment(500, "right", velocity=1000)
    await ssl5k.forward(14, True)
    await ssl5k.attachment(700, "right", velocity=-4000)
    await ssl5k.forward(-5, True)
    await ssl5k.attachment(700, "right", velocity=4000)
    await ssl5k.turn(-10)
    await ssl5k.forward(5, True)
    await ssl5k.attachment(700, "right", velocity=-4000)
    await ssl5k.turn(-20)
    await ssl5k.forward(-74, True, assist=True)

runloop.run(main())
