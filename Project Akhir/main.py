import menu

def logged_in():
    input(username)
    return True if username.strip() else False

def destroy():
    global username
username = ""

if __name__ == "__main__":
    while menu.pilihan_menu != "n":
        menu.menu_awal()