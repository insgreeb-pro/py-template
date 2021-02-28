import urllib3
import json

from . import BASE_API_SERVER, BASE_API_GATEWAY, env


def save_to_db(id_task, status, input_data, output_data):
    """
    Deprecated
    reason: result tidak perlu disimpan lagi
    """
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


def upload(id_ruang, id_task, status):
    if env.IS_UPLOAD_STATUS:
        http = urllib3.PoolManager()
        url = BASE_API_SERVER + "/room/status"
        data = {
            "id_task": id_task,
            "status": status,
            "id_ruang": id_ruang
        }
        body = json.dumps(data).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        http.request("POST", url, body=body, headers=headers)
        return True
    return False
