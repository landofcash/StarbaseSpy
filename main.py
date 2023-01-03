import asyncio
import winsound
import stationSpy
from datetime import datetime
import config
import requests


def sound_alarm():
    for i in range(0, 3):
        winsound.Beep(2000, 100)
        for j in range(0, 3):
            winsound.Beep(2000, 400)
            for k in range(0, 3):
                winsound.Beep(2000, 100)


def send_ping():
    response = requests.get(config.settings["url"]+"/ping",
                             params={"name":config.settings["name"],"location":config.settings["location"]},
                             verify=False)
    print("response:", response)


def send_new():
    response = requests.get(config.settings["url"]+"/new",
                             params={"name":config.settings["name"],"location":config.settings["location"]},
                             verify=False)
    print("response:", response)


def send_image(file_name):
    with open(file_name, "rb") as a_file:
        multipart_form_data = {
            'upload': ('image.png', a_file)
        }
        response = requests.post(config.settings["url"]+"/upload",
                                 files=multipart_form_data,
                                 params={'name':config.settings["name"],'location': config.settings["location"]},
                                 verify=False)
        print("response:", response)


async def monitor():
    last_ping=datetime.now()
    send_new()
    print(f"Bot Started: {config.settings['name']} @ {config.settings['location']}")
    while True:
        try:
            if (datetime.now()-last_ping).total_seconds()>60:
                last_ping = datetime.now()
                send_ping()
            t = datetime.now().strftime("%m-%d-%Y--%H-%M-%S")
            images_folder = config.settings["images_folder"]
            alarm = await stationSpy.act(t, images_folder, config.settings["window_name"])
            if alarm:
                send_image(f'{images_folder}/2.png')
                if config.settings["sound_alarm"]:
                    sound_alarm()
        except Exception as err:
            print(f"Error {type(err)}: {err}")


if __name__ == '__main__':
    asyncio.run(monitor())