''' This code completes the following missions: 
- "M10 - Submersible", 
- "M09 - Unexpected Encounter",
- "M05 - Angler Fish" 

This code can score up to 80 pts.
'''
import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def main():
    await ssl5k.forward(-5)
    await ssl5k.attachment(60, "right")
    await ssl5k.forward(46, False, assist=True)
    await ssl5k.turn(35, True)
    await ssl5k.forward(5.7, True) 
    await ssl5k.attachment(200, "right")
    await ssl5k.turn(60, True)
    await ssl5k.turn(-124, True)
    await ssl5k.attachment(300, "right", velocity=2000)
    await ssl5k.forward(70, True, assist=True, velocity=400)
    await ssl5k.attachment(300, "left")
    await ssl5k.forward(-20, True)
    await ssl5k.turn(-53, True)
    await ssl5k.forward(20, True)
    await ssl5k.forward(20, True)
    await ssl5k.forward(-20, True)
  
runloop.run(main())