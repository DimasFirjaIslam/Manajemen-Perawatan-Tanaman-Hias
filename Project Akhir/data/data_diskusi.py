from data.data_utility import *
from datetime import datetime

# Fungsi untuk mengambil data diskusi dari file JSON dengan nama file "data_diskusi.json"
def load_data_diskusi(tanaman = []):
    data = load_data("data_diskusi.json")
    data_terfilter = []
    for diskusi in data:
        if diskusi["tanaman"] in tanaman if tanaman else True:
            data_terfilter.append(diskusi)
    return data_terfilter

# Fungsi untuk menyimpan data diskusi ke dalam file JSON dengan nama file "data_diskusi.json"
def simpan_data_diskusi(databaru):
    return simpan_data(databaru, "data_diskusi.json")

# Fungsi untuk menambahkan diskusi baru
def tambah_diskusi(judul, tanaman, penulis, konten):
    result = {
        "status": False,
        "message": ""
    }
    # Menduplikasi data diskusi dari database
    data_diskusi = load_data_diskusi()

    # Menambahkan diskusi baru pada duplikasi
    data_diskusi.append({
        "judul": judul,
        "tanaman": tanaman,
        "penulis": penulis,
        "konten": konten,
        "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "jawaban": []
    })
    
    # Menyimpan data diskusi baru ke dalam file JSON
    result["status"] = simpan_data_diskusi(data_diskusi)
    result["message"] = "Diskusi berhasil ditambahkan...!"
    return result

# Fungsi untuk menambahkan jawaban pada diskusi yang dipilih
def tambah_jawaban(indeks_diskusi: int, penulis, konten):
    result = {
        "status": False,
        "message": ""
    }
    # Menduplikasi data diskusi dari database
    data_diskusi = load_data_diskusi()

    # Menambahkan jawaban pada diskusi yang dipilih
    data_diskusi[indeks_diskusi].get("jawaban").append({
        "penulis": penulis,
        "konten": konten,
        "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    })

    # Menimpan data jawaban dalam database dengan duplikais terbaru 
    result["status"] = simpan_data_diskusi(data_diskusi)
    result["message"] = "Jawaban berhasil ditambahkan...!"
    return result

# Fungsi untuk menghapus diskusi dengan indeks yang dipilih
def hapus_diskusi(indeks_diskusi: int):
    try:
        result = {
            "status": False,
            "message": ""
        }
        # Menduplikasi data diskusi dari database
        data = load_data_diskusi()

        # Beberapa syarat yang harus dipenuhi untuk menghapus data diskusi
        if str(indeks_diskusi).strip() == "":
            raise ValueError("Indeks tidak boleh kosong...!")
        elif not str(indeks_diskusi).isdigit():
            raise ValueError("Indeks harus berupa angka...!")
        elif indeks_diskusi < 0 or indeks_diskusi >= len(data):
            raise IndexError("Diskusi tidak ditemukan...")

        # Menghapus duplikasi data diskusi berdasarkan indeks yang dipilih
        data.pop(indeks_diskusi)

        # Menimpa data diskusi yang lama dengan duplikasi yang telah dihapus
        result["status"] = simpan_data_diskusi(data)
        result["message"] = "Diskusi berhasil dihapus...!"
    except IndexError or ValueError as e:
        result["message"] = str(e)
    finally:
        return result

# Fungsi untuk menghapus jawaban pada diskusi yang dipilih
def hapus_jawaban(indeks_diskusi: int, indeks_jawaban: int):
    try:
        result = {
            "status": False,
            "message": ""
        }
        # Menduplikasi data diskusi dari database
        data_diskusi = load_data_diskusi()

        # Beberapa syarat yang harus dipenuhi untuk menghapus jawaban
        if str(indeks_diskusi).strip() == "":
            raise ValueError("Indeks diskusi tidak boleh kosong...!")
        elif not str(indeks_diskusi).isdigit():
            raise ValueError("Indeks diskusi harus berupa angka...!")
        elif str(indeks_jawaban).strip() == "":
            raise ValueError("Indeks jawaban tidak boleh kosong...!")
        
        # Menghapus jawaban pada diskusi dengan indeks terkait pada duplikasi
        data_diskusi[indeks_diskusi]["jawaban"].pop(indeks_jawaban)

        # Menimpan data jawaban dalam database dengan duplikais terbaru
        result["status"] = simpan_data_diskusi(data_diskusi)
        result["message"] = "Jawaban berhasil dihapus...!"
    except IndexError or ValueError as e:
        result["message"] = str(e)
    finally:
        return result

# Fungsi untuk mengecek indeks diskusi dalam database berdasarkan judul dan tanaman
def cek_indeks_diskusi(judul, tanaman):
    data = load_data_diskusi()
    for i, diskusi in enumerate(data):
        if diskusi["judul"] == judul and diskusi["tanaman"] == tanaman:
            return i
    return False