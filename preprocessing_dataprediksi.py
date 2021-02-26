import json
from dateutil import parser
import config

def preprocess(data, indoor_field_type=0):
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
    count_data_excluded = 0
    
    #Preprocess sensor
    if status_indoor:
         # Atur data indoor
        # field1 = rhsht, ga dipake(?)
        variabel_indoor = [
            ['field2', 'field3', 'field4', 'field5', 'field6', 'field7'],
            ['field1', 'field2', 'field3', 'field4', 'field5', 'field6']
        ][indoor_field_type]
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

            try:
                # Atur data karakteristik, dibikin angka aja karena trainingnya udah dalam bentuk angka juga kan
                # Encoding data - One Hot Encoding
    
                data_ac = data_personal_satu['ac']
                
                #Pengkodean AC
                AC = config.AC[data_ac]
               
                
                data_kelamin = data_personal_satu['kelamin']
                
                KELAMIN = config.KELAMIN[data_kelamin]
    
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
    
                
                LAKI_LAKI = config.CLO['laki-laki']
                PEREMPUAN_TANPAJILBAB= config.CLO['perempuan_tanpajilbab']
                PEREMPUAN_BERJILBAB = config.CLO['perempuan_berjilbab']
    
                KONSTANTA_TERMAL = 0
    
                if KELAMIN == 1:  # Jika laki"
                    KONSTANTA_TERMAL = LAKI_LAKI[no_hari]
    
                elif KELAMIN == 2:  # Jika perempuan
                    jilbab = data_personal_satu['jilbab']
                    if jilbab == 'ya':
                        KONSTANTA_TERMAL = PEREMPUAN_TANPAJILBAB[no_hari]
                    elif jilbab == 'tidak':
                        KONSTANTA_TERMAL = PEREMPUAN_BERJILBAB[no_hari]
    
                # Kumpulin data
                # Data personal
                # 'usia','kelamin','tinggi','berat','jilbab'
                usia = data_personal_satu['usia']
                tinggi = data_personal_satu['tinggi']
                berat = data_personal_satu['berat']
    
                data_personal_element=[usia, KELAMIN, tinggi, berat, KONSTANTA_TERMAL]
                #print(data_personal_satu)
                
                # Latar belakangac,durasi_ac,durasi_kipas,asal,lama_dijogja
                durasi_ac = data_personal_satu['durasi_ac']
                durasi_kipas = data_personal_satu['durasi_kipas']
                lama_dijogja = data_personal_satu['lama_dijogja']
    
                data_latar_belakang_element=[AC, durasi_ac,durasi_kipas, daerah, lama_dijogja]
                
                data_personal_akhir.append(data_personal_element)
                data_latar_belakang.append(data_latar_belakang_element)
        
            #Untuk data none, hilangkan data (exclude data)
            except KeyError:
                count_data_excluded += 1
                pass
                
            
    elif not status_personal:
        pass

    return {
        "data_personal": data_personal_akhir,
        "data_latar_belakang": data_latar_belakang,
        "sensor_indoor": sensor_indoor,
        "sensor_outdoor": sensor_outdoor,
        "excluded_data":count_data_excluded
    }

