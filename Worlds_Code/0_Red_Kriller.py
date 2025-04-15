''' This code completes the following missions:
- "M03 - Flip Coral Reef",
- "M03 - Collect Reef Segments",
- "M12 - Collect Krill",
- "M14 - Collect Water Sample"

This code can score up to 25 pts.
'''

import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def main():
    await ssl5k.forward(80,True, assist=True, velocity=700)
    await ssl5k.forward(-100,True, assist=True, velocity=700)

runloop.run(main())