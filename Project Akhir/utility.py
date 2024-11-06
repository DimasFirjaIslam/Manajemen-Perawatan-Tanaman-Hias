import json
import os

def load_data(nama_file):
    with open(f"Project Akhir\data\{nama_file}") as file:
        return json.load(file)
    
def save_data(nama_file, data_baru):
    with open(f"Project Akhir\data\{nama_file}", "w") as file:
        json.dump(data_baru, file, indent=4)

def clear_screen():
    os.system("cls || clear")