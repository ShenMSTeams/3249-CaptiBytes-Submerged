import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def main():
    await ssl5k.forward(20, True, assist=True)
    await ssl5k.turn(-30, True)
    await ssl5k.forward(44, True, assist=True)
    await ssl5k.turn(82, True)
    await ssl5k.forward(30, True, assist=True)
    await ssl5k.forward(-30, True, assist=True)
    await ssl5k.turn(-100, True)
    await ssl5k.forward(-65, True, assist=True)

runloop.run(main())
