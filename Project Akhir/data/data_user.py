from data.data_utility import *

def load_data_user():
    return load_data("data_user.json")

def simpan_data_user(databaru):
    simpan_data(databaru, "data_user.json")

def login(username, password):
    users = load_data_user()
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user
    return False

def register(username, password):
    users = load_data_user()
    users.append({
        "username" : username,
        "password" : password,
        "role" : "user"
    })
    simpan_data_user(users)
    
def tambah_user():
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")
    role = input("Masukkan role: ")

    databaru = {
        "username": username,
        "password": password,
        "role": role
    }

    data = load_data_user()
    data.append(databaru)
    simpan_data_user(data)
    print("Data berhasil ditambahkan!")

def edit_user():
    data = load_data_user()
    nomor_pengguna = int(input("Masukkan pengguna yang ingin diubah: ")) - 1
    if 0 <= nomor_pengguna < len(data):
        pengguna = data[nomor_pengguna]
        pengguna["username"] = input("Masukkan username: ")
        pengguna["password"] = input("Masukkan password: ")
        pengguna["role"] = input("Masukkan role: ")
        
        simpan_data_user(data)
        print("Data berhasil diubah!")
    else:
        print("Nomor tanaman tidak valid.")

def hapus_user():
    nomor_user = int(input("Masukkan pengguna yang ingin dihapus: ")) - 1
    data = load_data_user()
    if nomor_user < len(data):
        data.pop(nomor_user)
        simpan_data_user(data)
        print("Pengguna berhasil dihapus!")
    else:
        print("Pengguna tidak ditemukan.")