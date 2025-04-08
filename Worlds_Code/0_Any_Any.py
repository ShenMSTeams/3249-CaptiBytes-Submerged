''' Code slot 0, Any Base, can use any attachment.

This program does not specifically complete any missions by itself.

Instead, it:
1. Is used at the start of runs in Red Base to collect coral, one krill and 
    "Water Sample",
2. Serves as a backup program to retry collecting the squid from 
    "M09 Unexpected Encounter" in case the bot does not collect it the first 
    time.

Purpose of case 1: Krill is used in "M12 Feed the Whale", "Water Sample" is used
    in "M15 Research Vessel".

Purpose of case 2: The squid is used later in the run for completing 
    "M09 Unexpected Encounter - Cold Seep".
'''

import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def main():
    await ssl5k.forward(140, True, assist=True, velocity=2000)
    await ssl5k.forward(-200, True, assist=True, velocity=2000)

runloop.run(main())
