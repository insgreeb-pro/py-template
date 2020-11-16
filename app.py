#import pandas as pd
import pickle
#from sklearn.model_selection import train_test_split
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.metrics import accuracy_score
#from sklearn import metrics

import json
#from sklearn.preprocessing import LabelEncoder
from dateutil import parser
import os.path

from helper import downloader

#Load model ke server lokal
'''
with open('r33_model_sensasi.pkl', 'rb') as sensasi:
    model_RF_sensasi = pickle.load(sensasi)
    
with open('r33_model_kenyamanan.pkl', 'rb') as kenyamanan:
    model_RF_kenyamanan = pickle.load(kenyamanan)
    

with open('r33_model_penerimaan.pkl', 'rb') as penerimaan:
    model_RF_penerimaan = pickle.load(penerimaan)
'''

ID_RUANG: int = 2

# memasukkan dataset
# data = json.loads("".join(open('prediction.json').readlines()))
data = json.loads(
    downloader.dataset(ID_RUANG)
)

data_asal = json.loads("".join(open('daerah.json').readlines()))

  
#Atur data untuk prediksi sensasi duluu
#fitur_sensasi = ['usia','kelamin','tinggi','berat','jilbab','ac','durasi_ac',
 #           'durasi_kipas','asal','lama_dijogja','indoor','outdoor']

#'in_rh','in_co2','in_ta','in_tg','in_ws','in_li','out_data1','out_data2','out_data3','out_data4','out_data5','out_data6'


#Ngambil data yang mau diprediksi
data_personal = data['data_dasar']
data_sensor_indoor = data['data_sensor']['indoor']
data_sensor_outdoor = data['data_sensor']['outdoor']

no_ruang =data['ruang'].lower()

#Buka model sesuai no ruangnya
status_model=os.path.exists(no_ruang+'.pkl')

    
#Cek semua kondisi data input ke model
status_personal = 1 if len(data_personal)!=0 else 0
status_indoor = 1 if len(data_sensor_indoor) else 0
status_outdoor = 1 if len(data_sensor_outdoor) else 0

#Nampung semua data akhir
prediksi_sensasi=[]
prediksi_kenyamanan=[]
prediksi_penerimaan=[]


if status_personal and status_indoor and status_outdoor ==1 and status_model==True:
    #Siapin model
    with open(no_ruang+'.pkl', 'rb') as sensasi:
        model = pickle.load(sensasi)
        model_sensasi=model[0]
        model_kenyamanan=model[1]
        model_penerimaan=model[2]
    #Atur data indoor
    #field1 = rhsht, ga dipake(?)
    variabel_indoor = ['field2','field3','field4','field5','field6','field7']
    sensor_indoor=[]
    for variabel in variabel_indoor:
        data_indoor=data_sensor_indoor[variabel]
        sensor_indoor.append(data_indoor)
        
    in_rh,in_co2,in_ta,in_tg,in_ws,in_li=sensor_indoor
    
    
    #Atur data outdoor
    variabel_outdoor = ['field1','field2','field3','field4','field5']  
    sensor_outdoor=[]
    for variabel in variabel_outdoor:
        data_outdoor=data_sensor_indoor[variabel]
        sensor_outdoor.append(data_outdoor)
        
    #windspeed, winddirection, solarpower, humidity, temperature
    out_ws,out_wd,out_sp,out_rh,out_ta=sensor_outdoor
    
    datetime = data_sensor_indoor['created_at'] # clo berdasar hari
    no_hari = int(parser.parse(datetime).strftime("%w"))
    
    for data_personal_satu in data_personal:
        #Atur data karakteristik, dibikin angka aja karena trainingnya udah dalam bentuk angka juga kan
        # Encoding data - One Hot Encoding
        #Encode untuk ac dan kipas
        #3 untuk tidak ac dan tidak kipas
        #2 - untuk kipas saja
        #1 - untuk ac dan kipas
        #0 - untuk ac saja
        ac = data_personal_satu['ac']
        if ac =='tidak':
            ac = 3
        
        elif ac =='kipas':
            ac = 2
            
        elif ac == 'ac dan kipas':
            ac = 1
        
        elif ac == 'ac':
            ac = 0
            
        #Encode untuk jenis kelamin
        #0 - untuk laki-laki
        #1 - untuk perempuan
        kelamin = 0 if data_personal_satu['kelamin'] == 'L' else 1
    
        
        #Encode untuk daerah asal, udah ada data dari daerah.json, antara sejuk atau hangat
        #0 - untuk sejuk
        #1 - untuk hangat
        asal = data_personal_satu['asal']
        daerah = 0 if asal == data_asal["sejuk"] else 1
    
        #Untuk jilbab, bakal jadi konstanta termal pakaian (bergantung kelamin, jilbab, hari)
    
        #Konstanta insulasi termal berdasarkan ASHRAE, liat di data.xlsx
        laki = [0,0.6,0.6,0.54,0.54,0.65,0.65]
        perempuan_tanpajilbab = [0,0.59,0.59,0.53,0.53,0.64,0.64]
        perempuan_berjilbab = [0,0.73,0.73,0.64,0.64,0.82,0.82]
        
        if kelamin ==0 :#Jika laki"
            konstanta_termal = laki[no_hari]
        
        elif kelamin ==1: #Jika perempuan
            jilbab = data_personal_satu['jilbab']
            if jilbab =='ya':
                konstanta_termal=perempuan_berjilbab[no_hari]
            elif jilbab =='tidak':
                konstanta_termal=perempuan_tanpajilbab[no_hari]
    
    
        #Kumpulin data
        #Data personal
        #'usia','kelamin','tinggi','berat','jilbab'
        usia = data_personal_satu['usia']
        tinggi = data_personal_satu['tinggi']
        berat = data_personal_satu['berat']
        
        data_personal=[usia,kelamin,tinggi,berat,konstanta_termal]
        
        #Latar belakangac,durasi_ac,durasi_kipas,asal,lama_dijogja
        durasi_ac=data_personal_satu['durasi_ac']
        durasi_kipas = data_personal_satu['durasi_kipas']
        lama_dijogja=data_personal_satu['lama_dijogja']
        
        data_latar_belakang = [ac,durasi_ac,durasi_kipas,daerah,lama_dijogja]
        
        
        
        
        
        
    
        #Prediksi per orang yang ada di ruangann
    
        #Prediksi sensasi termal
        data_prediksi_sensasi = data_personal+data_latar_belakang+sensor_indoor+sensor_outdoor
        
        output_sensasi = int(model_sensasi.predict([data_prediksi_sensasi]))
    
        #Prediksi kenyamanan termal
        data_prediksi_kenyamanan = data_personal+[output_sensasi]
        
        output_kenyamanan = int(model_kenyamanan.predict([data_prediksi_kenyamanan]))
        
        #Prediksi penerimaan termal
        data_prediksi_penerimaan = data_personal+[output_sensasi]+[output_kenyamanan]
        
        output_penerimaan = int(model_penerimaan.predict([data_prediksi_penerimaan]))
        
        
        #Masukin buat output akhir
        prediksi_sensasi.append(output_sensasi)
        prediksi_kenyamanan.append(output_kenyamanan)
        prediksi_penerimaan.append(output_penerimaan)
        
        
    print('Prediksi sensasi = ',prediksi_sensasi)
    print('Prediksi kenyamanan = ',prediksi_kenyamanan)
    print('Prediksi penerimaan = ',prediksi_penerimaan)
   
elif status_personal or status_indoor or status_outdoor !=1 and status_model==True:
    print('Data kosong')
    
elif status_personal and status_indoor and status_outdoor ==1 and status_model==False:
    print('Model tidak ditemukan')

