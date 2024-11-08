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
        "nama": nama,
        "jenis": jenis,
        "jadwal_siram": jadwal_siram,
        "suhu": suhu,
        "pemupukan": pemupukan,
        "media_tanam": media_tanam
    }

    data = load_data_tanaman()
    data.append(databaru)
    simpan_data_tanaman(data)
    input("Data berhasil ditambahkan...!")

def edit_tanaman():
    try:
        data = load_data_tanaman()
        print("(Ket: Kosongkan input untuk kembali ke menu.)")
        nomor_tanaman = input("Masukkan nomor tanaman yang ingin diubah: ")
        if not nomor_tanaman: return
        nomor_tanaman = int(nomor_tanaman) - 1
        if 0 <= nomor_tanaman < len(data):
            print("(Ket: Kosongkan input untuk mempertahankan nilai saat ini.)")
            tanaman = data[nomor_tanaman]
            tanaman["nama"] = input(f"Masukkan nama tanaman baru: ") or tanaman["nama"]
            tanaman["jenis"] = input(f"Masukkan jenis tanaman baru: ") or tanaman["jenis"]
            tanaman["jadwal_siram"] = input(f"Masukkan jadwal siram baru: ") or tanaman["jadwal_siram"]
            tanaman["suhu"] = input(f"Masukkan suhu baru: ") or tanaman["suhu"]
            tanaman["pemupukan"] = input(f"Masukkan jadwal pemupukan baru: ") or tanaman["pemupukan"]
            tanaman["media_tanam"] = input(f"Masukkan media tanam baru: ") or tanaman["media_tanam"]
            simpan_data_tanaman(data)
            input("Data berhasil diubah...!")
        else:
            input("Tanaman tidak ditemukan...!")
    except ValueError:
        input("Nomor tanaman tidak valid, silakan coba lagi...")

def hapus_tanaman():
    try:
        data = load_data_tanaman()
        print("(Ket: Kosongkan input untuk kembali ke menu.)")
        nomor_tanaman = input("Masukkan nomor tanaman yang ingin dihapus: ")
        if not nomor_tanaman: return
        nomor_tanaman = int(nomor_tanaman) - 1
        if 0 <= nomor_tanaman < len(data):
            data.pop(nomor_tanaman)
            simpan_data_tanaman(data)
            input("Data berhasil dihapus...!")
        else:
            input("Tanaman tidak ditemukan...!")
    except ValueError:
        input("Nomor tanaman tidak valid, silakan coba lagi...")