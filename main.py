import asyncio
import winsound
import stationSpy
from datetime import datetime
import config

async def monitor():
    while True:
        t = datetime.now().strftime("%m-%d-%Y--%H-%M-%S")
        alarm = await stationSpy.act(t, config.settings["window_name"])
        if alarm:
            for i in range(0, 3):
                winsound.Beep(2000, 100)
                for j in range(0, 3):
                    winsound.Beep(2000, 400)
                    for k in range(0, 3):
                        winsound.Beep(2000, 100)
if __name__ == '__main__':
    asyncio.run(monitor())
