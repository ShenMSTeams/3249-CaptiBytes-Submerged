import SuperSecretLib5000 as ssl5k
import runloop

ssl5k.init(use_json=True)

async def dinner():
    def black():
        if ssl5k.sensor("color", "left") == 0 and ssl5k.sensor("color", "left") == 0:
            return True

    await ssl5k.forward(40, True, assist=True)
    await ssl5k.turn(-30, False)
    await ssl5k.forward(26, True, assist=True)
    await ssl5k.turn(47, True)
    await ssl5k.forward(13, True, run_until=black)

async def feed_the_beast():
    await ssl5k.attachment(360, "left", velocity=-360)

async def dont_unfeed_the_beast():
    await ssl5k.attachment(-360, "left", velocity=360)

async def go_to_sonar():
    await ssl5k.forward(-30, True)
    await ssl5k.turn(-50)
    await ssl5k.forward(-100, True)


runloop.run(dinner())
runloop.run(feed_the_beast())
runloop.run(dont_unfeed_the_beast())
runloop.run(go_to_sonar())
