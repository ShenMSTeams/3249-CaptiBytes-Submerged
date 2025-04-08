import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def run():
    ssl5k.reset_gyro()
    await ssl5k.attachment(-5, "left", velocity=-360)
    await ssl5k.forward(22,True, assist=True)
    await ssl5k.turn(-87,True,assist=True)
    await ssl5k.forward(35.5,True,assitst=True)
    await ssl5k.turn(84,True,assist=True)
    await ssl5k.forward(28, True, assist=True,velocity=450)
    await ssl5k.forward(-10.3, True)
    ssl5k.reset_gyro()
    await ssl5k.turn(45, True)
    await ssl5k.forward(-400, True, assist=True, velocity=4000)
    await ssl5k.forward(17, True, assist=True)
    await ssl5k.turn(-54,True,assist=True)
    await ssl5k.forward(15, True, assist=True)
    await ssl5k.attachment(-700, "left",  velocity=-45000)
    await ssl5k.turn(122,True,assist=True)
    await ssl5k.forward(80,True,assitst=True)

runloop.run(run())
