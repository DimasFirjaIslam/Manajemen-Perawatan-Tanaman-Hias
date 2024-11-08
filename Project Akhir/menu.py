from utility import *
import data.data_user as data_user
import data.data_tanaman as data_tanaman

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

def menu_register():
    clear_screen()
    try:
        judul_halaman("Registrasi")
        print("(Ket: Kosongkan input untuk kembali.)")
        username_baru = input_string("Username: ")
        if not username_baru: return
        elif any(user["username"] == username_baru for user in data_user.load_data_user()):
            raise ValueError("Username sudah terdaftar!")
        password_baru = input("Password: ")
        if not password_baru: return

        data_user.register(username_baru, password_baru)
        print()
        input("Registrasi Berhasil...!")
    except ValueError as e:
        print()
        input(e)
        menu_register()

def menu_awal():
    clear_screen()
    global halaman, pilihan_menu, username

    judul_halaman("Menu Awal")
    print("1 > Registrasi")
    print("2 > Log in")
    print()
    print("N > Keluar Program")
    separator()

    pilihan_menu = input("Pilih Menu >> ").lower()
    if pilihan_menu == "1":
        menu_register()
    elif pilihan_menu == "2":
        clear_screen()
        judul_halaman("Log in")
        input_username = input("Username: ")
        if not input_username: return
        input_password = input("Password: ")
        if not input_password: return
        user_login_data = data_user.login(input_username, input_password)

        if user_login_data:
            print()
            input(f"Berhasil Login...!")
            username = user_login_data['username']
            halaman = "menu_utama"
            if user_login_data['role'].lower() == data_user.level[0]:
                menu_admin()
            else:
                menu_user()
        else:
            print()
            input("Username atau password salah...!")
    elif pilihan_menu != "n":
        print()
        input("Pilihan tidak valid, silakan coba lagi...")

def menu_admin():
    while logged_in():
        setup_halaman()

        if halaman == "menu_utama":
            menu_utama()
        elif halaman == "manajemen_tanaman":
            manajemen_tanaman()
        elif halaman == "manajemen_user":
            manajemen_user()
        elif halaman == "pengaturan":
            menu_pengaturan()

def menu_moderator():
    while logged_in():
        setup_halaman()

        if halaman == "menu_utama":
            menu_utama()
        elif halaman == "manajemen_tanaman":
            manajemen_tanaman()
        elif halaman == "pengaturan":
            menu_pengaturan()

def menu_user():
    while logged_in():
        setup_halaman()

        if halaman == "menu_utama":
            menu_utama()
        elif halaman == "manajemen_tanaman":
            manajemen_tanaman()
        elif halaman == "pengaturan":
            menu_pengaturan()

def tampilkan_tanaman():
    data = data_tanaman.load_data_tanaman()
    if data:
        for index, item in enumerate(data, start=1):
            print(f"""{index}.
            Nama         : {item['nama']}
            Jenis        : {item['jenis']}
            Jadwal Siram : {item['jadwal_siram']}
            Suhu         : {item['suhu']}
            Pemupukan    : {item['pemupukan']}
            Media Tanam  : {item['media_tanam']}
            """)
    else:
        print("Tidak ada data yang tersedia.")

def tampilkan_user(roles = []):
    data = data_user.load_data_user(roles)
    if data:
        for index, item in enumerate(data, start=1):
            print(f"""{index}.
            Username : {item['username']}
            Role     : {item['role']}
            """)
    else:
        print("Tidak ada data yang tersedia.")

def kembali():
    global halaman
    for i in range(2):
        if len(riwayatHalaman) > 0:
            halaman = riwayatHalaman.pop()
    
def setup_halaman():
    global halaman, riwayatHalaman
    clear_screen()
    try:
        if riwayatHalaman[len(riwayatHalaman) - 1] != halaman:
            riwayatHalaman.append(halaman)
    except IndexError:
        riwayatHalaman.append(halaman)
    
def menu_utama():
    global halaman, pilihan_menu
    
    judul_halaman("Menu Utama")
    print("Selamat datang, " + username + "!")
    print()
    if data_user.cek_admin(username):
        print("1 > Dashboard")
        print("2 > Manajemen Tanaman")
        print("3 > Manajemen User")
        print()
        print("S > Pengaturan")
        print("N > Keluar")
        print
        separator()

        pilihan_menu = input("Pilih Menu >> ").lower()
        if pilihan_menu == "1":
            clear_screen()
            judul_halaman("Dashboard")
            print("Jumlah Tanaman: " + str(len(data_tanaman.load_data_tanaman())))
            print("Jumlah User: " + str(len(data_user.load_data_user())))
            separator()
            input("Kembali ke menu...")
        elif pilihan_menu == "2":
            halaman = "manajemen_tanaman"
        elif pilihan_menu == "3":
            halaman = "manajemen_user"
        elif pilihan_menu == "s":
            halaman = "pengaturan"
        elif pilihan_menu != "n":
            input("Pilihan tidak valid, silakan coba lagi...")
    elif data_user.cek_moderator(username):
        print("1 > Manajemen Tanaman")
        print()
        print("S > Pengaturan")
        print("N > Keluar")
        separator()

        pilihan_menu = input("Pilih Menu >> ").lower()
        if pilihan_menu == "1":
            halaman = "manajemen_tanaman"
        elif pilihan_menu == "s":
            halaman = "pengaturan"
        elif pilihan_menu != "n":
            input("Pilihan tidak valid, silakan coba lagi...")
    else:
        print("1 > Manajemen Tanaman")
        print()
        print("S > Pengaturan")
        print("N > Keluar")
        separator()

        pilihan_menu = input("Pilih Menu >> ").lower()
        if pilihan_menu == "1":
            halaman = "manajemen_tanaman"
        elif pilihan_menu == "s":
            halaman = "pengaturan"
        elif pilihan_menu != "n":
            input("Pilihan tidak valid, silakan coba lagi...")
    if pilihan_menu == "n":
        logout()

def manajemen_tanaman():
    global halaman, pilihan_menu

    judul_halaman("Manajemen Tanaman")
    if data_user.cek_admin(username) or data_user.cek_moderator(username):
        print("1 > Lihat Tanaman")
        print("2 > Tambah Tanaman")
        print("3 > Edit Tanaman")
        print("4 > Hapus Tanaman")
        print()
        print("B > Kembali")
        print("S > Pengaturan")
        print("N > Keluar")
        separator()

        pilihan_menu = input("Pilih Menu >> ").lower()
        if pilihan_menu == "1":
            clear_screen()
            tampilkan_tanaman()
            input("Kembali ke menu...")
        elif pilihan_menu == "2":
            clear_screen()
            tampilkan_tanaman()
            data_tanaman.tambah_tanaman()
        elif pilihan_menu == "3":
            clear_screen()
            tampilkan_tanaman()
            data_tanaman.edit_tanaman()
        elif pilihan_menu == "4":
            clear_screen()
            tampilkan_tanaman()
            data_tanaman.hapus_tanaman()
        elif pilihan_menu == "b":
            kembali()
        elif pilihan_menu == "s":
            halaman = "pengaturan"
        elif pilihan_menu != "n":
            print()
            input("Pilihan tidak valid, silakan coba lagi...")
    else:
        print("1 > Lihat Tanaman")
        print()
        print("B > Kembali")
        print("S > Pengaturan")
        print("N > Keluar")
        separator()

        pilihan_menu = input("Pilih Menu >> ").lower()
        if pilihan_menu == "1":
            clear_screen()
            tampilkan_tanaman()
            input("Kembali ke menu...")
        elif pilihan_menu == "b":
            kembali()
        elif pilihan_menu == "s":
            halaman = "pengaturan"
        elif pilihan_menu != "n":
            print()
            input("Pilihan tidak valid, silakan coba lagi...")
    if pilihan_menu == "n":
        logout()

def manajemen_user():
    global halaman, pilihan_menu

    judul_halaman("Manajemen User")
    print("1 > Lihat User")
    print("2 > Register User")
    print("3 > Blokir User")
    print("4 > Edit Moderator")
    print()
    print("B > Kembali")
    print("S > Pengaturan")
    print("N > Keluar")
    separator()

    pilihan_menu = input("Pilih Menu >> ").lower()
    if pilihan_menu == "1":
        clear_screen()
        tampilkan_user()
        input("Kembali ke menu...")
    elif pilihan_menu == "2":
        clear_screen()
        menu_register()
    elif pilihan_menu == "3":
        ...
    elif pilihan_menu == "4":
        clear_screen()
        judul_halaman("Moderator")
        tampilkan_user([data_user.level[1], data_user.level[2]])
        data_user.edit_status_moderator()
    elif pilihan_menu == "b":
        kembali()
    elif pilihan_menu == "s":
        halaman = "pengaturan"
    elif pilihan_menu == "n":
        logout()
    else:
        print()
        input("Pilihan tidak valid, silakan coba lagi...")

def menu_pengaturan():
    global halaman, pilihan_menu, username

    judul_halaman("Pengaturan")
    print("1 > Ubah Username")
    print("2 > Ubah Password")
    print("3 > Log Out")
    print()
    print("B > Kembali")
    print("N > Keluar")
    separator()

    pilihan_menu = input("Pilih Menu >> ").lower()
    if pilihan_menu == "1":
        clear_screen()
        judul_halaman("Ubah Username")
        print("(Ket: Kosongkan input untuk kembali.)")
        username_baru = input_string("Masukkan username baru: ")
        if not username_baru: return
        if (data_user.edit_username(username, username_baru)):
            print()
            input("Username berhasil diubah...!")
            username = username_baru
    elif pilihan_menu == "2":
        clear_screen()
        judul_halaman("Ubah Password")
        print("(Ket: Kosongkan input untuk kembali.)")
        password_baru = input("Masukkan password baru: ")
        if not password_baru: return
        if (data_user.edit_password(username, password_baru)):
            print()
            input("Password berhasil diubah...!")
    elif pilihan_menu == "3":
        print()
        input("Berhasil Logout...!")
        logout()
    elif pilihan_menu == "b":
        kembali()
    elif pilihan_menu == "n":
        logout()
    else:
        print()
        input("Pilihan tidak valid, silakan coba lagi...")