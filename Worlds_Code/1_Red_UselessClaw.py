from hub import port
import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def ripuselessstick():

    await ssl5k.forward(13,True, velocity=1000)
    await ssl5k.attachment(-400, "right", velocity=2000)
    await ssl5k.forward(-100, True, velocity=2000)
    await ssl5k.attachment(360, "right")

runloop.run(ripuselessstick())
