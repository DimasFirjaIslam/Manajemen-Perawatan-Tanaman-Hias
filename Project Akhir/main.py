import menu

# Memulai program yang hanya dapat dijalankan dari file ini
if __name__ == "__main__":
    while menu.pilihan_menu != "n":
        clear_screen()
        menu.menu_awal()
    print()
input("Menutup program...")