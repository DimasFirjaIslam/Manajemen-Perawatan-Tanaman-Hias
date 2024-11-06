import os
from utility import clear_screen
import data.data_user as data_user
import data.data_tanaman as data_tanaman
import main

# Keterangan: Hanya gunakan variabel pilihan untuk pilihan menu
pilihan_menu = ""
main_menu = None

def tampilkan_tanaman():
    data = data_tanaman.load_data()
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

    data = data_tanaman.load_data()
    data.append(databaru)
    data.simpan_data(data)
    print("Data berhasil ditambahkan!")

def edit_tanaman():
    data = data_tanaman.load_data()
    tampilkan_tanaman()
    nomor_tanaman = int(input("Masukkan nomor tanaman yang ingin diubah: ")) - 1
    if 0 <= nomor_tanaman < len(data):
        tanaman = data[nomor_tanaman]
        tanaman["Nama"] = input("Masukkan nama tanaman baru: ")
        tanaman["Jenis"] = input("Masukkan jenis tanaman baru: ")
        tanaman["Jadwal_siram"] = input("Masukkan jadwal siram baru: ")
        tanaman["Suhu"] = input("Masukkan suhu baru: ")
        tanaman["Pemupukan"] = input("Masukkan jadwal pemupukan baru: ")
        tanaman["Media_Tanam"] = input("Masukkan media tanam baru: ")
        data_tanaman.simpan_data(data)
        print("Data berhasil diubah!")
    else:
        print("Nomor tanaman tidak valid.")

def hapus_tanaman():
    tampilkan_tanaman()
    nomor_tanaman = int(input("Masukkan nomor tanaman yang ingin dihapus: ")) - 1
    data = data_tanaman.load_data()
    if nomor_tanaman < len(data):
        data.pop(nomor_tanaman)
        data_tanaman.simpan_data(data)
        print("Data berhasil dihapus!")
    else:
        print("Data tanaman tidak ditemukan.")

def menu_awal():
    clear_screen()
    print("=" * 10 + " Menu Awal " + "=" * 10)
    print("1. Registrasi")
    print("2. Log in")
    print("3. Keluar Program")

    pilihan = input("Masukkan Angka Menu Pilihan: ")

    if pilihan == "1":
        print("=" * 10 + " Registrasi " + "=" * 10)
        user_baru = input("Masukkan Username Baru: ")
        password_baru = input("Masukkan Password Baru: ")
        user_exists = any(user["Username"] == user_baru for user in data_user.load_data())

        if user_exists:
            print("Username Sudah Terdaftar")
        else:
            data_user.register(user_baru, password_baru)
            print("Registrasi Berhasil")

    elif pilihan == "2":
        input_username = input("Username: ")
        input_password = input("Password: ")
        logon_user = data_user.login(input_username, input_password)

        if logon_user:
            if logon_user['role'].lower() == "admin":
                main_menu = MainMenuAdmin()
            else:
                main_menu = MainMenuUser()
        else:
            print("Akun atau password salah")
    elif pilihan == "3":
        print("Program Selesai, Terimakasih Telah Menggunakan Layanan Kami")
    else:
        print("Pilihan Tidak Valid")
        input("Tekan Enter Untuk Kembali")

def MainMenuAdmin():
    clear_screen()

    print("Menu Utama")
    print("1. Lihat Data")
    print("2. Tambah Data")
    print("3. Edit Data")
    print("4. Hapus Data")
    print("5. Keluar")

    pilihan_menu = input("Pilih menu: ")
    if pilihan_menu == "1":
        tampilkan_tanaman()
    elif pilihan_menu == "2":
        tambah_tanaman()
    elif pilihan_menu == "3":
        edit_tanaman()
    elif pilihan_menu == "4":
        hapus_tanaman()
    elif pilihan_menu == "5":
        print("Keluar dari program.")
    else:
        print("Pilihan tidak valid, silakan coba lagi.")
    
def MainMenuUser():
    clear_screen()

    print("Menu Utama")
    print("1. Lihat Data")
    print("2. Keluar")

    pilihan_menu = input("Pilih menu: ")
    if pilihan_menu == "1":
        tampilkan_tanaman()
    elif pilihan_menu == "2":
        print("Keluar dari program.")
    else:
        print("Pilihan tidak valid, silakan coba lagi.")