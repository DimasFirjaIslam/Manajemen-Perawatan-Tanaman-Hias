from data.data_utility import *

jenis = (
    "Bonsai Bunga",
    "Tropis",
    "Tropis Merambat",
    "Tropis Berdaun Besar",
    "Sukulen",
    "Tanaman Paku",
    "Hias Berdaun Warna",
    "Tanaman Semak",
    "Tanaman Hias Berbunga"
)

satuan_waktu = (
    "Hari",
    "Minggu",
    "Bulan",
    "Tahun",
)

media_tanam = (
    "Tanah",
    "Tanah Berpasir",
    "Tanah Lembab",
    "Tanah Humus",
    "Tanah Subur",
    "Tanah Subur dan Berpasir",
    "Tambus Gambut",
)

def load_data_tanaman(jenis_tanaman = [], jadwal_siram = [], min_suhu = 0, max_suhu = 0, pemupukan = [], media = []):
    data = load_data("data_tanaman.json")
    data_terfilter = []
    for tanaman in data:
        if tanaman["jenis"] in jenis_tanaman if jenis_tanaman else True:
            data_terfilter.append(tanaman)
            if tanaman["min_suhu"] < min_suhu if min_suhu else False:
                data_terfilter.remove(tanaman)
                continue
            elif tanaman["max_suhu"] > max_suhu if max_suhu else False:
                data_terfilter.remove(tanaman)
                continue
    return data_terfilter


def simpan_data_tanaman(databaru):
    simpan_data(databaru, "data_tanaman.json")

# Fungsi untuk menambahkan data tanaman baru
def tambah_tanaman(nama, jenis, jadwal_siram, min_suhu, max_suhu, pemupukan, media_tanam):
    try:
        result = {
            "status": False,
            "message": ""
        }

        if any(tanaman["nama"] == nama for tanaman in load_data_tanaman()):
            raise ValueError("Tanaman sudah ada...!")

        databaru = {
            "nama": nama,
            "jenis": jenis,
            "jadwal_siram": jadwal_siram,
            "min_suhu": min_suhu,
            "max_suhu": max_suhu,
            "pemupukan": pemupukan,
            "media_tanam": media_tanam
        }

        data = load_data_tanaman()
        data.append(databaru)
        result["status"] = simpan_data_tanaman(data)
        result["message"] = "Tanaman berhasil ditambahkan...!"
        return result
    except Exception as e:
        result["message"] = str(e)
    finally:
        return result

# Fungsi untuk menampilkan data tanaman
def edit_tanaman(indeks_tanaman: int, nama, jenis, jadwal_siram, min_suhu, max_suhu, pemupukan, media_tanam):
    try:
        result = {
            "status": False,
            "message": ""
        }
        data = load_data_tanaman()

        if str(indeks_tanaman).strip() == "":
            raise ValueError("Nomor tanaman tidak boleh kosong...!")
        elif not str(indeks_tanaman).isdigit():
            raise ValueError("Nomor tanaman harus berupa angka...!")
        elif indeks_tanaman < 0 or indeks_tanaman >= len(data):
            raise IndexError("Tanaman tidak ditemukan...")
        
        tanaman = data[indeks_tanaman]
        tanaman["nama"] = nama
        tanaman["jenis"] = jenis
        tanaman["jadwal_siram"] = jadwal_siram
        tanaman["min_suhu"] = min_suhu
        tanaman["max_suhu"] = max_suhu
        tanaman["pemupukan"] = pemupukan
        tanaman["media_tanam"] = media_tanam
        
        result["status"] = simpan_data_tanaman(data)
        result["message"] = "Data berhasil diubah...!"
    except IndexError or ValueError as e:
        result["message"] = str(e)
    finally:
        return result

def hapus_tanaman(indeks_tanaman: int):
    try:
        result = {
            "status": False,
            "message": ""
        }
        data = load_data_tanaman()

        if str(indeks_tanaman).strip() == "":
            raise ValueError("Nomor tanaman tidak boleh kosong...!")
        elif not str(indeks_tanaman).isdigit():
            raise ValueError("Nomor tanaman harus berupa angka...!")
        elif indeks_tanaman < 0 or indeks_tanaman >= len(data):
            raise IndexError("Tanaman tidak ditemukan...")
        
        data.pop(indeks_tanaman)
        result["status"] = simpan_data_tanaman(data)
        result["message"] = "Tanaman berhasil dihapus...!"
    except IndexError or ValueError as e:
        result["message"] = str(e)
    finally:
        return result
        

def cek_index(nama_tanaman):
    data = load_data_tanaman()
    for i, item in enumerate(data):
        if item["nama"] == nama_tanaman:
            return i
        
# A > Jenis Tanaman ("Sukulen", "Kaktus", "Bunga", "Sayuran", "Buah")
# B > Minimal Suhu (10 C)
# C > Maksimal Suhu (40 C)

# D > Hapus Filter
# E > Kembali