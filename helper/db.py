import urllib3
import json

from . import BASE_API_SERVER, BASE_API_GATEWAY


def save_to_db(id_task, status, input_data, output_data):
    http = urllib3.PoolManager()
    url = BASE_API_GATEWAY + "/api/ai/new-result"
    data = {
        "id_task": id_task,
        "status": status,
        "input": input_data,
        "output": output_data,
    }
    body = json.dumps(data).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    http.request("POST", url, body=body, headers=headers)


def upload(id_ruang, status):
    # TODO
    pass
