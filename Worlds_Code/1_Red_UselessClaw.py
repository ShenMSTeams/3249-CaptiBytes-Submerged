''' Code slot 1, run on Red Base, uses "Useless Claw" attachment.

This program does not specifically complete any missions by itself.

Instead, it:
1. Latches on to the "M15 Research Vessel" boat and takes it into Red Base.

Purpose of case 1: Place "Water Sample" inside for more points when docking the
    boat.
'''

import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def main():
    await ssl5k.forward(13, True, velocity=1000)
    await ssl5k.attachment(-400, "right", velocity=2000)
    await ssl5k.forward(-100, True, velocity=2000)
    await ssl5k.attachment(360, "right")

runloop.run(main())
