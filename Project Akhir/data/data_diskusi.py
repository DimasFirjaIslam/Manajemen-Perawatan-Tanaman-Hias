from data.data_utility import *
from datetime import datetime

def load_data_diskusi(tanaman = []):
    data = load_data("data_diskusi.json")
    data_terfilter = []
    for diskusi in data:
        if diskusi["tanaman"] in tanaman if tanaman else True:
            data_terfilter.append(diskusi)
    return data_terfilter

def simpan_data_diskusi(databaru):
    return simpan_data(databaru, "data_diskusi.json")

def tambah_diskusi(judul, tanaman, penulis, konten):
    result = {
        "status": False,
        "message": ""
    }

    data_diskusi = load_data_diskusi()
    data_diskusi.append({
        "judul": judul,
        "tanaman": tanaman,
        "penulis": penulis,
        "konten": konten,
        "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "jawaban": []
    })
    
    result["status"] = simpan_data_diskusi(data_diskusi)
    result["message"] = "Diskusi berhasil ditambahkan...!"
    return result

def tambah_jawaban(indeks_diskusi: int, penulis, konten):
    result = {
        "status": False,
        "message": ""
    }

    data_diskusi = load_data_diskusi()
    data_diskusi[indeks_diskusi].get("jawaban").append({
        "penulis": penulis,
        "konten": konten,
        "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    })
    
    result["status"] = simpan_data_diskusi(data_diskusi)
    result["message"] = "Jawaban berhasil ditambahkan...!"
    return result

def edit_diskusi():
    try:
        result = {
            "status": False,
            "message": ""
        }
        data = load_data_diskusi()
        
        result["status"] = simpan_data_diskusi(data)
        result["message"] = "Data berhasil diubah...!"
    except Exception as e:
        result["message"] = str(e)
    finally:
        return result
    
def edit_jawaban():
    try:
        result = {
            "status": False,
            "message": ""
        }
        data = load_data_diskusi()
        
        result["status"] = simpan_data_diskusi(data)
        result["message"] = "Data berhasil diubah...!"
    except Exception as e:
        result["message"] = str(e)
    finally:
        return result

def hapus_diskusi(indeks_diskusi: int):
    try:
        result = {
            "status": False,
            "message": ""
        }
        data = load_data_diskusi()

        if str(indeks_diskusi).strip() == "":
            raise ValueError("Indeks tidak boleh kosong...!")
        elif not str(indeks_diskusi).isdigit():
            raise ValueError("Indeks harus berupa angka...!")
        elif indeks_diskusi < 0 or indeks_diskusi >= len(data):
            raise IndexError("Diskusi tidak ditemukan...")

        data.pop(indeks_diskusi)
        result["status"] = simpan_data_diskusi(data)
        result["message"] = "Diskusi berhasil dihapus...!"
    except IndexError or ValueError as e:
        result["message"] = str(e)
    finally:
        return result

def hapus_jawaban(indeks_diskusi: int, indeks_jawaban: int):
    try:
        result = {
            "status": False,
            "message": ""
        }
        data_diskusi = load_data_diskusi()

        if str(indeks_diskusi).strip() == "":
            raise ValueError("Indeks diskusi tidak boleh kosong...!")
        elif not str(indeks_diskusi).isdigit():
            raise ValueError("Indeks diskusi harus berupa angka...!")
        elif str(indeks_jawaban).strip() == "":
            raise ValueError("Indeks jawaban tidak boleh kosong...!")
        
        data_diskusi[indeks_diskusi]["jawaban"].pop(indeks_jawaban)
        result["status"] = simpan_data_diskusi(data_diskusi)
        result["message"] = "Jawaban berhasil dihapus...!"
    except IndexError or ValueError as e:
        result["message"] = str(e)
    finally:
        return result

def cek_indeks_diskusi(judul, tanaman):
    data = load_data_diskusi()
    for i, diskusi in enumerate(data):
        if diskusi["judul"] == judul and diskusi["tanaman"] == tanaman:
            return i
    return False

def cek_tanaman(tanaman):
    data = load_data_diskusi()
    for user in data:
        if user["tanaman"] == tanaman:
            return user["tanaman"]
    return False
