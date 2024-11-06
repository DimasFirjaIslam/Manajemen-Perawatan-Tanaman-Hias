from utility import *

def load_data():
    with open("Project Akhir\data\data_user.json", "r") as file_json:
        return json.load(file_json)

def simpan_data(databaru):
    with open("Project Akhir\data\data_user.json", "w") as file_json:
        json.dump(databaru, file_json, indent=4)

def login(username, password):
    users = load_data()
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user
    return False

def register(username, password):
    users = load_data()
    users.append({
        "username" : username,
        "password" : password,
        "role" : "user"
    })
    simpan_data(users)