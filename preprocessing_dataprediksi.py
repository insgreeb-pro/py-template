import json
from dateutil import parser

def preprocess(data):
    data_asal = json.loads("".join(open('assets/daerah.json').readlines()))


    # Ngambil data yang mau diprediksi
    data_personal = data['data_dasar']
    data_sensor_indoor = data['data_sensor']['indoor']
    data_sensor_outdoor = data['data_sensor']['outdoor']


    # Cek semua kondisi data input ke model
    status_personal = 1 if len(data_personal) != 0 else 0
    status_indoor = 1 if len(data_sensor_indoor) != 0 else 0
    status_outdoor = 1 if len(data_sensor_outdoor) != 0 else 0

    # Nampung semua data akhir
    data_personal_akhir=[]
    data_latar_belakang=[]
    sensor_indoor=[]
    sensor_outdoor=[]
    
    if status_personal == 1 and status_indoor == 1 and status_outdoor == 1:
       
        # Atur data indoor
        # field1 = rhsht, ga dipake(?)
        variabel_indoor = ['field2', 'field3',
                           'field4', 'field5', 'field6', 'field7']
        sensor_indoor = []
        for variabel in variabel_indoor:
            data_indoor = float(data_sensor_indoor[variabel])
            sensor_indoor.append(data_indoor)
        #print(sensor_indoor)
        in_rh, in_co2, in_ta, in_tg, in_ws, in_li = sensor_indoor

        # Atur data outdoor
        variabel_outdoor = ['field1', 'field2', 'field3', 'field4', 'field5']
        sensor_outdoor = []
        for variabel in variabel_outdoor:
            data_outdoor = float(data_sensor_indoor[variabel])
            sensor_outdoor.append(data_outdoor)

        # windspeed, winddirection, solarpower, humidity, temperature
        out_ws, out_wd, out_sp, out_rh, out_ta = sensor_outdoor

        datetime = data_sensor_indoor['created_at']  # clo berdasar hari
        no_hari = int(parser.parse(datetime).strftime("%w"))
        #print(data_personal)
        for data_personal_satu in data_personal:
            
            # Atur data karakteristik, dibikin angka aja karena trainingnya udah dalam bentuk angka juga kan
            # Encoding data - One Hot Encoding
            # Encode untuk ac dan kipas
            # 3 untuk tidak ac dan tidak kipas
            # 2 - untuk kipas saja
            # 1 - untuk ac dan kipas
            # 0 - untuk ac saja
            ac = data_personal_satu['ac']
            if ac == 'tidak':
                ac = 3

            elif ac == 'kipas':
                ac = 2

            elif ac == 'ac dan kipas':
                ac = 1

            elif ac == 'ac':
                ac = 0
          
            # Encode untuk jenis kelamin
            # 0 - untuk laki-laki
            # 1 - untuk perempuan
            kelamin = 0 if data_personal_satu['kelamin'] == 'L' else 1

            # Encode untuk daerah asal, udah ada data dari daerah.json, antara sejuk atau hangat
            # 0 - untuk sejuk
            # 1 - untuk hangat
            asal = data_personal_satu['asal']
            daerah = 0 if asal == data_asal["sejuk"] else 1

            # Untuk jilbab, bakal jadi konstanta termal pakaian (bergantung kelamin, jilbab, hari)

            # Konstanta insulasi termal berdasarkan ASHRAE, liat di data.xlsx
            laki = [0, 0.6, 0.6, 0.54, 0.54, 0.65, 0.65]
            perempuan_tanpajilbab = [0, 0.59, 0.59, 0.53, 0.53, 0.64, 0.64]
            perempuan_berjilbab = [0, 0.73, 0.73, 0.64, 0.64, 0.82, 0.82]

            konstanta_termal = 0

            if kelamin == 0:  # Jika laki"
                konstanta_termal = laki[no_hari]

            elif kelamin == 1:  # Jika perempuan
                jilbab = data_personal_satu['jilbab']
                if jilbab == 'ya':
                    konstanta_termal = perempuan_berjilbab[no_hari]
                elif jilbab == 'tidak':
                    konstanta_termal = perempuan_tanpajilbab[no_hari]

            # Kumpulin data
            # Data personal
            # 'usia','kelamin','tinggi','berat','jilbab'
            usia = data_personal_satu['usia']
            tinggi = data_personal_satu['tinggi']
            berat = data_personal_satu['berat']

            data_personal_element=[usia, kelamin, tinggi, berat, konstanta_termal]
            #print(data_personal_satu)
            
            # Latar belakangac,durasi_ac,durasi_kipas,asal,lama_dijogja
            durasi_ac = data_personal_satu['durasi_ac']
            durasi_kipas = data_personal_satu['durasi_kipas']
            lama_dijogja = data_personal_satu['lama_dijogja']

            data_latar_belakang_element=[ac, durasi_ac,durasi_kipas, daerah, lama_dijogja]
            
            data_personal_akhir.append(data_personal_element)
            data_latar_belakang.append(data_latar_belakang_element)
            
    elif not all([status_personal,status_indoor,status_outdoor]):
        pass

    return {
        "data_personal": data_personal_akhir,
        "data_latar_belakang": data_latar_belakang,
        "sensor_indoor": sensor_indoor,
        "sensor_outdoor": sensor_outdoor
    }

