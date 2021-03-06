import urllib3
import json
from . import BASE_API_GATEWAY, BASE_API_SERVER


def dataset(id_ruang: int) -> str():
    print("Downloading dataset...")
    http = urllib3.PoolManager()
    req = http.request("GET", BASE_API_SERVER + "/room/%i" % id_ruang)
    return req.data


def model(id_model: int):
    print("Downloading model...")
    http = urllib3.PoolManager()
    urlPath = "/api/model/download?id=%s" % id_model
    req = http.request("GET", BASE_API_GATEWAY + urlPath)
    return req.data

def validation_data(ruang: int, date_start: str, date_end: str):
    http = urllib3.PoolManager()
    urlPath = "/api/kuis/result?ruang=%s&start_date=%s&end_date=%s" % (ruang, date_start, date_end)
    req = http.request('GET', BASE_API_GATEWAY + urlPath)
    return json.loads(req.data)['surveys']