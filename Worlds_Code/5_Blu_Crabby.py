''' Code slot 5, run from Blue Base, uses "Crabby" attachment.

This program completes the following mission:
- "M08 Artificial Habitat"
'''

import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def main():
    await ssl5k.turn(3)
    await ssl5k.forward(46.7, True)
    await ssl5k.attachment(620, "right", velocity=-2000)
    await ssl5k.forward(-5, True, assist=True)
    await ssl5k.attachment(415, "right", velocity=460)
    await ssl5k.forward(18, True, assist=True)
    await ssl5k.attachment(130, "right", velocity=-600)
    await ssl5k.forward(-74, True, assist=True)

runloop.run(main())
