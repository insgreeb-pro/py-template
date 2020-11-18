import pickle
from helper.env import TELEGRAM_CHANNEL, TELEGRAM_TOKEN
from helper import telegram
from helper.db import save_to_db
from helper.downloader import model
import json
import schedule
import time
from sys import argv
from helper import downloader
import app

"""
command:
python run.py <task_id> <room_id> <model_id>

ex:
python run.py 1 2 7
"""

TIME_DELAY = 5  # minutes

if __name__ == "__main__":
    _, ID_TASK, ID_RUANG, ID_MODEL = argv
    try:
        model = pickle.loads(
            downloader.model(ID_MODEL)
        )

        def run():
            data = json.loads(
                downloader.dataset(int(ID_RUANG))
            )
            data_output, status = app.main(data, model)
            save_to_db(ID_TASK, status, data, data_output)

        # Secheduller
        schedule.every(TIME_DELAY).minutes.do(run)
        while(True):
            schedule.run_pending()
            time.sleep(1)

    except Exception as e:
        # Error Notification
        msg = telegram.msg_generator(ID_TASK, e)
        telegram.push(
            msg, TELEGRAM_TOKEN, TELEGRAM_CHANNEL
        )
