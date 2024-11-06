from menu import menu_awal, pilihan_menu

username = ""

def logged_in():
    return True if username else False

def destroy():
    global username
    username = ""

if __name__ == "__main__":
    while pilihan_menu != "n":
        input("Halo")
