''' Code slot 8, run on Blue Base, uses "Squiddler" attachment.

This program completes the following missions:
- "M06 Angler Fish",
- "M09 Unexpected Encounter - Cold Seep",
- "M13 Change Shipping Lanes"
'''

import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def main():
    await ssl5k.forward(-5)
    await ssl5k.attachment(50,"Right")
    await ssl5k.forward(42, False, assist=True)
    await ssl5k.turn(30,True)
    await ssl5k.forward(5,True) 
    await ssl5k.attachment(200,"Right")
    await ssl5k.turn(60,True)
    await ssl5k.turn(-139,True)
    await ssl5k.attachment(300,"right", velocity=2000)
    await ssl5k.forward(70, True, assist=True, velocity=400)
    await ssl5k.attachment(300,"left")
    await ssl5k.forward(-20,True)
    await ssl5k.turn(-50,True)
    await ssl5k.forward(20,True)
    await ssl5k.forward(15,True)
    await ssl5k.forward(-15,True)

runloop.run(run())
