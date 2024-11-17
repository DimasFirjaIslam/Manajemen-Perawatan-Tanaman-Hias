from data.data_utility import *
import data.data_diskusi as data_diskusi

# Mendeklarasikan role dan status yang tersedia untuk akun pengguna
role = ("admin", "moderator", "user")
status = ("aktif", "diblokir")

# Fungsi untuk mengambil data_user dari file JSON dengan nama file "data_user.json"
def load_data_user(roles = [], status = []):
    data = load_data("data_user.json")
    data_terfilter = []
    for user in data:
        if user["role"] in roles if roles else True:
            data_terfilter.append(user)
        if user["status"] not in status if status else False:
            data_terfilter.remove(user)
        
    return data_terfilter

# Fungsi untuk menyimpan data pengguna ke dalam file JSON dengan nama file "data_user.json"
def simpan_data_user(databaru):
    return simpan_data(databaru, "data_user.json")

# Fungsi untuk melakukan login/autentikasi pengguna
def login(username, password):
    result = {
        "data": None,
        "status": False,
        "message": ""
    }
    users = load_data_user()
    
    # Membuat perulangan pada setiap akun yang tersedia
    for user in users:
        # Membandingkan setiap akun dengan inputan username dan password
        if user["username"] == username and user["password"] == password:
            # Walaupun berhasil memasukkan data login, tetapi status akun diblokir, maka login gagal
            if user["status"] == status[1]:
                result["message"] = "Akun diblokir, silakan hubungi admin...!"
                break
            result["data"] = user
            result["status"] = True
            result["message"] = "Login berhasil...!"
            break
        else:
            result["message"] = "Username atau password salah...!"
    return result

# Fungsi untuk melakukan registrasi pengguna
def registrasi(username, password):
    result = {
        "status": False,
        "message": ""
    }
    # Menduplikasi data pengguna dari database
    users = load_data_user()
    
    # Menambahkan data baru pada duplikasi 
    users.append({
        "username" : username,
        "password" : password,
        "role" : role[2],
        "status" : status[0]
    })
    
    # Menimpa data pengguna yang lama dengan duplikasi yang baru
    result["status"] = simpan_data_user(users)
    result["message"] = "Registrasi berhasil...!"
    return result

# Fungsi untuk mengubah data pengguna yang sudah terdaftar
def edit_user(indeks_user, username_baru, password_baru, role_baru, status_baru):
    try:
        result = {
            "status": False,
            "message": ""
        }
        # Menduplikasi data tanaman dari database dan mengambil data tanaman dengan indeks spesifik
        data = load_data_user()
        user = data[indeks_user]

        # Beberapa syarat yang harus dipenuhi untuk mengubah data pengguna
        if str(indeks_user).strip() == "":
            raise ValueError("Nomor pengguna tidak boleh kosong...!")
        elif role_baru.lower() not in role:
            raise ValueError("Role pengguna tidak valid...!")
        elif (user["role"].lower() == role[1] or user["role"].lower() == role[2]) and role_baru.lower() == role[0]:
            raise ValueError("Tidak dapat mengubah pengguna menjadi admin...!")
        elif user["role"].lower() == role[0] and (role_baru.lower() == role[1] or role_baru.lower() == role[2]):
            raise ValueError("Tidak dapat mengubah admin menjadi moderator atau user...!")
        elif indeks_user < 0 or indeks_user >= len(data):
            raise IndexError("Pengguna tidak ditemukan...")
        
        # Memperbarui data yang menyangkut dengan pengguna yang diedit
        list_diskusi = data_diskusi.load_data_diskusi()
        for diskusi in list_diskusi:
            if diskusi["penulis"] == user["username"]:
                diskusi["penulis"] = username_baru
            for jawaban in diskusi["jawaban"]:
                if jawaban["penulis"] == user["username"]:
                    jawaban["penulis"] = username_baru
        data_diskusi.simpan_data_diskusi(list_diskusi)
        
        # Memperbarui data pengguna dengan data baru
        user["username"] = username_baru
        user["password"] = password_baru
        user["role"] = role_baru
        user["status"] = status_baru

        # Menimpa data pengguna yang lama dengan duplikasi yang telah diubah
        result["status"] = simpan_data_user(data)
        result["message"] = "Data berhasil diubah...!"
    except Exception as e:
        result["message"] = str(e)
    finally:
        return result

# Fungsi untuk menghapus data pengguna yang sudah terdaftar
def hapus_user(indeks_user: int):
    try:
        result = {
            "status": False,
            "message": ""
        }
        # Menduplikasi data pengguna dari database
        data = load_data_user()

        # Beberapa syarat yang harus dipenuhi untuk menghapus data pengguna
        if str(indeks_user).strip() == "":
            raise ValueError("Nomor pengguna tidak boleh kosong...!")
        elif not str(indeks_user).isdigit():
            raise ValueError("Nomor pengguna harus berupa angka...!")
        elif indeks_user < 0 or indeks_user >= len(data):
            raise IndexError("Pengguna tidak ditemukan...")

        # Menghapus duplikasi data pengguna berdasarkan indeks yang dipilih
        data.pop(indeks_user)
        
        # Menimpa data pengguna yang lama dengan duplikasi yang telah dihapus
        result["status"] = simpan_data_user(data)
        result["message"] = "Data berhasil dihapus...!"
    except IndexError or ValueError as e:
        result["message"] = str(e)
    finally:
        return result

# Fungsi untuk mengecek role pengguna berdasarkan usernamenyadd
def cek_role(username):
    data = load_data_user()
    for user in data:
        if user["username"] == username:
            return user["role"]
    return False

# Fungsi untuk mengecek apakah pengguna dengan username terkait adalah admin
def cek_admin(username):
    return cek_role(username).lower() == role[0]

# Fungsi untuk mengecek apakah pengguna dengan username terkait adalah moderator
def cek_moderator(username):
    return cek_role(username).lower() == role[1]

# Fungsi untuk mengambil indeks pengguna pada database berdasarkan usernamenya
def cek_indeks(username):
    data = load_data_user()
    for i, user in enumerate(data):
        if user["username"] == username:
            return i
    return False