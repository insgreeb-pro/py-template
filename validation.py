from sys import argv
from helper.downloader import validation_data, model
from preprocessing_dataprediksi import preprocess

import pickle
import json

import tes_app as app

# example running
# python validation.py <id_ruang> <id_model> <date_start> <date_end>
# python validation.py 2 8 2020-02-21T11:00:21 2020-02-28T11:00:24
# argv = [2,  "2", "8", "2020-02-21T11:00:21", "2020-02-28T11:00:24"]

if __name__ == "__main__":
    _, ID_RUANG, ID_MODEL, DATE_START, DATE_END = argv

    data = validation_data(ID_RUANG, DATE_START, DATE_END)

    data_model = pickle.loads(
        model(int(ID_MODEL)) 
    ) 

    model_type = ['sensasi', 'kenyamanan', 'penerimaan']
    soal_type = ['soal1', 'soal3', 'soal4']

    result = {}
    kuesioner = {}

    for i in model_type:
        result[i] = []
        kuesioner[i] = []

    kuesioner['ids'] = []

    for single in data:
        kuesioner['ids'].append(single['id'])

        s = {
            "datetime": single['created_at'],
            "data_dasar": [single['data_dasar']],
            "data_sensor": single['data_sensor']
        }
        isField7 = 0 if single['data_sensor']['indoor']['field7'] else 1
        processed = preprocess(s, isField7)
        out = app.main(processed, data_model)[0]

        for i, soal in zip(model_type, soal_type):
            kuesioner[i].append(
                single[soal]
            )
            try:
                result[i].append(out[i][0])
            except:
                result[i].append(None)

    output = {
        "hasil_prediksi": result,
        "hasil_kuesioner": kuesioner
    }
    print(
        json.dumps(output)
    )