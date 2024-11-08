import json
import os

def clear_screen():
    os.system("cls || clear")

def input_string(prompt):
    try:
        value_string = input(prompt)
        if value_string:
            if not value_string.strip():
                raise ValueError("Input tidak boleh kosong!")
            elif value_string.isdigit():
                raise ValueError("Input tidak boleh angka!")
        return value_string
    except ValueError as e:
        input(e)
        return input_string(prompt)
    
def judul_halaman(nama_halaman):
    nama_halaman = f" {nama_halaman} "
    print(nama_halaman.center(30, "="))

# def judul_halaman(nama_halaman):
#     print(f"{"─"*10} {nama_halaman} {"─"*10}")

def separator():
    print("─"*30)