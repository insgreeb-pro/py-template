import urllib3

BASE_API_SERVER = "https://api.insgreeb.com"


def dataset(id_ruang: int) -> str():
    print("Downloading dataset...")
    http = urllib3.PoolManager()
    req = http.request("GET", BASE_API_SERVER + "/room/%i" % id_ruang)
    return req.data
