from data_utility import *

def load_data_user():
    return load_data("data_user.json")

def simpan_data_tanaman(databaru):
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
    simpan_data_tanaman(users)
    