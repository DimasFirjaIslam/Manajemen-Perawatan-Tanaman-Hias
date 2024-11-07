import os
from utility import clear_screen
import data.data_user as data_user
import data.data_tanaman as data_tanaman
import main

# Keterangan: Hanya gunakan variabel pilihan untuk pilihan menu
username = ""
pilihan_menu = ""
riwayatHalaman = []
halaman = ""

def logged_in():
    return True if username.strip() else False

def logout():
    global username, riwayatHalaman, halaman
    username = ""
    riwayatHalaman.clear()
    halaman = ""

def tampilkan_tanaman():
    data = data_tanaman.load_data_tanaman()
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

def tampilkan_user():
    data = data_user.load_data_user()
    if data:
        for index, item in enumerate(data, start=1):
            print(f"""{index}.
            Username : {item['username']}
            Role     : {item['role']}
            """)
    else:
        print("Tidak ada data yang tersedia.")

def menu_awal():
    clear_screen()
    global halaman, pilihan_menu, username

    print("=" * 10 + " Menu Awal " + "=" * 10)
    print("1. Registrasi")
    print("2. Log in")
    
    print("N. Keluar Program")

    pilihan_menu = input("Masukkan Angka Menu Pilihan: ").lower()
    if pilihan_menu == "1":
        print("=" * 10 + " Registrasi " + "=" * 10)
        username_baru = input("Masukkan Username Baru: ")
        password_baru = input("Masukkan Password Baru: ")
        user_exists = any(user["username"] == username_baru for user in data_user.load_data_user())

        if user_exists:
            input("Username Sudah Terdaftar")
        else:
            data_user.register(username_baru, password_baru)
            print("Registrasi Berhasil")

    elif pilihan_menu == "2":
        input_username = input("Username: ")
        input_password = input("Password: ")
        user_login_data = data_user.login(input_username, input_password)

        if user_login_data:
            username = user_login_data['username']
            halaman = "menu_utama"
            if user_login_data['role'].lower() == "admin":
                MenuAdmin()
            else:
                MenuUser()
        else:
            print("Username atau password salah")
    elif pilihan_menu == "N":
        print("Program Selesai, Terimakasih Telah Menggunakan Layanan Kami")
    else:
        print("Pilihan Tidak Valid")
        input("Tekan Enter Untuk Kembali")

def kembali():
    global halaman
    for i in range(2):
        if len(riwayatHalaman) > 0:
            halaman = riwayatHalaman.pop()
    
def setup_halaman():
    try:
        if riwayatHalaman[len(riwayatHalaman) - 1] != halaman:
            riwayatHalaman.append(halaman)
    except IndexError:
        riwayatHalaman.append(halaman)
    
def MenuUtama():
    global halaman, pilihan_menu
    setup_halaman()
    
    print("Menu Utama")
    print("1. Manajemen Tanaman")
    print("2. Manajemen User")
    print()
    print("L. Log Out")
    print("N. Keluar")

    pilihan_menu = input("Pilih menu: ").lower()
    if pilihan_menu == "1":
        halaman = "manajemen_tanaman"
    elif pilihan_menu == "2":
        halaman = "manajemen_user"
    elif pilihan_menu == "l":
        input("Berhasil logout...!")
        logout()
    elif pilihan_menu == "n":
        input("Keluar program...!")
        logout()
    else:
        input("Input tidak valid, silakan coba lagi.")

def ManajemenTanaman():
    global halaman, pilihan_menu
    setup_halaman()

    print("Manajemen Tanaman")
    print("1. Lihat Tanaman")
    print("2. Tambah Data")
    print("3. Edit Data")
    print("4. Hapus Data")
    print()
    print("B. Kembali")
    print("N. Keluar")

    pilihan_menu = input("Pilih menu:").lower()
    if pilihan_menu == "1":
        tampilkan_tanaman()
        input("Kembali ke menu...")
    elif pilihan_menu == "2":
        tampilkan_tanaman()
        data_tanaman.tambah_tanaman()
    elif pilihan_menu == "3":
        tampilkan_tanaman()
        data_tanaman.edit_tanaman()
    elif pilihan_menu == "4":
        tampilkan_tanaman()
        data_tanaman.hapus_tanaman()
    elif pilihan_menu == "b":
        kembali()
    elif pilihan_menu == "l":
        logout()
        input("Berhasil Logout...!")
    elif pilihan_menu == "n":
        logout()
        input("Berhasil Keluar...!")

def ManajemenUser():
    global halaman, pilihan_menu
    setup_halaman()

    print("Manajemen User")
    print("1. Lihat User")
    print("2. Tambah User")
    print("3. Edit User")
    print("4. Hapus User")
    print()
    print("B. Kembali")
    print("N. Keluar")

    pilihan_menu = input("Pilih menu:").lower()
    if pilihan_menu == "1":
        tampilkan_user()
        input("Kembali ke menu...")
    elif pilihan_menu == "2":
        tampilkan_user()
        data_user.tambah_user()
    elif pilihan_menu == "3":
        tampilkan_user()
        data_user.edit_user()
    elif pilihan_menu == "4":
        tampilkan_user()
        data_user.hapus_user()
    elif pilihan_menu == "b":
        kembali()
    elif pilihan_menu == "l":
        logout()
        input("Berhasil Logout...!")
    elif pilihan_menu == "n":
        logout()
        input("Berhasil Keluar...!")


def MenuAdmin():
    while logged_in():
        clear_screen()

        if halaman == "menu_utama":
            MenuUtama()
        elif halaman == "manajemen_tanaman":
            ManajemenTanaman()
        elif halaman == "manajemen_user":
            ManajemenUser()

def MenuUser():
    clear_screen()
    global username, pilihan_menu

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