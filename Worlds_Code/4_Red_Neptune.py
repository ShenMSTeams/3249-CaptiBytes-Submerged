''' Code slot 4, run from Red Base, uses "Neptune" attachment.

(No Info)

NOTE: Not currently in use.
'''

import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def run():
    await ssl5k.turn(-34,True)
    await ssl5k.forward(60,True, assit=True)
    await ssl5k.turn(-29,True)
    await ssl5k.forward(20,True, assit=True)
    await ssl5k.forward(-4,True, assit=True)
    await ssl5k.turn(-25,True)
    await ssl5k.attachment(500, "Right", velocity=-500)
    await ssl5k.forward(-4,True, assit=True)
    await ssl5k.attachment(400, "Right", velocity=300)
  
runloop.run(run())
