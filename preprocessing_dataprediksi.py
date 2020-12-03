import json
from dateutil import parser

def preprocess(data):
    data_asal = json.loads("".join(open('assets/daerah.json').readlines()))


    # Ngambil data yang mau diprediksi
    data_personal = data['data_dasar']
    data_sensor_indoor = data['data_sensor']['indoor']
    data_sensor_outdoor = data['data_sensor']['outdoor']


    # Cek semua kondisi data input ke pre-processing
    status_personal = True if len(data_personal) != 0 else False
    status_indoor = True if len(data_sensor_indoor) != 0 else False
    status_outdoor = True if len(data_sensor_outdoor) != 0 else False
    #print(status_personal,status_indoor,status_outdoor)
    # Nampung semua data akhir
    data_personal_akhir=[]
    data_latar_belakang=[]
    sensor_indoor=[]
    sensor_outdoor=[]
    
    #Preprocess sensor
    if status_indoor:
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
    
    elif not status_indoor:
        pass
    
    if status_outdoor:
        # Atur data outdoor
        variabel_outdoor = ['field1', 'field2', 'field3', 'field4', 'field5']
        sensor_outdoor = []
        for variabel in variabel_outdoor:
            data_outdoor = float(data_sensor_outdoor[variabel])
            sensor_outdoor.append(data_outdoor)

        # windspeed, winddirection, solarpower, humidity, temperature
        out_ws, out_wd, out_sp, out_rh, out_ta = sensor_outdoor
    
    elif not status_outdoor:
        pass
        
    if status_personal:
        datetime = data['datetime']  # clo berdasar hari
        no_hari = int(parser.parse(datetime).strftime("%w"))
        #print(data_personal)
        for data_personal_satu in data_personal:
            
            # Atur data karakteristik, dibikin angka aja karena trainingnya udah dalam bentuk angka juga kan
            # Encoding data - One Hot Encoding
            # Encode untuk ac dan kipas
            # 0 untuk tidak ac dan tidak kipas
            # 1 - untuk kipas saja
            # 2 - untuk ac dan kipas
            # 3 - untuk ac saja
            ac = data_personal_satu['ac']
            if ac == 'tidak':
                ac = 0

            elif ac == 'kipas':
                ac = 1

            elif ac == 'ac dan kipas':
                ac = 2

            elif ac == 'ac':
                ac = 3
          
            # Encode untuk jenis kelamin
            # 1 - untuk laki-laki
            # 2 - untuk perempuan
            kelamin = 1 if data_personal_satu['kelamin'] == 'L' else 2

            # Encode untuk daerah asal, udah ada data dari daerah.json, antara sejuk atau hangat
            # 0 - untuk sejuk
            # 1 - untuk hangat
            #ini masih belom pake data kecamatan terbaru, soalnya inputnya belomm format kecamatan.
            asal = data_personal_satu['asal']
            daerah = 0 if asal == data_asal["sejuk"] else 1
            
            '''
            #Encode untuk daerah asal, data input rawnya masih asal daerah, belom alamat tinggal di jogjaa
            #Inputnya udah dikategorikan sama mas wafa dan udah bakal sesuai sama data excel yang skrg kecamatan_dijogja
            asal = [variable["asal"] for variable in data_bersih]
            daerah = [(data_asal[data_asal['nama']==item.upper()]['output']) for item in asal]
            '''

            # Untuk jilbab, bakal jadi konstanta termal pakaian (bergantung kelamin, jilbab, hari)

            # Konstanta insulasi termal berdasarkan ASHRAE, liat di data.xlsx
            #Urutannya biru putih 3x - batik - pramuka?
            #Ga ada sampe sabtu kah? Sementara sabtu kasih untuk pramuka
            laki = [0, 0.58, 0.58, 0.58, 0.51, 0.67, 0.67]
            perempuan_tanpajilbab = [0, 0.57, 0.57, 0.57, 0.5, 0.66, 0.66]
            perempuan_berjilbab = [0, 0.94, 0.94, 0.94, 0.87, 1.03, 1.03]

            konstanta_termal = 0

            if kelamin == 1:  # Jika laki"
                konstanta_termal = laki[no_hari]

            elif kelamin == 2:  # Jika perempuan
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
            
    elif not status_personal:
        pass

    return {
        "data_personal": data_personal_akhir,
        "data_latar_belakang": data_latar_belakang,
        "sensor_indoor": sensor_indoor,
        "sensor_outdoor": sensor_outdoor
    }

