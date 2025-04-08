''' Code slot 4, run from Red Base, uses "Useless Transporter attachment.

This program completes the following missions:
- "M15 Research Vessel",
- "M09 Unexpected Encounter - Unknown Creature"

In addition, it:
1. Sets up "M08 Artificial Habitat" cages in a square formation.

Purpose of case 1: Later in the run, the bot will attempt to flip these cages
    in a way that all crabs are facing up, totaling 40pts.
'''

import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def main():
    await ssl5k.attachment(30, "left", velocity=-1000)
    await ssl5k.forward(80, True, velocity=1600)
    await ssl5k.turn(200, True, velocity=1000)
    await ssl5k.forward(190,True,velocity=1440)
    await ssl5k.forward(-3, True)
    await ssl5k.attachment(-500, "left",velocity=500)
    await ssl5k.forward(-30, True)
    await ssl5k.attachment(300, "left", velocity=-360)
    await ssl5k.turn(-60, True)
    await ssl5k.forward(30, True)
    await ssl5k.turn(140, True, velocity=1440)
    await ssl5k.forward(35, True, velocity=1440)
    await ssl5k.turn(-600, True, velocity=2000)
    await ssl5k.turn(40, True)
    await ssl5k.forward(50, True, velocity=1440)

runloop.run(main())
