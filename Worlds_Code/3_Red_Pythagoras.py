import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def main():
    ssl5k.reset_gyro()
    await ssl5k.attachment(-5, "left", velocity=-360)
    await ssl5k.forward(20, True, assist=True)
    await ssl5k.turn(-87, True, assist=True)
    await ssl5k.forward(32, True, assitst=True)
    await ssl5k.turn(83, True, assist=True)
    await ssl5k.forward(26.5, True, assist=True)
    await ssl5k.forward(-9, True)
    ssl5k.reset_gyro()
    await ssl5k.turn(51, True)
    await ssl5k.forward(-400, True, assist=True, velocity=4000)
    await ssl5k.forward(2, True, assist=True, velocity=400)
    await ssl5k.forward(15.5, True, assist=True)
    await ssl5k.turn(-50, True, assist=True)
    await ssl5k.forward(11, True, assist=True)
    await ssl5k.attachment(300, "left",  velocity=45000)
    await ssl5k.turn(113, True, assist=True)
    await ssl5k.forward(80, True, assitst=True)
  
runloop.run(main())
