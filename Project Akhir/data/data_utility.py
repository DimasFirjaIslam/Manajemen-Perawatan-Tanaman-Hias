import json
def load_data(nama_file):
    with open(nama_file, "r") as file:
       return json.load(file)
def simpan_data(data_baru, nama_file):
    with open(nama_file, "w") as file:
        json.dump(data_baru, nama_file, indent=4)
