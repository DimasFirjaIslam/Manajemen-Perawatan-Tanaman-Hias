import os
from utility import *

os.system("cls || clear")

nama_file = "data_user.json"

def load_data_user():
    return load_data(nama_file)
    
def save_data_user(data):
    save_data(nama_file, data)

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
    save_data_user(users)