''' This code completes the following missions:
- "M14 - Sample Collection Trident",
- "M04 - Drop Off Shark"

This code can score up to 40 pts.
'''

import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def main():
    await ssl5k.forward(55, True, velocity=1000)
    await ssl5k.turn(-50, True)
    await ssl5k.forward(6, True, velocity=1000)
    await ssl5k.attachment(-300, "left", velocity=1000)
    await ssl5k.forward(-18, True, velocity=1000)
    await ssl5k.attachment(-500, "left", velocity=-1000)
    await ssl5k.forward(26, True, velocity=1000)
    await ssl5k.forward(-22, True, velocity=1000)
    await ssl5k.turn(-130, True)
    await ssl5k.forward(70, True, velocity=1000)

runloop.run(main())