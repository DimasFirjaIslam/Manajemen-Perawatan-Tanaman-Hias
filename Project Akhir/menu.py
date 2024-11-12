from utility import *
import data.data_user as data_user
import data.data_tanaman as data_tanaman

username = ""
pilihan_menu = ""
riwayatHalaman = []
halaman = ""

# ------------------------------------------------------------

def cek_login():
    return True if username.strip() else False

def logout():
    global username, riwayatHalaman, halaman
    username = ""
    riwayatHalaman.clear()
    halaman = ""

# ------------------------------------------------------------

def form_register():
    clear_screen()
    try:
        judul_halaman("Registrasi")
        print("(Ket: Kosongkan input untuk kembali.)")
        print()
        input_username = input_string("Username: ").strip()
        if not input_username:
            return
        elif any(user["username"].strip().lower() == input_username.strip().lower() for user in data_user.load_data_user()):
            raise ValueError("Username sudah terdaftar!")
        
        input_password = input_string("Password: ").strip()
        if not input_password:
            return

        registrasi_data = data_user.registrasi(input_username, input_password)
        if registrasi_data.get("status"):
            print()
            input(registrasi_data.get("message"))
    except ValueError as e:
        print()
        input(e)
        form_register()

def menu_login():
    global username, halaman
    clear_screen()
    try:
        judul_halaman("Log in")
        print("(Ket: Kosongkan input untuk kembali.)")
        print()
        input_username = input("Username: ")
        if not input_username:
            return
        input_password = input("Password: ")
        if not input_password:
            return
        
        user_login_data = data_user.login(input_username, input_password)
        print()
        input(user_login_data.get("message"))
        if user_login_data.get("status"):
            username = user_login_data["data"]['username']
            halaman = "menu_utama"
            if user_login_data["data"]['role'].lower() == data_user.level[0]:
                menu_admin()
            else:
                menu_user()
    except Exception or KeyboardInterrupt:
        return
        
# ------------------------------------------------------------

def tampilkan_tanaman():
    data = []
    for i, item in enumerate(data_tanaman.load_data_tanaman()):
        data.append({
            "No": i + 1,
            "Nama": item["nama"],
            "Jenis": item["jenis"],
            "Jadwal Siram": item["jadwal_siram"],
            "Suhu": f"{item['min_suhu']}{"—" + str(item['max_suhu']) if item['max_suhu'] > item['min_suhu'] else ""} °C",
            "Pemupukan": item["pemupukan"],
            "Media Tanam": item["media_tanam"]
        })

    if data:
        dt = tabel(data)
        print(dt)
    else:
        print()
        print("Tidak ada data yang tersedia.")
    print()

def tampilkan_jenis_tanaman():
    for i, item in enumerate(data_tanaman.jenis, start=1):
        print(f"{i} > {item}")
    print()

def tampilkan_media_tanam():
    for i, item in enumerate(data_tanaman.media_tanam, start=1):
        print(f"{i} > {item}")
    print()

def tampilkan_satuan_waktu():
    for i, item in enumerate(data_tanaman.satuan_waktu, start=1):
        print(f"{i} > {item}")
    print()

def form_tambah_tanaman():
    clear_screen()
    judul_halaman("Tambah Tanaman")
    print("(Ket: Kosongkan input untuk kembali.)")
    print()
    nama = input_string("Nama Tanaman: ")
    satuan_waktu = data_tanaman.satuan_waktu
    if nama:
        if not any(tanaman["nama"].strip().lower() == nama.strip().lower() for tanaman in data_tanaman.load_data_tanaman()):
            print()
            tampilkan_jenis_tanaman()
            pilihan_jenis = input_pilihan("Jenis Tanaman: ", range(1, len(data_tanaman.jenis) + 1))
            if not pilihan_jenis: return
            jenis = data_tanaman.jenis[pilihan_jenis - 1]

            print()
            tampilkan_satuan_waktu()
            satuan_siram = input_pilihan("Jadwal Siram: ", range(1, len(satuan_waktu) + 1))
            if satuan_siram:
                jadwal_siram = input_int(f"Berapa lama waktu ({satuan_waktu[satuan_siram - 1]}) untuk setiap siram: ")
                if not jadwal_siram: return
                jadwal_siram = f"{jadwal_siram} {satuan_waktu[satuan_siram - 1]} Sekali"
            else:
                return
            
            min_suhu = input_float("Suhu Minimum: ")
            if not min_suhu: return
            while True:
                max_suhu = input_float("Suhu Maksimum: ")
                if not max_suhu: return
                if max_suhu <= min_suhu:
                    print()
                    input("Suhu maksimum harus lebih besar dari suhu minimum...!")
                    continue
                break

            print()
            tampilkan_satuan_waktu()
            satuan_pemupukan = input_pilihan("Satuan Waktu Pemupukan: ", range(1, len(satuan_waktu) + 1))
            if satuan_pemupukan:
                pemupukan = input_int(f"Berapa lama waktu ({satuan_waktu[satuan_pemupukan - 1]}) untuk setiap pemupukan: ")
                if not pemupukan: return
                pemupukan = f"{pemupukan} {satuan_waktu[satuan_pemupukan - 1]} Sekali"
            else:
                return
            
            print()
            tampilkan_media_tanam()                               
            pilihan_media = input_pilihan("Media Tanam: ", range(1, len(data_tanaman.media_tanam) + 1))
            if not pilihan_media: return
            media_tanam = data_tanaman.media_tanam[pilihan_media - 1]

            tambah_data = data_tanaman.tambah_tanaman(nama, jenis, jadwal_siram, min_suhu, max_suhu, pemupukan, media_tanam)

            print()
            input(tambah_data.get("message"))
        else:
            print()
            input("Tanaman sudah ada...!")
            form_tambah_tanaman()

def form_edit_tanaman():
    try:
        clear_screen()
        judul_halaman("Edit Tanaman")
        tampilkan_tanaman()
        data = data_tanaman.load_data_tanaman()

        print("(Ket: Kosongkan input untuk mempertahankan nilai lama.)")
        indeks_tanaman = input("Nomor Tanaman: ")
        if indeks_tanaman.strip():
            if not indeks_tanaman.isdigit():
                raise ValueError("Nomor tanaman harus berupa angka...!")
            indeks_tanaman = int(indeks_tanaman) - 1

            if indeks_tanaman < 0 or indeks_tanaman >= len(data):
                raise IndexError("Tanaman tidak ditemukan...!")
            tanaman = data[indeks_tanaman]
        else:
            return
    
        while True:
            nama = input_string("Nama Tanaman: ") or tanaman["nama"]
            if any(tanaman["nama"].strip().lower() == nama.strip().lower() and tanaman["nama"] != data[indeks_tanaman]["nama"] for tanaman in data):
                print()
                input("Tanaman sudah ada...!")
                continue
            break

        print()
        tampilkan_jenis_tanaman()
        jenis = input_pilihan("Jenis Tanaman: ", range(1, len(data_tanaman.jenis) + 1) or data[indeks_tanaman]["jenis"])
        
        print()
        tampilkan_satuan_waktu()
        satuan_siram = input_pilihan("Satuan Waktu Penyiraman: ", range(1, len(data_tanaman.satuan_waktu) + 1) or data[indeks_tanaman]["jadwal_siram"])
        if satuan_siram:
            jadwal_siram = input_int(f"Berapa lama waktu ({data_tanaman.satuan_waktu[satuan_siram - 1]}) untuk setiap siram: ") or data[indeks_tanaman]["jadwal_siram"]
            jadwal_siram = f"{jadwal_siram} {data_tanaman.satuan_waktu[satuan_siram - 1]} Sekali"
        
        min_suhu = input_float("Suhu Minimum: ") or data[indeks_tanaman]["min_suhu"]
        if min_suhu:
            while True:
                max_suhu = input_float("Suhu Maksimum: ") or data[indeks_tanaman]["max_suhu"]
                if max_suhu <= min_suhu:
                    print()
                    input("Suhu maksimum harus lebih besar dari suhu minimum...!")
                    continue
                break

        print()
        tampilkan_satuan_waktu()
        satuan_pemupukan = input_pilihan("Satuan Waktu Pemupukan: ", range(1, len(data_tanaman.satuan_waktu) + 1) or data[indeks_tanaman]["pemupukan"])
        if satuan_pemupukan:
            pemupukan = input_int(f"Berapa lama waktu ({data_tanaman.satuan_waktu[satuan_pemupukan - 1]}) untuk setiap pemupukan: ") or data[indeks_tanaman]["pemupukan"]
            pemupukan = f"{pemupukan} {data_tanaman.satuan_waktu[satuan_pemupukan - 1]} Sekali"
        
        print()
        tampilkan_media_tanam()
        pilihan_media = input_pilihan("Media Tanam: ", range(1, len(data_tanaman.media_tanam) + 1) or data[indeks_tanaman]["media_tanam"])
        media_tanam = data_tanaman.media_tanam[pilihan_media - 1]

        edit_data = data_tanaman.edit_tanaman(indeks_tanaman, nama, jenis, jadwal_siram, min_suhu, max_suhu, pemupukan, media_tanam)
        
        print()
        input(edit_data.get("message"))
    except Exception as e:
        print()
        input(e)
        form_edit_tanaman()

def form_hapus_tanaman():
    try:
        clear_screen()
        judul_halaman("Hapus Tanaman")
        tampilkan_tanaman()
        data = data_tanaman.load_data_tanaman()

        print("Ket: Kosongkan input untuk kembali.")
        indeks_tanaman = input("Nomor Tanaman: ")
        if indeks_tanaman.strip():
            if not indeks_tanaman.isdigit():
                raise ValueError("Nomor tanaman harus berupa angka...!")
            indeks_tanaman = int(indeks_tanaman) - 1

            if indeks_tanaman < 0 or indeks_tanaman >= len(data):
                raise IndexError("Tanaman tidak ditemukan...!")
        else:
            return
        
        if (dialog_konfirmasi(f"Yakin ingin menghapus {data[indeks_tanaman]['nama']}?")):
            hapus_data = data_tanaman.hapus_tanaman(indeks_tanaman)
            print()
            input(hapus_data.get("message"))
        else:
            print()
            input("Batal menghapus tanaman...!")
    except Exception as e:
        print()
        input(e)
        form_hapus_tanaman()

def tampilkan_user_role(roles = [data_user.level[0], data_user.level[1], data_user.level[2]]):
    data = []
    for i, item in enumerate(data_user.load_data_user(roles)):
        data.append({
            "No": i + 1,
            "Username": item["username"],
            "Role": item["role"],
        })
    
    if data:
        dt = tabel(data)
        print(dt)
    else:
        print()
        print("Tidak ada data yang tersedia.")

def tampilkan_user_status(roles = [data_user.level[0], data_user.level[1], data_user.level[2]]):
    data = []
    for i, item in enumerate(data_user.load_data_user(roles)):
        data.append({
            "No": i + 1,
            "Username": item["username"],
            "Status": item["status"],
        })
    
    if data:
        dt = tabel(data)
        print(dt)
    else:
        print()
        print("Tidak ada data yang tersedia.")

# Fungsi untuk menambahkan atau menghapus role "Moderator" pada pengguna
def form_edit_moderator():
    try:
        clear_screen()
        judul_halaman("Moderator")
        tampilkan_user_role([data_user.level[1], data_user.level[2]])        
        data = data_user.load_data_user([data_user.level[1], data_user.level[2]])
        
        print("Ket: Kosongkan input untuk kembali.")
        indeks_user = input("Nomor Pengguna: ")
        if indeks_user.strip():
            if not indeks_user.isdigit():
                raise ValueError("Nomor pengguna harus berupa angka...!")
            indeks_user = int(indeks_user) - 1

            if indeks_user < 0 or indeks_user >= len(data):
                raise IndexError("Pengguna tidak ditemukan...!")
            user = data[indeks_user]
            global_indeks_user = data_user.indeks_user(user["username"])
        else:
            return

        # Jika status role pengguna adalah "User", maka akan dipromosikan menjadi "Moderator"
        if user["role"] == data_user.level[2]:
            if dialog_konfirmasi(f"Yakin ingin menambahkan {user['username']} sebagai Moderator?"):
                data_user.edit_user(global_indeks_user, user["username"], user["password"], data_user.level[1], user["status"])
                input(f"Berhasil menambahkan Moderator...!")
            else:
                input("Batal menambahkan Moderator...!")
        
        # Jika status role pengguna sudah "Moderator", maka akan dikembalikan menjadi role "User"
        elif user["role"] == data_user.level[1]:
            if dialog_konfirmasi(f"Yakin ingin menghapus {user['username']} sebagai Moderator?"):
                data_user.edit_user(global_indeks_user, user["username"], user["password"], data_user.level[2], user["status"])
                input(f"Berhasil menghapus Moderator...!")
            else:
                input("Batal menghapus Moderator...!")
    except Exception as e:
        print()
        input(e)
        form_edit_moderator()

def form_edit_blokir():
    try:
        clear_screen()
        judul_halaman("Blokir User")
        tampilkan_user_status([data_user.level[1], data_user.level[2]])
        data = data_user.load_data_user([data_user.level[1], data_user.level[2]])

        print("Ket: Kosongkan input untuk kembali.")
        indeks_user = input("Nomor Pengguna: ")
        if indeks_user.strip():
            if not indeks_user.isdigit():
                raise ValueError("Nomor pengguna harus berupa angka...!")
            indeks_user = int(indeks_user) - 1
            input(indeks_user)

            if indeks_user < 0 or indeks_user >= len(data):
                raise IndexError("Pengguna tidak ditemukan...!")
            user = data[indeks_user]
            global_indeks_user = data_user.indeks_user(user["username"])
        else:
            return
        
        if user["status"] == data_user.status[0]:
            if dialog_konfirmasi(f"Yakin ingin memblokir {user['username']}?"):
                data_user.edit_user(global_indeks_user, user["username"], user["password"], user["role"], data_user.status[1])
                input(f"Berhasil memblokir pengguna...!")
            else:
                input("Batal memblokir pengguna...!")
        elif user["status"] == data_user.status[1]:
            if dialog_konfirmasi(f"Yakin ingin membuka blokir {user['username']}?"):
                data_user.edit_user(global_indeks_user, user["username"], user["password"], user["role"], data_user.status[0])
                input(f"Berhasil membuka blokir pengguna...!")
            else:
                input("Batal membuka blokir pengguna...!")
    except Exception as e:
        print()
        input(e)
        form_edit_blokir()

def detail_tanaman(indeks_tanaman):
    clear_screen()
    judul_halaman("Detail Tanaman")
    data = data_tanaman.load_data_tanaman()
    tanaman = data[indeks_tanaman]

    print(f"Nama Tanaman: {tanaman['nama']}")
    print(f"Jenis Tanaman: {tanaman['jenis']}")
    print(f"Jadwal Siram: {tanaman['jadwal_siram']}")
    print(f"Suhu: {tanaman['min_suhu']}{"—" + str(tanaman['max_suhu']) if tanaman['max_suhu'] > tanaman['min_suhu'] else ""} °C")
    print(f"Pemupukan: {tanaman['pemupukan']}")
    print(f"Media Tanam: {tanaman['media_tanam']}")
    print()
    input("Kembali ke menu...")
# ------------------------------------------------------------

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

# ------------------------------------------------------------
    
def menu_utama():
    global halaman, pilihan_menu
    
    judul_halaman("Menu Utama")
    print("Selamat datang, " + username + "!")
    print()

    # Menu Utama Admin
    if data_user.cek_admin(username):
        print("1 > Dashboard")
        print("2 > Manajemen Tanaman")
        print("3 > Manajemen User")
        print()
        print("S > Pengaturan")
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
        else:
            input("Pilihan tidak valid, silakan coba lagi...")
            pilihan_menu = ""
    
    # Menu Utama Moderator
    elif data_user.cek_moderator(username):
        print("1 > Manajemen Tanaman")
        print()
        print("S > Pengaturan")
        separator()

        pilihan_menu = input("Pilih Menu >> ").lower()
        if pilihan_menu == "1":
            halaman = "manajemen_tanaman"
        elif pilihan_menu == "s":
            halaman = "pengaturan"
        else:
            input("Pilihan tidak valid, silakan coba lagi...")
            pilihan_menu = ""
    
    # Menu Utama User
    else:
        print("1 > Manajemen Tanaman")
        print()
        print("S > Pengaturan")
        separator()

        pilihan_menu = input("Pilih Menu >> ").lower()
        if pilihan_menu == "1":
            halaman = "manajemen_tanaman"
        elif pilihan_menu == "s":
            halaman = "pengaturan"
        else:
            input("Pilihan tidak valid, silakan coba lagi...")
            pilihan_menu = ""

data_page = 1
def manajemen_tanaman():
    global halaman, pilihan_menu, data_page

    data = data_tanaman.load_data_tanaman()
    data_per_page = 5
    total_halaman = int((len(data) - 1) / data_per_page) + 1

    nomor_indeks_tersedia = {}

    judul_halaman("Manajemen Tanaman")

    # Menu Manajemen Tanaman Admin/Moderator
    if data_user.cek_admin(username) or data_user.cek_moderator(username):
        # print("1 > Lihat Tanaman")
        print("A > Tambah Tanaman")
        print("U > Edit Tanaman")
        print("D > Hapus Tanaman")
        print("F > Filter")
        print()
        for i, item in enumerate(data):
            if i >= (data_page - 1) * 5 and i < data_page * 5:
                print(f"{i + 1} > {item['nama']} ({item['jenis']})")
                nomor_indeks_tersedia[str(i + 1)] = data_tanaman.cek_index(item["nama"])

        print()
        print(f"({data_page} dari {total_halaman} halaman)")
        if data_page > 1:
            print("Q > Halaman Sebelumnya", end=" ")
        if data_page > 1 and data_page < total_halaman:
            print("|", end=" ")
        if data_page < total_halaman:
            print("E > Halaman Selanjutnya", end=" ")
        
        print()
        print("B > Kembali")
        print("S > Pengaturan")
        separator()

        pilihan_menu = input("Pilih Menu >> ").lower()
        # if pilihan_menu == "1":
        #     clear_screen()
        #     judul_halaman("Data Tanaman")
        #     tampilkan_tanaman()
        #     input("Kembali ke menu...")
        if pilihan_menu == "a":
            form_tambah_tanaman()
        elif pilihan_menu == "u":
            form_edit_tanaman()
        elif pilihan_menu == "d":
            form_hapus_tanaman()
        elif any(pilihan_menu == str(nomor) for nomor in nomor_indeks_tersedia):
            detail_tanaman(nomor_indeks_tersedia[pilihan_menu])
        elif pilihan_menu == "q" and data_page > 1:
            data_page -= 1
            manajemen_tanaman()
        elif pilihan_menu == "e" and data_page < total_halaman:
            data_page += 1
            manajemen_tanaman()
        elif pilihan_menu == "b":
            kembali()
        elif pilihan_menu == "s":
            halaman = "pengaturan"
        elif pilihan_menu != "n":
            print()
            input("Pilihan tidak valid, silakan coba lagi...")

    # Menu Manajemen Tanaman User
    else:
        print("1 > Lihat Tanaman")
        print()
        print("B > Kembali")
        print("S > Pengaturan")
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
        else:
            print()
            input("Pilihan tidak valid, silakan coba lagi...")
            pilihan_menu = ""

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
    separator()

    pilihan_menu = input("Pilih Menu >> ").lower()
    if pilihan_menu == "1":
        clear_screen()
        judul_halaman("Data User")
        tampilkan_user_role()
        input("Kembali ke menu...")
    elif pilihan_menu == "2":
        form_register()
    elif pilihan_menu == "3":
        form_edit_blokir()
    elif pilihan_menu == "4":
        form_edit_moderator()
    elif pilihan_menu == "b":
        kembali()
    elif pilihan_menu == "s":
        halaman = "pengaturan"
    else:
        print()
        input("Pilihan tidak valid, silakan coba lagi...")
        pilihan_menu = ""

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

# ------------------------------------------------------------

def menu_awal():
    clear_screen()
    try:
        global halaman, pilihan_menu, username

        judul_halaman("Menu Awal")
        print("1 > Registrasi")
        print("2 > Log in")
        print()
        print("N > Keluar Program")
        separator()

        pilihan_menu = input("Pilih Menu >> ").lower()
        if pilihan_menu == "1":
            form_register()
        elif pilihan_menu == "2":
            menu_login()
        elif pilihan_menu != "n":
            print()
            input("Pilihan tidak valid, silakan coba lagi...")
    except Exception or KeyboardInterrupt as e:
        return

def menu_admin():
    try:
        while cek_login():
            setup_halaman()

            if halaman == "menu_utama":
                menu_utama()
            elif halaman == "manajemen_tanaman":
                manajemen_tanaman()
            elif halaman == "manajemen_user":
                manajemen_user()
            elif halaman == "pengaturan":
                menu_pengaturan()
    except Exception or KeyboardInterrupt as e:
        input(e)
        menu_admin()

def menu_moderator():
    try:
        while cek_login():
            setup_halaman()

            if halaman == "menu_utama":
                menu_utama()
            elif halaman == "manajemen_tanaman":
                manajemen_tanaman()
            elif halaman == "pengaturan":
                menu_pengaturan()
    except Exception or KeyboardInterrupt as e:
        input(e)
        menu_moderator()

def menu_user():
    try:
        while cek_login():
            setup_halaman()

            if halaman == "menu_utama":
                menu_utama()
            elif halaman == "manajemen_tanaman":
                manajemen_tanaman()
            elif halaman == "pengaturan":
                menu_pengaturan()
    except Exception or KeyboardInterrupt as e:
        input(e)
        menu_user()

