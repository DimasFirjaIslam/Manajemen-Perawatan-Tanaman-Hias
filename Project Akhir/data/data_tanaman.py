from data.data_utility import *

def load_data_tanaman():
    return load_data("data_tanaman.json")

def simpan_data_tanaman(databaru):
    simpan_data(databaru, "data_tanaman.json")

def tambah_tanaman():
    nama = input("Masukkan nama tanaman: ")
    jenis = input("Masukkan jenis tanaman: ")
    jadwal_siram = input("Masukkan jadwal siram: ")
    suhu = input("Masukkan suhu yang cocok: ")
    pemupukan = input("Masukkan jadwal pemupukan: ")
    media_tanam = input("Masukkan media tanam: ")

    databaru = {
        "Nama": nama,
        "Jenis": jenis,
        "Jadwal_siram": jadwal_siram,
        "Suhu": suhu,
        "Pemupukan": pemupukan,
        "Media_Tanam": media_tanam
    }

    data = load_data_tanaman()
    data.append(databaru)
    simpan_data_tanaman(data)
    print("Data berhasil ditambahkan!")

def edit_tanaman():
    data = load_data_tanaman()
    nomor_tanaman = int(input("Masukkan nomor tanaman yang ingin diubah: ")) - 1
    if 0 <= nomor_tanaman < len(data):
        tanaman = data[nomor_tanaman]
        tanaman["Nama"] = input("Masukkan nama tanaman baru: ")
        tanaman["Jenis"] = input("Masukkan jenis tanaman baru: ")
        tanaman["Jadwal_siram"] = input("Masukkan jadwal siram baru: ")
        tanaman["Suhu"] = input("Masukkan suhu baru: ")
        tanaman["Pemupukan"] = input("Masukkan jadwal pemupukan baru: ")
        tanaman["Media_Tanam"] = input("Masukkan media tanam baru: ")
        simpan_data_tanaman(data)
        print("Data berhasil diubah!")
    else:
        print("Nomor tanaman tidak valid.")

def hapus_tanaman():
    nomor_tanaman = int(input("Masukkan nomor tanaman yang ingin dihapus: ")) - 1
    data = load_data_tanaman()
    if 0 <= nomor_tanaman < len(data):
        data.pop(nomor_tanaman)
        simpan_data_tanaman(data)
        print("Data berhasil dihapus!")
    else:
        print("Data tanaman tidak ditemukan.")