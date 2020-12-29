# Encode untuk ac dan kipas
# 0 untuk tidak ac dan tidak kipas
# 1 - untuk kipas saja
# 2 - untuk ac dan kipas
# 3 - untuk ac saja

AC = {
      "tidak":0,
      "kipas":1,
      "ac dan kipas":2,
      "ac":3
      }


# Encode untuk jenis kelamin
# 1 - untuk laki-laki
# 2 - untuk perempuan
KELAMIN = {
        "L":1,
        "P":2
        }

#Untuk daerah sudah dicover sama file kategori kecamatan nantinya, confignya dari file daerah aja.

#Konstanta termal pakaian (bergantung kelamin, jilbab, hari)

# Konstanta insulasi termal berdasarkan ASHRAE, liat di data.xlsx
#Urutannya biru putih 3x - batik - pramuka?
#Ga ada sampe sabtu kah? Sementara sabtu kasih untuk pramuka
CLO ={
"laki-laki":[0, 0.58, 0.58, 0.58, 0.51, 0.67, 0.67],
"perempuan_tanpajilbab": [0, 0.57, 0.57, 0.57, 0.5, 0.66, 0.66],
"perempuan_berjilbab":[0, 0.94, 0.94, 0.94, 0.87, 1.03, 1.03]
}