import urllib3
import urllib.parse
import os.path
import sys
import traceback


def push(m, token, channel):
    baseurl = "https://api.telegram.org/bot"
    q = "/sendMessage?chat_id=%s&text=" % channel
    http = urllib3.PoolManager()
    r = http.request("GET", baseurl + token + q + urllib.parse.quote_plus(m))
    return r.data


def msg_generator(ID_TASK, e):
    msg = "TASK ERROR\n"
    msg += "-"*10 + "\n"

    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

    msg += "Type: %s\n" % exc_type
    msg += "Position: %s:%s\n" % (fname, exc_tb.tb_lineno)
    msg += "ID: %s\nMESSAGE: \n\n%s\n\n%s" % (
        ID_TASK, str(e), traceback.format_exc())
    return msg
