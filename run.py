from os import name
import pickle
from helper.env import TELEGRAM_CHANNEL, TELEGRAM_TOKEN
from helper import telegram, db
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
data_input = {}

if __name__ == "__main__":
    _, ID_TASK, ID_RUANG, ID_MODEL = argv
    try:
        model = pickle.loads(
            downloader.model(ID_MODEL)
        )

        def run():
            global data_input
            data_input = json.loads(
                downloader.dataset(int(ID_RUANG))
            )
            data_output, status = app.main(data_input, model)
            db.save_to_db(ID_TASK, status, data_input, data_output)

        run()  # first running

        # Secheduller
        schedule.every(TIME_DELAY).minutes.do(run)
        while(True):
            schedule.run_pending()
            time.sleep(1)

    except Exception as e:
        # Error Notification
        msg = telegram.msg_generator(ID_TASK, e)
        telegram.push(msg)
        telegram.sendFile(json.dumps(data_input), name="input_data.json")
