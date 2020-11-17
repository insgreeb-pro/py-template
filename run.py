from helper.db import save_to_db
from helper.downloader import model
import json
import sched
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

TIME_DELAY = 5 * 60

if __name__ == "__main__":
    _, ID_TASK, ID_RUANG, ID_MODEL = argv

    model = downloader.model(ID_MODEL)

    def run():
        data = json.loads(
            downloader.dataset(int(ID_RUANG))
        )
        data_output, status = app.main(data, model)
        save_to_db(ID_TASK, status, data, data_output)

    # SECHEDULER
    s = sched.scheduler(time.time, time.sleep)

    def do_something(sc):
        run()
        s.enter(TIME_DELAY, 1, do_something, (sc,))

    s.enter(TIME_DELAY, 1, do_something, (s,))
    s.run()
