import sys
import getpass
import pyperclip
import keyboard
from pykeepass import PyKeePass
import threading
import ctypes
from Cryptodome.Cipher import AES, ChaCha20, Salsa20

def read_kdbx(file_path, password):
    try:
        kp = PyKeePass(file_path, password=password)
        return kp.entries
    except Exception as e:
        print(f'Ocurrió un error: {e}')
        return []

def copy_password_to_clipboard(entries, title):
    for entry in entries:
        if entry.title == title:
            pyperclip.copy(entry.password)
            print(f'Contraseña para "{title}" copiada al portapapeles.')
            return

def listen_for_keypress(entries):
    is_copying = False
    while True:
        if keyboard.is_pressed('ctrl+shift+1') and not is_copying:
            copy_password_to_clipboard(entries, 'tittle1')
            is_copying = True
        elif keyboard.is_pressed('ctrl+shift+2') and not is_copying:
            copy_password_to_clipboard(entries, 'tittle2')
            is_copying = True
        elif keyboard.is_pressed('ctrl+alt+3') and not is_copying:
            copy_password_to_clipboard(entries, 'tittle3')
            is_copying = True
        else:
            is_copying = False

def hide_console():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

if __name__ == '__main__':
    file_path = "PATH/TO/DATABASE.kdbx"
    
    password = getpass.getpass('Introduce la contraseña de la base de datos: ')
    entries = read_kdbx(file_path, password)

    if entries:
        hide_console()
        listener_thread = threading.Thread(target=listen_for_keypress, args=(entries,), daemon=True)
        listener_thread.start()
        listener_thread.join()
    else:
        print("Contraseña incorrecta.")
        sys.exit(1)
