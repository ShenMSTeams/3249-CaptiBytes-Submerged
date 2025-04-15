''' This code completes the following missions:
- "M09 - Grab Unexpected Encounter"

This code can score a total of 20 pts.
'''

import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def squidkid():
    await ssl5k.forward(40,True, assist=True, velocity=700)
    await ssl5k.forward(-50,True, assist=True, velocity=700)

runloop.run(squidkid())