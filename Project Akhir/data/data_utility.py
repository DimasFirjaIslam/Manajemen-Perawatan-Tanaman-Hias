import pathlib
import json

data_path = pathlib.Path(__file__).parent.absolute()

def load_data(nama_file):
    with open(f"{data_path}/{nama_file}", "r") as file:
       return json.load(file)

def simpan_data(data_baru, nama_file):
    with open(f"{data_path}/{nama_file}", "w") as nama_file:
        json.dump(data_baru, nama_file, indent=4)