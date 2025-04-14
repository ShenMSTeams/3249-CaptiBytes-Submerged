import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def main():
 await ssl5k.forward(80,True, assist=True, velocity=700)
 await ssl5k.forward(-100,True, assist=True, velocity=700)

runloop.run(main())
