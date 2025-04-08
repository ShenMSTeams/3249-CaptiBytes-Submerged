'''Gets estimated battery percent based on data from our bots.'''

from hub import battery_voltage
from hub import light_matrix
from hub import light

import color

voltage = battery_voltage()
soc = 0.0512*voltage + -323
avg_error = -0.3

if voltage < 7349:
    soc = 0.134*voltage + -929
    avg_error = 3.2
elif voltage < 7199:
    soc = 0.0953*voltage + -657
    avg_error = -0.1

soc = round(soc, 2) # Use two decimal places when showing in output.
light_matrix_soc = round(soc) # Use no decimal places when displaying on hub.

if voltage < 7022:
    soc = "LOW"

print("SoC is (about):", soc, "%   +/-", avg_error, "%")

light_matrix.write(str(light_matrix_soc), 100, 1000)
if soc == "LOW":
    while True:
        light.color(0, color.RED)
        light.color(0, color.BLACK)
