''' This program does not specifically complete any missions by itself.
Instead it:
- Is used at the start of runs in Red Base to collect coral, one krill and a sample,
- Serves as a backup program in case the bot fails to collect the "Unexpected Encounter" squid.
'''

import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def main():
    await ssl5k.forward(140, True, assist=True, velocity=2000)
    await ssl5k.forward(-200, True, assist=True, velocity=2000)

runloop.run(main())
