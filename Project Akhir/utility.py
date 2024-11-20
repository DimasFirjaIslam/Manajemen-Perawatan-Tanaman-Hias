import os
import tabulate as tb

# Fungsi untuk membersihkan layar terminal
def clear_screen():
    os.system("cls || clear")

# Fungsi untuk merapikan input, seperti menghilangkan spasi di awal dan akhir input
def input_fixed(prompt):
    try:
        value = input(prompt).strip()
        return value
    except ValueError as e:
        input(e)
        return input_fixed(prompt)

# Fungsi untuk membuat input yang hanya menerima teks (tidak menerima angka saja)
def input_string(prompt):
    try:
        value_string = input_fixed(prompt).strip()
        if value_string:
            if value_string.isdigit():
                raise ValueError("Input tidak boleh angka!")
            return value_string
        return ""
    except ValueError as e:
        input(e)
        return input_string(prompt)
    
# Fungsi untuk membuat input yang meminta rentang pilihan    
def input_pilihan(prompt, pilihan):
    try:
        value_pilihan = input_fixed(prompt).strip()
        if value_pilihan:
            if value_pilihan.isdigit():
                if int(value_pilihan) in pilihan:
                    return int(value_pilihan)
                else:
                    raise ValueError("Pilihan tidak ada!")
            else:
                raise ValueError("Input harus angka!")
        return 0
    except ValueError as e:
        input(e)
        return input_pilihan(prompt, pilihan)
    
# Fungsi untuk membuat judul halaman
def judul_halaman(nama_halaman):
    nama_halaman = f" {nama_halaman} "
    print(nama_halaman.center(45, "="))

# Fungsi untuk membuat garis pemisah
def separator():
    print("─"*45)

# Fungsi untuk membuat input konfirmasi sebuah aksi
def dialog_konfirmasi(pesan):
    while True:
        konfirmasi = input(f"{pesan} (y/n) ").lower()
        if konfirmasi == "y":
            return True
        elif konfirmasi == "n":
            return False
        else:
            input("Input tidak valid, silakan coba lagi...")

# Fungsi untuk menampilkan data dalam bentuk tabel tabulate
def tabel(data, headers="keys"):
    try:
        if data:
            return tb.tabulate(data, headers, tablefmt="fancy_grid", stralign="left", numalign="right")
    except Exception as e:
        return str(e)
    
# Fungsi untuk mengecek apakah value merupakan angka
def checkNumString(value):
    if value:
        # Jika tipe data value sudah integer atau float, maka True
        if type(value) == int or type(value) == float:
            return True
        # Jika tipe data value adalah string dan value dicek apakah merupakan angka, maka True
        if value.lstrip("-").isdigit() if type(value) == str else False:
            return True
    return False