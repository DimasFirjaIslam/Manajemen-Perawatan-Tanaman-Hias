import json

def load_data():
    with open("Project Akhir\data\data_tanaman.json", "r") as file_json:
        return json.load(file_json)

def simpan_data(databaru):
    with open("Project Akhir\data\data_tanaman.json", "w") as file_json:
        json.dump(databaru, file_json, indent=4)