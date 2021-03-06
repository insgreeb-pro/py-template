import pickle
from helper import telegram, db, processing
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
        
        comfort_status = processing.calculateComfort(data_output)
        db.upload(ID_RUANG, ID_TASK, comfort_status)

    try:
        run()  # first running
    except Exception as e:
        telegram.errorNotification(ID_TASK, e, data_input)

    # Scheduler
    schedule.every(TIME_DELAY).minutes.do(run)
    while(True):
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            telegram.errorNotification(ID_TASK, e, data_input)
