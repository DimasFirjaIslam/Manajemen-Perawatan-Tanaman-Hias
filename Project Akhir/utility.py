import os
import tabulate as tb

def clear_screen():
    os.system("cls || clear")

def input_fixed(prompt):
    try:
        value = input(prompt).strip()
        # if value:
        #     if not value.strip():
        #         raise ValueError("Input tidak boleh kosong!")
        return value
    except ValueError as e:
        input(e)
        return input_fixed(prompt)

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
    
def input_int(prompt):
    try:
        value_int = input_fixed(prompt).strip()
        if value_int:
            return int(value_int)
        return 0
    except ValueError as e:
        input("Input harus angka!")
        return input_int(prompt)
    
def input_float(prompt):
    try:
        value_float = input_fixed(prompt).strip()
        if value_float:
            return float(value_float)
        return 0.0
    except ValueError as e:
        input("Input harus angka!")
        return input_float(prompt)
    
def input_pilihan(prompt, pilihan):
    try:
        value_pilihan = input_fixed(prompt).strip()
        if value_pilihan:
            if value_pilihan.isdigit():
                if int(value_pilihan) in pilihan:
                    return int(value_pilihan)
                else:
                    raise ValueError("Pilihan tidak valid!")
            else:
                raise ValueError("Input harus angka!")
        return 0
    except ValueError as e:
        input(e)
        return input_pilihan(prompt, pilihan)
    
def judul_halaman(nama_halaman):
    nama_halaman = f" {nama_halaman} "
    print(nama_halaman.center(45, "="))

# def judul_halaman(nama_halaman):
#     print(f"{"─"*10} {nama_halaman} {"─"*10}")

def separator():
    print("─"*45)

def dialog_konfirmasi(pesan):
    while True:
        konfirmasi = input(f"{pesan} (y/n) ").lower()
        if konfirmasi == "y":
            return True
        elif konfirmasi == "n":
            return False
        else:
            input("Input tidak valid, silakan coba lagi...")

def tabel(data, headers="keys"):
    try:
        if data:
            return tb.tabulate(data, headers, tablefmt="fancy_grid", stralign="left", numalign="right")
    except Exception as e:
        return str(e)