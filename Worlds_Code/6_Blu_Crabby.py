import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)
ssl5k.forward_assist=True

async def ripuselessstick():
    await ssl5k.turn(3)
    await ssl5k.forward(46.7,True,assist=True)
    await ssl5k.attachment(620,"right", velocity=-2000)
    await ssl5k.forward(-5,True,assit=True)
    await ssl5k.attachment(415, "right", velocity=460)
    await ssl5k.forward(18,True,assit=True)
    await ssl5k.attachment(130,"right", velocity=-600)
    await ssl5k.forward(-74,True,assist=True)

runloop.run(ripuselessstick())
