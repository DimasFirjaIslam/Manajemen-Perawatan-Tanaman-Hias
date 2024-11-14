from utility import *
import data.data_user as data_user
import data.data_tanaman as data_tanaman
import data.data_diskusi as data_diskusi

username = ""
pilihan_menu = ""
riwayatHalaman = []
halaman = ""

# ------------------------------------------------------------
# Fungsi mengenai variabel login-logout di Menu

# Memeriksa apakah pengguna sudah login
def cek_login():
    return True if username.strip() else False

# Fungsi untuk logout (menghapus data login)
def logout():
    global username, riwayatHalaman, halaman
    username = ""
    riwayatHalaman.clear()
    halaman = ""

# ------------------------------------------------------------
# Fungsi Utilitas Halaman Menu

# Fungsi untuk kembali ke halaman sebelumnya dengan riwayat halaman
def kembali():
    global halaman
    for i in range(2):
        if len(riwayatHalaman) > 0:
            halaman = riwayatHalaman.pop()

# Fungsi yang selalu dilakukan saat halaman baru dibuka
def setup_halaman():
    global halaman, riwayatHalaman
    clear_screen()
    try:
        # Menambahkan halaman baru ke dalam riwayat halaman
        if riwayatHalaman[len(riwayatHalaman) - 1] != halaman:
            riwayatHalaman.append(halaman)
    except IndexError:
        riwayatHalaman.append(halaman)

# ------------------------------------------------------------
# Fungsi singkat untuk membuat tampilan data dari database

# Fungsi menampilkan data tanaman dalam bentuk tabel
def tampilkan_tanaman():
    data = []
    for i, item in enumerate(data_tanaman.load_data_tanaman()):
        data.append({
            "No": i + 1,
            "Nama": item["nama"],
            "Jenis": item["jenis"],
            "Jadwal Siram": item["jadwal_siram"],
            "Suhu": f"{item["min_suhu"]}{"—" + str(item["max_suhu"]) if item["max_suhu"] > item["min_suhu"] else ""} °C",
            "Pemupukan": item["pemupukan"],
            "Media Tanam": item["media_tanam"]
        })

    if data:
        dt = tabel(data)
        print(dt)
    else:
        print()
        print("Tidak ada data yang tersedia.")

# Fungsi menampilkan pilihan jenis tanaman
def tampilkan_jenis_tanaman():
    for i, item in enumerate(data_tanaman.jenis, start=1):
        print(f"{i} > {item}")
    print()

# Fungsi menampilkan pilihan media tanam
def tampilkan_media_tanam():
    for i, item in enumerate(data_tanaman.media_tanam, start=1):
        print(f"{i} > {item}")
    print()

# Fungsi menampilkan pilihan satuan waktu
def tampilkan_satuan_waktu():
    for i, item in enumerate(data_tanaman.satuan_waktu, start=1):
        print(f"{i} > {item}")
    print()

# Fungsi menampilkan username dan role pengguna dalam tabel
def tampilkan_user(roles = [], status = [], kolom = ["No", "Username", "Role", "Status"]):
    data = []
    for i, item in enumerate(data_user.load_data_user(roles, status)):
        data.append({})
        if "No" in kolom:
            data[i]["No"] = i + 1
        if "Username" in kolom:
            data[i]["Username"] = item["username"]
        if "Role" in kolom:
            data[i]["Role"] = item["role"]
        if "Status" in kolom:
            data[i]["Status"] = item["status"]
    
    if data:
        dt = tabel(data)
        print(dt)
    else:
        print()
        print("Tidak ada data yang tersedia.")

# ------------------------------------------------------------
# Mini Menu Tampilan Form CRUD

# Fungsi menampilkan form registrasi
def form_register():
    clear_screen()
    try:
        judul_halaman("Registrasi")
        print("(Ket: Kosongkan input untuk kembali.)")
        print()
        input_username = input_string("Username (Maks 24 Huruf): ")

        if not input_username:
            return
        elif len(input_username) > 24:
            raise ValueError("Username maksimal 24 karakter...!")
        if any(user["username"].lower() == input_username.lower() for user in data_user.load_data_user()):
            raise ValueError("Username sudah terdaftar!")
        
        while True:
            input_password = input_fixed("Password (Maks 16 Huruf): ")
            if not input_password:
                return
            elif len(input_password) > 16:
                print()
                input("Password maksimal 16 karakter...!")
                continue
            break

        registrasi_data = data_user.registrasi(input_username, input_password)
        if registrasi_data.get("status"):
            separator()
            input(registrasi_data.get("message"))
    except ValueError as e:
        print()
        input(e)
        form_register()

def form_login():
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
        separator()
        input(user_login_data.get("message"))
        if user_login_data.get("status"):
            username = user_login_data["data"]["username"]
            halaman = "menu_utama"
            if user_login_data["data"]["role"].lower() == data_user.role[0]:
                menu_admin()
            elif user_login_data["data"]["role"].lower() == data_user.role[1]:
                menu_moderator()
            else:
                menu_user()
    except Exception or KeyboardInterrupt:
        return

def form_tambah_tanaman():
    clear_screen()
    try:
        satuan_waktu = data_tanaman.satuan_waktu
        judul_halaman("Tambah Tanaman")
        print("(Ket: Kosongkan input untuk kembali.)")
        print()
        nama = input_string("Nama Tanaman (Maks 30 Huruf)\t: ")
            
        if not nama:
            return
        elif len(nama) > 30:
            raise ValueError("Nama tanaman maksimal 30 karakter...!")
        elif any(tanaman["nama"].strip() == nama for tanaman in data_tanaman.load_data_tanaman()):
            raise ValueError("Tanaman sudah terdaftar...!")

        separator()
        tampilkan_jenis_tanaman()
        pilihan_jenis = input_pilihan("Jenis Tanaman\t\t\t: ", range(1, len(data_tanaman.jenis) + 1))
        if not pilihan_jenis: return
        jenis = data_tanaman.jenis[pilihan_jenis - 1]

        separator()
        tampilkan_satuan_waktu()
        satuan_siram = input_pilihan("Satuan Lama Siram\t\t: ", range(1, len(satuan_waktu) + 1))
        if satuan_siram:
            while True:
                jadwal_siram = input_fixed(f"Lama Penyiraman ({satuan_waktu[satuan_siram - 1]})  \t: ")
                if jadwal_siram == "":
                    return
                elif not jadwal_siram.isdigit():
                    print()
                    input("Input harus angka...!")
                    continue
                break                    
            jadwal_siram = f"{jadwal_siram} {satuan_waktu[satuan_siram - 1]} Sekali"
        else:
            return
        
        separator()
        while True:
            min_suhu = input_fixed("Suhu Minimum (°C)\t\t: ")
            if min_suhu == "": return
            elif not min_suhu.isdigit():
                print()
                input("Input harus angka...!")
                continue
            min_suhu = float(min_suhu)
            
            while True:
                max_suhu = input_fixed("Suhu Maksimum (°C)\t\t: ")
                if max_suhu == "": return
                elif not max_suhu.isdigit():
                    print()
                    input("Input harus angka...!")
                    continue
                max_suhu = float(max_suhu)
                if max_suhu < min_suhu:
                    print()
                    input("Suhu maksimum harus lebih besar dari suhu minimum...!")
                    continue
                break
            break

        separator()
        tampilkan_satuan_waktu()
        satuan_pemupukan = input_pilihan("Satuan Lama Pemupukan\t\t: ", range(1, len(satuan_waktu) + 1))
        if satuan_pemupukan:
            while True:
                pemupukan = input_fixed(f"Lama Pemupukan ({satuan_waktu[satuan_pemupukan - 1]})\t\t: ")
                if pemupukan == "":
                    return
                elif not pemupukan.isdigit():
                    print()
                    input("Input harus angka...!")
                    continue
                break
            pemupukan = f"{pemupukan} {satuan_waktu[satuan_pemupukan - 1]} Sekali"
        else:
            return
        
        separator()
        tampilkan_media_tanam()                               
        pilihan_media = input_pilihan("Media Tanam\t\t\t: ", range(1, len(data_tanaman.media_tanam) + 1))
        if not pilihan_media: return
        media_tanam = data_tanaman.media_tanam[pilihan_media - 1]

        tambah_data = data_tanaman.tambah_tanaman(nama, jenis, jadwal_siram, min_suhu, max_suhu, pemupukan, media_tanam)

        separator()
        input(tambah_data.get("message"))
    except Exception as e:
        print()
        input(e)
        form_tambah_tanaman()

def form_edit_tanaman():
    try:
        clear_screen()
        judul_halaman("Edit Tanaman")
        tampilkan_tanaman()
        separator()
        data = data_tanaman.load_data_tanaman()

        if data:
            print("(Ket: Kosongkan input untuk mempertahankan nilai lama.)")
            indeks_tanaman = input("Nomor Tanaman\t\t\t: ")
            separator()
        else:
            input("Kembali ke menu...!")
            return
        
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
            nama = input_string("Nama Tanaman (Maks 30 Huruf)\t: ") or tanaman["nama"]
            if not nama:
                return
            elif len(nama) > 30:
                print()
                input("Nama tanaman maksimal 30 karakter...!")
                continue
            elif any(tanaman["nama"].lower() == nama.lower() and tanaman["nama"].lower() != data[indeks_tanaman]["nama"].lower() for tanaman in data):
                print()
                input("Tanaman sudah terdaftar...!")
                continue
            break

        separator()
        tampilkan_jenis_tanaman()
        pilihan_jenis = input_pilihan("Jenis Tanaman\t\t\t: ", range(1, len(data_tanaman.jenis) + 1) or data[indeks_tanaman]["jenis"])
        if not pilihan_jenis: return
        jenis = data_tanaman.jenis[pilihan_jenis - 1]
        
        separator()
        tampilkan_satuan_waktu()
        satuan_siram = input_pilihan("Satuan Lama Penyiraman\t\t: ", range(1, len(data_tanaman.satuan_waktu) + 1) or data[indeks_tanaman]["jadwal_siram"])
        if satuan_siram:
            while True:
                jadwal_siram = input_fixed(f"Lama Penyiraman ({data_tanaman.satuan_waktu[satuan_siram - 1]}) \t: ") or data[indeks_tanaman]["jadwal_siram"]
                if jadwal_siram == "":
                    return
                elif not jadwal_siram.isdigit():
                    print()
                    input("Input harus angka...!")
                    continue
                break
            jadwal_siram = f"{jadwal_siram} {data_tanaman.satuan_waktu[satuan_siram - 1]} Sekali"
        
        separator()
        while True:
            min_suhu = input_fixed("Suhu Minimum (°C)\t\t: ")
            if min_suhu == "": return
            elif not min_suhu.isdigit():
                print()
                input("Input harus angka...!")
                continue
            min_suhu = float(min_suhu)
            
            while True:
                max_suhu = input_fixed("Suhu Maksimum (°C)\t\t: ")
                if max_suhu == "": return
                elif not max_suhu.isdigit():
                    print()
                    input("Input harus angka...!")
                    continue
                max_suhu = float(max_suhu)
                if max_suhu < min_suhu:
                    print()
                    input("Suhu maksimum harus lebih besar dari suhu minimum...!")
                    continue
                break
            break

        separator()
        tampilkan_satuan_waktu()
        satuan_pemupukan = input_pilihan("Satuan Lama Pemupukan\t\t: ", range(1, len(data_tanaman.satuan_waktu) + 1) or data[indeks_tanaman]["pemupukan"])
        if satuan_pemupukan:
            while True:
                pemupukan = input_fixed(f"Lama Pemupukan ({data_tanaman.satuan_waktu[satuan_pemupukan - 1]})\t\t: ") or data[indeks_tanaman]["pemupukan"]
                if pemupukan == "":
                    return
                elif not pemupukan.isdigit():
                    print()
                    input("Input harus angka...!")
                    continue
                break
            pemupukan = f"{pemupukan} {data_tanaman.satuan_waktu[satuan_pemupukan - 1]} Sekali"
        
        separator()
        tampilkan_media_tanam()
        pilihan_media = input_pilihan("Media Tanam\t\t\t: ", range(1, len(data_tanaman.media_tanam) + 1) or data[indeks_tanaman]["media_tanam"])
        media_tanam = data_tanaman.media_tanam[pilihan_media - 1]

        edit_data = data_tanaman.edit_tanaman(indeks_tanaman, nama, jenis, jadwal_siram, min_suhu, max_suhu, pemupukan, media_tanam)
        
        separator()
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
        separator()
        data = data_tanaman.load_data_tanaman()

        if data:
            print("(Ket: Kosongkan input untuk kembali.)")
            indeks_tanaman = input("Nomor Tanaman: ")
        else:
            input("Kembali ke menu...!")
            return

        if indeks_tanaman.strip():
            if not indeks_tanaman.isdigit():
                raise ValueError("Nomor tanaman harus berupa angka...!")
            indeks_tanaman = int(indeks_tanaman) - 1

            if indeks_tanaman < 0 or indeks_tanaman >= len(data):
                raise IndexError("Tanaman tidak ditemukan...!")
        else:
            return
        
        if (dialog_konfirmasi(f"Yakin ingin menghapus {data[indeks_tanaman]["nama"]}?")):
            hapus_data = data_tanaman.hapus_tanaman(indeks_tanaman)
            separator()
            input(hapus_data.get("message"))
        else:
            print()
            input("Batal menghapus tanaman...!")
    except Exception as e:
        print()
        input(e)
        form_hapus_tanaman()

def form_edit_username():
    global username
    try:
        data = data_user.load_data_user()
        self_index = data_user.cek_indeks(username)
        used_user = data[self_index]

        clear_screen()
        judul_halaman("Ubah Username")
        print("(Ket: Kosongkan input untuk kembali.)")
        print()
        input_username = input_string("Username (Maks 24 Huruf): ")
        if not input_username:
            return
        elif len(input_username) > 24:
            raise ValueError("Username maksimal 24 karakter...!")
        elif any(user["username"] == input_username.lower() and username.lower() != input_username.lower() for user in data):
            raise ValueError("Username sudah terdaftar...!")
        
        if dialog_konfirmasi(f"Yakin ingin mengubah username menjadi {input_username}?"):
            edit_data = data_user.edit_user(self_index, input_username, used_user["password"], used_user["role"], used_user["status"])
            username = input_username
            separator()
            if edit_data["status"]:
                input("Berhasil mengubah username...!")
            else:
                input(edit_data["message"])
    except Exception as e:
        print()
        input(e)
        form_edit_username()

def form_edit_password():
    global username
    try:
        data = data_user.load_data_user()
        self_index = data_user.cek_indeks(username)
        used_user = data[self_index]

        clear_screen()
        judul_halaman("Ubah Password")
        print("(Ket: Kosongkan input untuk kembali.)")
        print()
        konfirmasi_password = input_fixed("Konfirmasi Password\t\t: ")
        if not konfirmasi_password:
            return
        elif konfirmasi_password != used_user["password"]:
            raise ValueError("Password salah...!")

        while True:
            input_password = input_fixed("Password (Maks 16 Huruf)\t: ")
            if not input_password:
                return
            elif len(input_password) > 16:
                print()
                input("Password maksimal 16 karakter...!")
                continue
            break

        if dialog_konfirmasi(f"Yakin ingin mengubah password?"):
            edit_data = data_user.edit_user(self_index, used_user["username"], input_password, used_user["role"], used_user["status"])
            separator()
            if edit_data["status"]:
                input("Berhasil mengubah password...!")
            else:
                input(edit_data["message"])
        else:
            input("Batal mengubah password...!")
    except Exception as e:
        print()
        input(e)
        form_edit_password()

# Fungsi untuk menambahkan atau menghapus role "Moderator" pada pengguna
def form_edit_moderator():
    try:
        clear_screen()
        judul_halaman("Moderator")
        roles = [data_user.role[1], data_user.role[2]]
        status = [data_user.status[0]]
        tampilkan_user(roles, status, kolom=["No", "Username", "Role"])        
        data = data_user.load_data_user(roles, status)
        print()
        
        if data:
            print("(Ket: Kosongkan input untuk kembali.)")
            indeks_user = input_fixed("Nomor Pengguna: ")
            if not indeks_user:
                return
            if not indeks_user.isdigit():
                raise ValueError("Nomor pengguna harus berupa angka...!")
            indeks_user = int(indeks_user) - 1

            if indeks_user < 0 or indeks_user >= len(data):
                raise IndexError("Pengguna tidak ditemukan...!")
            user = data[indeks_user]
            
            global_indeks_user = data_user.cek_indeks(user["username"])
        else:
            input("Kembali ke menu...!")
            return

        # Jika status role pengguna adalah "User", maka akan dipromosikan menjadi "Moderator"
        if user["role"] == data_user.role[2]:
            if dialog_konfirmasi(f"Yakin ingin menambahkan {user["username"]} sebagai Moderator?"):
                data_user.edit_user(global_indeks_user, user["username"], user["password"], data_user.role[1], user["status"])
                input(f"Berhasil menambahkan Moderator...!")
            else:
                input("Batal menambahkan Moderator...!")
        
        # Jika status role pengguna sudah "Moderator", maka akan dikembalikan menjadi role "User"
        elif user["role"] == data_user.role[1]:
            if dialog_konfirmasi(f"Yakin ingin menghapus {user["username"]} sebagai Moderator?"):
                data_user.edit_user(global_indeks_user, user["username"], user["password"], data_user.role[2], user["status"])
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
        roles = [data_user.role[1], data_user.role[2]]
        tampilkan_user(roles, kolom=["No", "Username", "Status"])
        data = data_user.load_data_user(roles)
        print()
        if data:
            print("(Ket: Kosongkan input untuk kembali.)")
            indeks_user = input("Nomor Pengguna: ")
        else:
            input("Kembali ke menu...!")
            return
        
        if indeks_user.strip():
            if not indeks_user.isdigit():
                raise ValueError("Nomor pengguna harus berupa angka...!")
            indeks_user = int(indeks_user) - 1

            if indeks_user < 0 or indeks_user >= len(data):
                raise IndexError("Pengguna tidak ditemukan...!")
            user = data[indeks_user]
            global_indeks_user = data_user.cek_indeks(user["username"])
        else:
            return
        
        if user["status"] == data_user.status[0]:
            if dialog_konfirmasi(f"Yakin ingin memblokir {user["username"]}?"):
                data_user.edit_user(global_indeks_user, user["username"], user["password"], user["role"], data_user.status[1])
                input(f"Berhasil memblokir pengguna...!")
            else:
                input("Batal memblokir pengguna...!")
        elif user["status"] == data_user.status[1]:
            if dialog_konfirmasi(f"Yakin ingin membuka blokir {user["username"]}?"):
                data_user.edit_user(global_indeks_user, user["username"], user["password"], user["role"], data_user.status[0])
                input(f"Berhasil membuka blokir pengguna...!")
            else:
                input("Batal membuka blokir pengguna...!")
    except Exception as e:
        print()
        input(e)
        form_edit_blokir()

def form_tambah_diskusi(indeks_tanaman):
    try:
        clear_screen()
        judul_halaman("Tambah Diskusi")
        list_tanaman = data_tanaman.load_data_tanaman()
        list_diskusi = data_diskusi.load_data_diskusi()
        tanaman = list_tanaman[indeks_tanaman]

        print(f"Tanaman: {tanaman["nama"]}")
        print()
        print("(Ket: Kosongkan input untuk kembali.)")
        print()
        judul = input_string("Judul (Maks 40 Huruf)\t: ")
        
        if not judul:
            return
        elif len(judul) > 40:
            raise ValueError("Judul diskusi maksimal 40 karakter...!")
        elif any(diskusi["judul"].lower() == judul.lower() and diskusi["tanaman"] == tanaman["nama"] for diskusi in list_diskusi):
            raise ValueError("Judul diskusi sudah ada, silakan melihat diskusi yang sudah ada...")
        
        konten = input_string("Konten\t\t\t: ")
        if not konten:
            return
        
        tambah_diskusi = data_diskusi.tambah_diskusi(judul, tanaman["nama"], username, konten)
        separator()
        input(tambah_diskusi.get("message"))
    except Exception as e:
        print()
        input(e)
        form_tambah_diskusi(indeks_tanaman)
        

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

data_page_tanaman = 1
filter_tanaman = {}
def manajemen_tanaman():
    global halaman, pilihan_menu, data_page_tanaman, filter_tanaman
    data = data_tanaman.load_data_tanaman(filter_tanaman.get("jenis", []), filter_tanaman.get("min_suhu", ""), filter_tanaman.get("max_suhu", ""), filter_tanaman.get("media", []))
    data_per_page = 5
    total_halaman = int((len(data) - 1) / data_per_page) + 1
    nomor_indeks_tersedia = {}

    judul_halaman("Manajemen Tanaman")

    # Menu Manajemen Tanaman Admin/Moderator
    if data_user.cek_admin(username) or data_user.cek_moderator(username):
        print("A > Tambah Tanaman")
        print("U > Edit Tanaman")
        print("D > Hapus Tanaman")
        print("F > Filter")
        print()
        for i, item in enumerate(data):
            if i >= (data_page_tanaman - 1) * 5 and i < data_page_tanaman * 5:
                print(f"{i + 1} > {item["nama"]} ({item["jenis"]})")
                nomor_indeks_tersedia[str(i + 1)] = data_tanaman.cek_index(item["nama"])

        if total_halaman > 1:
            print()
            print(f"({data_page_tanaman} dari {total_halaman} halaman)")
        if data_page_tanaman > 1:
            print("Q > Halaman Sebelumnya", end=" ")
        if data_page_tanaman > 1 and data_page_tanaman < total_halaman:
            print("|", end=" ")
        if data_page_tanaman < total_halaman:
            print("E > Halaman Selanjutnya", end=" ")
        print()
        print("B > Kembali")
        print("S > Pengaturan")
        separator()

        pilihan_menu = input("Pilih Menu >> ").lower()
        if pilihan_menu == "a":
            form_tambah_tanaman()
        elif pilihan_menu == "u":
            form_edit_tanaman()
        elif pilihan_menu == "d":
            form_hapus_tanaman()
        elif pilihan_menu == "f":
            menu_filter_tanaman()
        elif any(pilihan_menu == str(nomor) for nomor in nomor_indeks_tersedia):
            halaman = f"detail_tanaman?{nomor_indeks_tersedia[pilihan_menu]}"
        elif pilihan_menu == "q" and data_page_tanaman > 1:
            data_page_tanaman -= 1
            clear_screen()
            manajemen_tanaman()
        elif pilihan_menu == "e" and data_page_tanaman < total_halaman:
            data_page_tanaman += 1
            clear_screen()
            manajemen_tanaman()
        elif pilihan_menu == "b":
            kembali()
        elif pilihan_menu == "s":
            halaman = "pengaturan"
        elif pilihan_menu != "n":
            print()
            input("Pilihan tidak valid, silakan coba lagi...")
            clear_screen()
            manajemen_tanaman()

    # Menu Manajemen Tanaman User
    else:
        print("F > Filter")
        print()
        for i, item in enumerate(data):
            if i >= (data_page_tanaman - 1) * 5 and i < data_page_tanaman * 5:
                print(f"{i + 1} > {item["nama"]} ({item["jenis"]})")
                nomor_indeks_tersedia[str(i + 1)] = data_tanaman.cek_index(item["nama"])

        print()
        print(f"({data_page_tanaman} dari {total_halaman} halaman)")
        if data_page_tanaman > 1:
            print("Q > Halaman Sebelumnya", end=" ")
        if data_page_tanaman > 1 and data_page_tanaman < total_halaman:
            print("|", end=" ")
        if data_page_tanaman < total_halaman:
            print("E > Halaman Selanjutnya", end=" ")
        
        print()
        print("B > Kembali")
        print("S > Pengaturan")
        separator()

        pilihan_menu = input("Pilih Menu >> ").lower()
        clear_screen()
        if pilihan_menu == "f":
            menu_filter_tanaman()
        elif any(pilihan_menu == str(nomor) for nomor in nomor_indeks_tersedia):
            halaman = f"detail_tanaman?{nomor_indeks_tersedia[pilihan_menu]}"
        elif pilihan_menu == "q" and data_page_tanaman > 1:
            data_page_tanaman -= 1
            manajemen_tanaman()
        elif pilihan_menu == "e" and data_page_tanaman < total_halaman:
            data_page_tanaman += 1
            manajemen_tanaman()
        elif pilihan_menu == "b":
            kembali()
        elif pilihan_menu == "s":
            halaman = "pengaturan"
        elif pilihan_menu != "n":
            print()
            input("Pilihan tidak valid, silakan coba lagi...")

def menu_filter_tanaman():
    global halaman, pilihan_menu, filter_tanaman
    green_text = "\033[92m"
    white_text = "\033[0m"
    
    clear_screen()
    judul_halaman("Filter Tanaman")
    teks_jenis_aktif = ('(' + ', '.join(filter_tanaman.get('jenis', [])) + ')') if filter_tanaman.get('jenis', []) else ''
    suhu_aktif = ""
    if filter_tanaman.get('min_suhu', ''):
        if filter_tanaman.get('max_suhu', ''):
            suhu_aktif = f"(Min Suhu: {filter_tanaman.get('min_suhu')}, Maks Suhu: {filter_tanaman.get('max_suhu')})"
        else:
            suhu_aktif = f"(Min Suhu: {filter_tanaman.get('min_suhu')})"
    elif filter_tanaman.get('max_suhu', ''):
        suhu_aktif = f"(Maks Suhu: {filter_tanaman.get('max_suhu')})"
    media_aktif = ('(' + ', '.join(filter_tanaman.get('media_tanam', [])) + ')') if filter_tanaman.get('media_tanam', []) else ''
    print("1 > Jenis Tanaman", teks_jenis_aktif)
    print("2 > Suhu", suhu_aktif)
    print("3 > Media Tanam", media_aktif)
    print()
    print("C > Clear Filter")
    print("B > Kembali") 

    pilihan_menu = input("Pilih Menu >> ").lower()
    if pilihan_menu == "1":
        while True:
            clear_screen()
            judul_halaman("Filter Jenis Tanaman")
            for i, item in enumerate(data_tanaman.jenis, start=1):
                print(f"{i} > {green_text if item in filter_tanaman.get('jenis', []) else ""}{item}{white_text}")
            print()
            print("(Ket: Kosongkan input untuk kembali.)")
            pilihan_menu = input_pilihan("Pilih Jenis Tanaman: ", range(1, len(data_tanaman.jenis) + 1))
            if not pilihan_menu:
                break

            filter_tanaman["jenis"] = [] if "jenis" not in filter_tanaman else filter_tanaman["jenis"]
            if data_tanaman.jenis[pilihan_menu - 1] in filter_tanaman["jenis"]:
                filter_tanaman["jenis"].remove(data_tanaman.jenis[pilihan_menu - 1])
            else:
                filter_tanaman["jenis"].append(data_tanaman.jenis[pilihan_menu - 1])
        menu_filter_tanaman()
    elif pilihan_menu == "2":
        while True:
            clear_screen()
            judul_halaman("Filter Suhu")
            min_suhu = input_fixed("Suhu Minimum (°C)\t: ")
            if not min_suhu.isdigit() and min_suhu != "":
                print()
                input("Input harus angka...!")
                continue
            if min_suhu.isdigit():
                min_suhu = float(min_suhu)
            
            while True:
                max_suhu = input_fixed("Suhu Maksimum (°C)\t: ")
                if not max_suhu.isdigit() and max_suhu != "":
                    print()
                    input("Input harus angka...!")
                    continue
                if max_suhu.isdigit():
                    max_suhu = float(max_suhu)

                if max_suhu < min_suhu if min_suhu != "" and max_suhu != "" else False:
                    print()
                    input("Suhu maksimum harus lebih besar dari suhu minimum...!")
                    continue
                break
            filter_tanaman["min_suhu"] = min_suhu
            filter_tanaman["max_suhu"] = max_suhu
            break
        menu_filter_tanaman()
    elif pilihan_menu == "3":
        while True:
            clear_screen()
            judul_halaman("Filter Media Tanam")
            for i, item in enumerate(data_tanaman.media_tanam, start=1):
                print(f"{i} > {green_text if item in filter_tanaman.get('media_tanam', []) else ""}{item}{white_text}")
            print()
            print("(Ket: Kosongkan input untuk kembali.)")
            pilihan_menu = input_pilihan("Pilih Media Tanam: ", range(1, len(data_tanaman.media_tanam) + 1))
            if not pilihan_menu:
                break

            filter_tanaman["media_tanam"] = [] if "media_tanam" not in filter_tanaman else filter_tanaman["media_tanam"]
            if data_tanaman.media_tanam[pilihan_menu - 1] in filter_tanaman["media_tanam"]:
                filter_tanaman["media_tanam"].remove(data_tanaman.media_tanam[pilihan_menu - 1])
            else:
                filter_tanaman["media_tanam"].append(data_tanaman.media_tanam[pilihan_menu - 1])
        menu_filter_tanaman()
    elif pilihan_menu == "c":
        filter_tanaman = {}
        menu_filter_tanaman()
    elif pilihan_menu == "b":
        return
    else:
        print()
        input("Pilihan tidak valid, silakan coba lagi...")
        menu_filter_tanaman()

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
        tampilkan_user()
        print()
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
        form_edit_username()
    elif pilihan_menu == "2":
        clear_screen()
        form_edit_password()
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

def detail_tanaman(indeks_tanaman):
    global halaman, pilihan_menu
    data = data_tanaman.load_data_tanaman()
    tanaman = data[indeks_tanaman]
    data_row = []

    clear_screen()
    judul_halaman(f"Detail Tanaman")
    print("Informasi:")
    data_row.append(["Nama Tanaman", tanaman["nama"]])
    data_row.append(["Jenis Tanaman", tanaman["jenis"]])
    data_row.append(["Jadwal Siram", tanaman["jadwal_siram"]])
    data_row.append(["Suhu", f"{tanaman["min_suhu"]}{"—" + str(tanaman["max_suhu"]) if tanaman["max_suhu"] > tanaman["min_suhu"] else ""} °C"])
    data_row.append(["Pemupukan", tanaman["pemupukan"]])
    data_row.append(["Media Tanam", tanaman["media_tanam"]])
    
    print(tabel(data_row, headers=""))
    print()
    print("1 > Pertanyaan dan Diskusi")
    print()
    print("B > Kembali")
    print("S > Pengaturan")
    separator()
    pilihan_menu = input("Pilih Menu >> ").lower()
    if pilihan_menu == "1":
        halaman = f"diskusi?{indeks_tanaman}"
    elif pilihan_menu == "b":
        kembali()
    elif pilihan_menu == "s":
        halaman = "pengaturan"
    else:
        input("Pilihan tidak valid, silakan coba lagi...")

def menu_diskusi(indeks_tanaman):
    global halaman, pilihan_menu
    list_tanaman = data_tanaman.load_data_tanaman()
    tanaman = list_tanaman[indeks_tanaman]
    list_diskusi = data_diskusi.load_data_diskusi([tanaman["nama"]])
    nomor_diskusi_tersedia = {}

    clear_screen()
    judul_halaman("Pertanyaan dan Diskusi")
    print(f"Diskusi Tanaman: {tanaman["nama"]}")
    print("A > Tambah Diskusi")
    print()
    if list_diskusi:
        for i, item in enumerate(reversed(list_diskusi)):
            jarak_spasi = " "*len(f"{i + 1} > ")
            print(f"{i + 1} > {item["judul"]}")
            print(f"{jarak_spasi}{item["penulis"]}: {item["konten"]}")
            nomor_diskusi_tersedia[str(i + 1)] = data_diskusi.cek_indeks_diskusi(item["judul"], item["tanaman"])
    else:
        print("Tidak ada diskusi yang tersedia.")
    print()
    print("B > Kembali")
    print("S > Pengaturan")
    separator()
    pilihan_menu = input("Pilih Menu >> ").lower()
    if pilihan_menu == "a":
        form_tambah_diskusi(indeks_tanaman)
    elif any(pilihan_menu == str(nomor) for nomor in nomor_diskusi_tersedia):
        halaman = f"konten_diskusi?{nomor_diskusi_tersedia[pilihan_menu]}"
    elif pilihan_menu == "b":
        kembali()
    elif pilihan_menu == "s":
        halaman = "pengaturan"
    else:
        input("Pilihan tidak valid, silakan coba lagi...")

def konten_diskusi(indeks_diskusi):
    global halaman, pilihan_menu
    list_diskusi = data_diskusi.load_data_diskusi()
    diskusi = list_diskusi[indeks_diskusi]

    clear_screen()
    judul_halaman("Pertanyaan dan Diskusi")
    print(f"Diskusi: {diskusi["judul"]} ({diskusi["tanaman"]})")
    print(f"Penulis: {diskusi["penulis"]}")
    print(f"{diskusi["tanggal"]}")
    print()
    print("Pertanyaan:")
    print(diskusi["konten"])
    print()
    print("Respons:")
    if diskusi.get("jawaban"):
        for jawaban in diskusi["jawaban"]:
            print(f"> {jawaban["penulis"]}: {jawaban["konten"]}")
    else:
        print("Belum ada jawaban...")
    print()
    if data_user.cek_admin(username) or data_user.cek_moderator(username):
        print("A > Jawab")
    if data_user.cek_admin(username) or data_user.cek_moderator(username) or username == diskusi["penulis"]:
        print("D > Hapus Diskusi Ini")
    print("B > Kembali")
    print("S > Pengaturan")
    separator()
    pilihan_menu = input("Pilih Menu >> ").lower()
    if pilihan_menu == "a" and (data_user.cek_admin(username) or data_user.cek_moderator(username)):
        print()
        jawab = input_string("Jawaban     : ")
        if not jawab:
            return
        data_diskusi.tambah_jawaban(indeks_diskusi, username, jawab)
    elif pilihan_menu == "d" and (data_user.cek_admin(username) or data_user.cek_moderator(username) or username == diskusi["penulis"]):
        if dialog_konfirmasi("Yakin ingin menghapus diskusi ini?"):
            data_diskusi.hapus_diskusi(indeks_diskusi)
            input("Berhasil menghapus diskusi...!")
            kembali()
        else:
            input("Batal menghapus diskusi...!")
    elif pilihan_menu == "b":
        kembali()
    elif pilihan_menu == "s":
        halaman = "pengaturan"
    else:
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
            form_login()
        elif pilihan_menu != "n":
            print()
            input("Pilihan tidak valid, silakan coba lagi...")
    except Exception or KeyboardInterrupt as e:
        return

def menu_admin():
    global halaman, data_page_tanaman
    try:
        while cek_login():
            setup_halaman()
            parameter_halaman = halaman.split("?")

            if halaman == "menu_utama":
                menu_utama()
            elif halaman == "manajemen_tanaman":
                data_page_tanaman = 1
                manajemen_tanaman()
            elif halaman == "manajemen_user":
                manajemen_user()
            elif halaman == "pengaturan":
                menu_pengaturan()
            elif parameter_halaman[0] == "detail_tanaman":
                indeks_tanaman = int(parameter_halaman[1])
                detail_tanaman(indeks_tanaman)
            elif parameter_halaman[0] == "diskusi":
                indeks_tanaman = int(parameter_halaman[1])
                menu_diskusi(indeks_tanaman)
            elif parameter_halaman[0] == "konten_diskusi":
                indeks_diskusi = int(parameter_halaman[1])
                konten_diskusi(indeks_diskusi)
    except Exception or KeyboardInterrupt as e:
        input(e)
        menu_admin()

def menu_moderator():
    global halaman, data_page_tanaman
    try:
        while cek_login():
            setup_halaman()
            parameter_halaman = halaman.split("?")

            if halaman == "menu_utama":
                menu_utama()
            elif halaman == "manajemen_tanaman":
                data_page_tanaman = 1
                manajemen_tanaman()
            elif halaman == "pengaturan":
                menu_pengaturan()
            elif parameter_halaman[0] == "detail_tanaman":
                indeks_tanaman = int(parameter_halaman[1])
                detail_tanaman(indeks_tanaman)
            elif parameter_halaman[0] == "diskusi":
                indeks_tanaman = int(parameter_halaman[1])
                menu_diskusi(indeks_tanaman)
            elif parameter_halaman[0] == "konten_diskusi":
                indeks_diskusi = int(parameter_halaman[1])
                konten_diskusi(indeks_diskusi)
    except Exception or KeyboardInterrupt as e:
        input(e)
        menu_moderator()

def menu_user():
    global halaman, data_page_tanaman
    try:
        while cek_login():
            setup_halaman()
            parameter_halaman = halaman.split("?")

            if halaman == "menu_utama":
                menu_utama()
            elif halaman == "manajemen_tanaman":
                data_page_tanaman = 1
                manajemen_tanaman()
            elif halaman == "pengaturan":
                menu_pengaturan()
            elif parameter_halaman[0] == "detail_tanaman":
                indeks_tanaman = int(parameter_halaman[1])
                detail_tanaman(indeks_tanaman)
            elif parameter_halaman[0] == "diskusi":
                indeks_tanaman = int(parameter_halaman[1])
                menu_diskusi(indeks_tanaman)
            elif parameter_halaman[0] == "konten_diskusi":
                indeks_diskusi = int(parameter_halaman[1])
                konten_diskusi(indeks_diskusi)
    except Exception or KeyboardInterrupt as e:
        input(e)
        menu_user()