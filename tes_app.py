import preprocessing_dataprediksi
# import pandas as pd
import glob
import pickle
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score
# from sklearn import metrics

import json
# from sklearn.preprocessing import LabelEncoder
#from dateutil import parser
# import os.path

from helper import downloader


def main(data, model):
    status_nyaman = []
    # Ngambil data yang mau diprediksi
    data_personal = data['data_personal']
    data_latar_belakang=data['data_latar_belakang']
    sensor_indoor = data['sensor_indoor']
    sensor_outdoor = data['sensor_outdoor']
    status_model = True

    # Cek semua kondisi data input ke model
    status_personal = True if len(data_personal) != 0 else False
    status_lb = True if len(data_latar_belakang) !=0 else False
    status_indoor = True if len(sensor_indoor) != 0 else False
    status_outdoor = True if len(sensor_outdoor) != 0 else False
    
    status = [status_personal,status_lb,status_indoor,status_outdoor]
    #print(data)    
    # Nampung semua data akhir
    prediksi_sensasi = []
    prediksi_kenyamanan = []
    prediksi_penerimaan = []
    count_data_excluded = 0

    if all(status) and status_model:
        model_sensasi, model_kenyamanan, model_penerimaan,scaler = model
        scaler_sensasi,scaler_kenyamanan,scaler_penerimaan = scaler

        data_dasar = list(zip(data_personal,data_latar_belakang))
        for data_personal_satu,data_lb_satu in data_dasar:            
            cek_none_personal = any(x is None for x in data_personal_satu)
            cek_none_latar = any(x is None for x in data_lb_satu)

            # Prediksi per orang yang ada di ruangan khusus yang ada datanya saja
            if cek_none_personal == False and cek_none_latar == False:
                # Prediksi sensasi termal
                data_prediksi_sensasi = [data_personal_satu + \
                    data_lb_satu+sensor_indoor+sensor_outdoor]
                
                #Kalo modelnya ANN, data input dinormalisasi terlebih dahulu
                if type(model_sensasi).__name__ == 'MLPClassifier':
                    #print(data_prediksi_sensasi)
                    data_prediksi_sensasi = scaler_sensasi.transform(data_prediksi_sensasi)
                    #print(data_prediksi_sensasi)
                    #print('Scaling...')
                
                elif type(model_sensasi).__name__ != 'MLPClassifier':
                    pass
                
                output_sensasi = int(
                    model_sensasi.predict(data_prediksi_sensasi))

                # Prediksi kenyamanan termal
                data_prediksi_kenyamanan = [data_personal_satu+[output_sensasi]]
                
                if type(model_kenyamanan).__name__ == 'MLPClassifier':
                    data_prediksi_kenyamanan = scaler_kenyamanan.transform(data_prediksi_kenyamanan)
                    #print('Scaling...')
                    
                elif type(model_kenyamanan).__name__ != 'MLPClassifier':
                    pass
                
                output_kenyamanan = int(
                    model_kenyamanan.predict(data_prediksi_kenyamanan))

                # Prediksi penerimaan termal
                data_prediksi_penerimaan = [data_personal_satu + \
                    [output_sensasi]+[output_kenyamanan]]
                
                if type(model_penerimaan).__name__ == 'MLPClassifier':
                    data_prediksi_penerimaan = scaler_penerimaan.transform(data_prediksi_penerimaan)
                    #print('Scaling...')
                    
                elif type(model_penerimaan).__name__ != 'MLPClassifier':
                    pass
                
                output_penerimaan = int(
                    model_penerimaan.predict(data_prediksi_penerimaan))

                # Masukin buat output akhir
                prediksi_sensasi.append(output_sensasi)
                prediksi_kenyamanan.append(output_kenyamanan)
                prediksi_penerimaan.append(output_penerimaan)

            # Yang datanya None, outputnya None juga
            elif cek_none_personal or cek_none_latar:
                count_data_excluded += 1

        print('Prediksi sensasi = ', prediksi_sensasi)
        print('Prediksi kenyamanan = ', prediksi_kenyamanan)
        print('Prediksi penerimaan = ', prediksi_penerimaan)
        print('Total', count_data_excluded, 'data excluded')

        # Output akhir untuk thermal comfort level satu ruang
        # Parameter : Kenyamanan dan Penerimaan

        # Hitung berapa persen yang nyaman (sementara pake penerimaan dulu)
        # percentage_nyaman=(prediksi_kenyamanan.count(1)/len(prediksi_kenyamanan))*100
        percentage_penerimaan = (prediksi_penerimaan.count(
            1)/len(prediksi_penerimaan))*100

        if percentage_penerimaan >= 80:
            status_nyaman.append("Nyaman")
        elif 60 <= percentage_penerimaan < 80:
            status_nyaman.append("Netral") 
        elif percentage_penerimaan < 60:
            status_nyaman.append("Tidak nyaman")
        print("Status = ", status_nyaman)

    #Jika tidak ada eror di orang dan/sensor
    elif not all(status) and status_model:
       
        error_msg=[i for i in range(len(status)) if status[i] == 0]
        status_nyaman.append('No data')
        #print(error_msg)
        for error in error_msg:
            if error == 0:
                status_nyaman.append('Empty room')
                print('No data : Empty room')
            elif error == 2:
                status_nyaman.append('Indoor sensors')
                print('No data : Indoor sensors')
            elif error == 3:
                status_nyaman.append('Outdoor sensors')
                print('No data : Outdoor sensors')
                
    elif all(status) and not status_model:
        print('Model tidak ditemukan')

    return {
        "sensasi": prediksi_sensasi,
        "kenyamanan": prediksi_kenyamanan,
        "penerimaan": prediksi_penerimaan,
        "status": status_nyaman
    }, status_nyaman


if __name__ == '__main__':

    ID_RUANG: int = 2

    data = json.loads(
        downloader.dataset(ID_RUANG)
    )
    data_prediksi = preprocessing_dataprediksi.preprocess(data)

    with open("assets/r33_update.pkl", 'rb') as sensasi:
        model = pickle.load(sensasi)

        print("-" * 50)
        print("Data dari api server:")
        main(data_prediksi, model)

        # Test Multiple Prediction File
        data_paths = glob.glob("assets/prediction*.json")
        for data_path in data_paths:
            print("-"*50)
            print("Data dari:", data_path)
            with open(data_path) as d:
                data = json.load(d)
                data_prediksi = preprocessing_dataprediksi.preprocess(data)
                output, _ = main(data_prediksi, model)
                print("\nOutput Function:")
                for k in output.keys():
                    print("%11s : %s" % (k, output[k]))
