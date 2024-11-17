import pathlib
import json

# Mengambil lokasi folder pada penyimpanan lokal
data_path = pathlib.Path(__file__).parent.absolute()

# Fungsi untuk memuat/mengambil/membaca data dari file JSON
def load_data(nama_file):
    try:
        with open(f"{data_path}/{nama_file}", "r") as file:
            return json.load(file)
    except Exception:
        return []

# Fungsi untuk menyimpan data ke dalam file JSON
def simpan_data(data_baru, nama_file):
    try:
        with open(f"{data_path}/{nama_file}", "w") as nama_file:
            json.dump(data_baru, nama_file, indent=4)
            return True
    except Exception:
        return False