''' Code slot 1, Red Base, uses 'Useless Claw' attachment.
This program does not complete any missions on its own.
Instead, it:
'''

import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def main():

    await ssl5k.forward(13,True, velocity=1000)
    await ssl5k.attachment(-400, "right", velocity=2000)
    await ssl5k.forward(-100, True, velocity=2000)
    await ssl5k.attachment(360, "right")

runloop.run(main())
