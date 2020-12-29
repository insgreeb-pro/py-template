import pickle
from helper import telegram, db
import json
import schedule
import time
from sys import argv
from helper import downloader
import tes_app as app
from preprocessing_dataprediksi import preprocess

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
            raw = json.loads(
                downloader.dataset(int(ID_RUANG))
            )
            data_input = preprocess(raw)
            data_output, status = app.main(data_input, model)
            db.save_to_db(ID_TASK, status, data_input, data_output)
            db.upload(ID_RUANG, ID_TASK, status)

        run()  # first running

        # Scheduler
        schedule.every(TIME_DELAY).minutes.do(run)
        while(True):
            schedule.run_pending()
            time.sleep(1)

    except Exception as e:
        # Error Notification
        msg = telegram.msg_generator(ID_TASK, e)
        telegram.push(msg)
        telegram.sendFile(json.dumps(msg), name="error.txt")
        telegram.sendFile(json.dumps(data_input), name="input_data.json")
