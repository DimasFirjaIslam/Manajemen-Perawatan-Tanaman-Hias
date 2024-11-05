import os
import json

os.system("cls || clear")


def load_data():
    with open("data.json", "r") as file_json:
        return json.load(file_json)


def simpan_data(databaru):
    with open("data.json", "w") as file_json:
        json.dump(databaru, file_json, indent=4)


def tampilkan_data():
    data = load_data()
    if data:
        for index, item in enumerate(data, start=1):
            print(f"""{index}.
            Nama         : {item['Nama']}
            Jenis        : {item['Jenis']}
            Jadwal Siram : {item['Jadwal_siram']}
            Suhu         : {item['Suhu']}
            Pemupukan    : {item['Pemupukan']}
            Media Tanam  : {item['Media_Tanam']}
            """)

    else:
        print("Tidak ada data yang tersedia.")


def tambah_data():
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

    data = load_data()
    data.append(databaru)
    simpan_data(data)
    print("Data berhasil ditambahkan!")


def edit_data():
    data = load_data()
    tampilkan_data()
    nomor_tanaman = int(input("Masukkan nomor tanaman yang ingin diubah: ")) - 1
    if 0 <= nomor_tanaman < len(data):
        tanaman = data[nomor_tanaman]
        tanaman["Nama"] = input("Masukkan nama tanaman baru: ")
        tanaman["Jenis"] = input("Masukkan jenis tanaman baru: ")
        tanaman["Jadwal_siram"] = input("Masukkan jadwal siram baru: ")
        tanaman["Suhu"] = input("Masukkan suhu baru: ")
        tanaman["Pemupukan"] = input("Masukkan jadwal pemupukan baru: ")
        tanaman["Media_Tanam"] = input("Masukkan media tanam baru: ")
        simpan_data(data)
        print("Data berhasil diubah!")
    else:
        print("Nomor tanaman tidak valid.")


def hapus_data():
    tampilkan_data()
    nomor_tanaman = int(input("Masukkan nomor tanaman yang ingin dihapus: ")) - 1
    data = load_data()
    if nomor_tanaman < len(data):
        data.pop(nomor_tanaman)
        simpan_data(data)
        print("Data berhasil dihapus!")
    else:
        print("Data tanaman tidak ditemukan.")


def menu():
    while True:
        print("Menu")
        print("1. Lihat Data")
        print("2. Tambah Data")
        print("3. Edit Data")
        print("4. Hapus Data")
        print("5. Keluar")

        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            tampilkan_data()
        elif pilihan == "2":
            tambah_data()
        elif pilihan == "3":
            edit_data()
        elif pilihan == "4":
            hapus_data()
        elif pilihan == "5":
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")


menu()

