from data.data_utility import *
import data.data_diskusi as data_diskusi

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

def load_data_tanaman(jenis_tanaman = [], min_suhu = "", max_suhu = "", media = []):
    data = load_data("data_tanaman.json")
    data_terfilter = []
    for tanaman in data:
        if tanaman["jenis"] in jenis_tanaman if jenis_tanaman else True:
            data_terfilter.append(tanaman)
            if tanaman["min_suhu"] < int(min_suhu) if min_suhu else False:
                data_terfilter.remove(tanaman)
            elif tanaman["max_suhu"] > int(max_suhu) if max_suhu else False:
                data_terfilter.remove(tanaman)
            elif tanaman["media_tanam"] not in media if media else False:
                data_terfilter.remove(tanaman)
    return data_terfilter


def simpan_data_tanaman(databaru):
    return simpan_data(databaru, "data_tanaman.json")

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
def edit_tanaman(indeks_tanaman: int, nama_baru, jenis_baru, jadwal_siram_baru, min_suhu_baru, max_suhu_baru, pemupukan_baru, media_tanam_baru):
    try:
        result = {
            "status": False,
            "message": ""
        }
        data = load_data_tanaman()
        tanaman = data[indeks_tanaman]

        if str(indeks_tanaman).strip() == "":
            raise ValueError("Nomor tanaman tidak boleh kosong...!")
        elif not str(indeks_tanaman).isdigit():
            raise ValueError("Nomor tanaman harus berupa angka...!")
        elif indeks_tanaman < 0 or indeks_tanaman >= len(data):
            raise IndexError("Tanaman tidak ditemukan...")
        
        # Memperbarui data diskusi yang menyangkut dengan tanaman yang diedit
        list_diskusi = data_diskusi.load_data_diskusi()
        for diskusi in list_diskusi:
            if diskusi["tanaman"] == tanaman["nama"]:
                diskusi["tanaman"] = nama_baru
        data_diskusi.simpan_data_diskusi(list_diskusi)
        
        tanaman["nama"] = nama_baru
        tanaman["jenis"] = jenis_baru
        tanaman["jadwal_siram"] = jadwal_siram_baru
        tanaman["min_suhu"] = min_suhu_baru
        tanaman["max_suhu"] = max_suhu_baru
        tanaman["pemupukan"] = pemupukan_baru
        tanaman["media_tanam"] = media_tanam_baru
        
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