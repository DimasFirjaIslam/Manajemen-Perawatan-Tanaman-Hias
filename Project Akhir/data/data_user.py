from data.data_utility import *

level = ("admin", "moderator", "user")

def load_data_user(roles = []):
    data = load_data("data_user.json")
    data_terfilter = data.copy()
    if roles:
        data_terfilter.clear()
        for user in data:
            if user["role"] in roles:
                data_terfilter.append(user)
    return data_terfilter

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
        "role" : level[2]
    })
    simpan_data_user(users)

# Fungsi untuk menambahkan atau menghapus role "Moderator" pada pengguna
def edit_status_moderator():
    try:
        data = load_data_user([level[1], level[2]])
        print("(Ket: Kosongkan input untuk kembali ke menu.)")
        nomor_pengguna = input("Masukkan pengguna yang ingin dipromosikan: ")
        if not nomor_pengguna: return
        nomor_pengguna = int(nomor_pengguna) - 1
        if 0 <= nomor_pengguna < len(data):
            while True:
                # Jika status role pengguna adalah "User", maka akan dipromosikan menjadi "Moderator"
                if data[nomor_pengguna]["role"] == level[2]:
                    konfirmasi = input(f"Tambahkan {data[nomor_pengguna]['username']} sebagai Moderator? (y/n) ").lower()
                    if konfirmasi == "y":
                        edit_user(data[nomor_pengguna]["username"], data[nomor_pengguna]["password"], level[1])
                        input(f"Berhasil menambahkan Moderator...!")
                    elif konfirmasi == "n":
                        input("Batal menambahkan Moderator...!")
                        break
                    else:
                        input("Input tidak valid, silakan coba lagi...")

                # Jika status role pengguna sudah "Moderator", maka akan dikembalikan menjadi role "User"
                elif data[nomor_pengguna]["role"] == level[1]:
                    konfirmasi = input(f"Hapus {data[nomor_pengguna]['username']} dari Moderator? (y/n) ").lower()
                    if konfirmasi == "y":
                        edit_user(data[nomor_pengguna]["username"], data[nomor_pengguna]["password"], level[2])
                        input(f"Berhasil menghapus Moderator...!")
                    elif konfirmasi == "n":
                        input("Batal menghapus Moderator...!")
                        break
                    else:
                        input("Input tidak valid, silakan coba lagi...")
        else:
            input("Pengguna tidak ditemukan...!")
    except ValueError:
        input("Nomor pengguna tidak valid, silakan coba lagi...")

def edit_user(username, password, role = level[2]):
    data = load_data_user()
    for user in data:
        if user['username'] == username:
            user['username'] = username
            user['password'] = password
            user['role'] = role
            simpan_data_user(data)
            return True
    return False

def hapus_user():
    try:
        data = load_data_user()
        print("(Ket: Kosongkan input untuk kembali ke menu.)")
        nomor_user = input("Masukkan pengguna yang ingin dihapus: ")
        if not nomor_user: return
        nomor_user = int(nomor_user) - 1
        if nomor_user < len(data):
            data.pop(nomor_user)
            simpan_data_user(data)
            input("Pengguna berhasil dihapus...!")
        else:
            input("Pengguna tidak ditemukan...!")
    except ValueError:
        input("Nomor pengguna tidak valid, silakan coba lagi...")

def edit_username(username, username_baru):
    data = load_data_user()
    for user in data:
        if user['username'] == username:
            user['username'] = username_baru
            simpan_data_user(data)
            return True
    return False

def edit_password(username, password_baru):
    data = load_data_user()
    for user in data:
        if user['username'] == username:
            user['password'] = password_baru
            simpan_data_user(data)
            return True
    return False

def cek_role(username):
    data = load_data_user()
    for user in data:
        if user['username'] == username:
            return user['role']
    return False

def cek_admin(username):
    return cek_role(username).lower() == level[0]

def cek_moderator(username):
    return cek_role(username).lower() == level[1]