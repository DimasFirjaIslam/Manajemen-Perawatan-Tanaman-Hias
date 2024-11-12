from data.data_utility import *

level = ("admin", "moderator", "user")
status = ("aktif", "diblokir")

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
    result = {
        "data": None,
        "status": False,
        "message": ""
    }
    users = load_data_user()
    
    for user in users:
        if user['username'] == username and user['password'] == password:
            if user['status'] == status[1]:
                result["message"] = "Akun diblokir, silakan hubungi admin...!"
                break
            result["data"] = user
            result["status"] = True
            result["message"] = "Login berhasil...!"
            break
        else:
            result["message"] = "Username atau password salah...!"
    return result

def registrasi(username, password):
    result = {
        "status": False,
        "message": ""
    }

    users = load_data_user()
    users.append({
        "username" : username,
        "password" : password,
        "role" : level[2],
        "status" : status[0]
    })
    
    result["status"] = simpan_data_user(users)
    result["message"] = "Registrasi berhasil...!"
    return result

def edit_user(indeks_user, username, password, role, status):
    try:
        result = {
            "status": False,
            "message": ""
        }
        data = load_data_user()

        if str(indeks_user).strip() == "":
            raise ValueError("Nomor pengguna tidak boleh kosong...!")
        elif not str(indeks_user).isdigit():
            raise ValueError("Nomor pengguna harus berupa angka...!")
        elif role.lower() not in level:
            raise ValueError("Role pengguna tidak valid...!")
        elif role.lower() == level[0]:
            raise ValueError("Role Admin tidak dapat diubah...!")
        elif indeks_user < 0 or indeks_user >= len(data):
            raise IndexError("Pengguna tidak ditemukan...")
        
        user = data[indeks_user]
        user["username"] = username
        user["password"] = password
        user["role"] = role
        user["status"] = status

        result["status"] = simpan_data_user(data)
        result["message"] = "Data berhasil diubah...!"
    except IndexError or ValueError as e:
        result["message"] = str(e)
    finally:
        return result

def hapus_user(indeks_user: int):
    try:
        result = {
            "status": False,
            "message": ""
        }
        data = load_data_user()

        if str(indeks_user).strip() == "":
            raise ValueError("Nomor pengguna tidak boleh kosong...!")
        elif not str(indeks_user).isdigit():
            raise ValueError("Nomor pengguna harus berupa angka...!")
        elif indeks_user < 0 or indeks_user >= len(data):
            raise IndexError("Pengguna tidak ditemukan...")

        data.pop(indeks_user)
        result["status"] = simpan_data_user(data)
        result["message"] = "Data berhasil dihapus...!"
    except IndexError or ValueError as e:
        result["message"] = str(e)
    finally:
        return result 

# def edit_username(username, username_baru):
#     data = load_data_user()
#     for user in data:
#         if user['username'] == username:
#             user['username'] = username_baru
#             simpan_data_user(data)
#             return True
#     return False

# def edit_password(username, password_baru):
#     result = {
#         "status": False,
#         "message": ""
#     }
#     data = load_data_user()
#     for user in data:
#         if user['username'] == username:
#             user['password'] = password_baru
#             simpan_data_user(data)
#             result["status"] = True
#             result["message"] = "Password berhasil diubah...!"
#             break
#         else:
#             result["message"] = "Pengguna tidak ditemukan...!"
#     return result

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

def indeks_user(username):
    data = load_data_user()
    for i, user in enumerate(data):
        if user['username'] == username:
            return i
    return False