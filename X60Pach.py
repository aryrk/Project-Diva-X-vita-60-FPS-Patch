import os
import shutil
import tkinter as tk
from tkinter import filedialog
import subprocess

def dir_getter():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(initialdir=os.getcwd(), title="Select Project Diva X folder")

def decrypt_psarc(dir_path):
    zRIF_string = input("\nPlease enter the zRIF string for the game:\n")
    if not zRIF_string:
        print("Error: zRIF string not valid!")
        return
    
    target_path = os.path.join(dir_path, "patched")
    command = f'lib\\psvpfsparser -i "{dir_path}" -o "{target_path}" -z "{zRIF_string}" -f cma.henkaku.xyz'
    print(command)
    subprocess.run(command, shell=True)

def get_list_required_files(dir_path):
    psarc_path = os.path.join(dir_path, "rom", "data.psarc")
    txt_psarc_path = os.path.join(dir_path, "rom", "data.psarc.txt")
    subprocess.run(f'lib\\PSARC -l "{psarc_path}"', shell=True)
    
    if not os.path.exists(txt_psarc_path):
        decrypt_psarc(dir_path)
        psarc_path = os.path.join(dir_path, "patched", "rom", "data.psarc")
        txt_psarc_path = os.path.join(dir_path, "patched", "rom", "data.psarc.txt")
        subprocess.run(f'lib\\PSARC -l "{psarc_path}"', shell=True)
    
    with open(txt_psarc_path, 'r') as file:
        lines = file.readlines()
        names = [line.split('|')[2].strip() for line in lines[1:]]

    unique_sorted_names = sorted(set(names))
    os.remove(txt_psarc_path)

    return [os.path.splitext(name)[0] for name in unique_sorted_names]

def create_post_process_table(dir_path, list_required_files):
    table_path = os.path.join(dir_path, "rom", "post_process_table")
    if os.path.exists(table_path):
        shutil.rmtree(table_path, ignore_errors=True)
    os.makedirs(table_path)
    
    for i, filename in enumerate(list_required_files, start=1):
        with open(os.path.join(table_path, f"{filename}.dft"), 'w'):
            pass
        print(f"Created: {filename[:50]:<50} ({i}/{len(list_required_files)})", end='\r')

def eboot_patch(dir_path):
    eboot_path = os.path.join(dir_path, "eboot.bin")
    if not os.path.exists(os.path.join(dir_path, "eboot.bin.bak")):
        shutil.copyfile(eboot_path, os.path.join(dir_path, "eboot.bin.bak"))
    os.remove(eboot_path)
    shutil.copyfile("lib\\eboot.bin", eboot_path)

def header():
    print("-" * 92)
    print("  _____           _           _     _____  _             __   __                 _ _        ")
    print(" |  __ \         (_)         | |   |  __ \(_)            \ \ / /                (_) |       ")
    print(" | |__) | __ ___  _  ___  ___| |_  | |  | |___   ____ _   \ V /   ______  __   ___| |_ __ _ ")
    print(" |  ___/ '__/ _ \| |/ _ \/ __| __| | |  | | \ \ / / _` |   > <   |______| \ \ / / | __/ _` |")
    print(" | |   | | | (_) | |  __/ (__| |_  | |__| | |\ V / (_| |  / . \            \ V /| | || (_| |")
    print(" |_|   |_|  \___/| |\___|\___|\__| |_____/|_| \_/ \__,_| /_/ \_\            \_/ |_|\__\__,_|")
    print("                _/ |                                                                        ")
    print("               |__/                                                                         ")
    print("\nProject Diva X PSVita 60fps patcher")
    print("-" * 92)

def main():
    header()
    
    print("\nPlease select Project Diva X folder.\n(where eboot.bin located)")
    dir_path = dir_getter()
    print(f"\nFolder used: {dir_path}")

    if not (os.path.isfile(os.path.join(dir_path, "rom", "data.psarc")) and os.path.isfile(os.path.join(dir_path, "eboot.bin"))):
        print("Error: directory not valid!")
        return
    else:
        print("VALID!")
        
    print("-" * 10)

    list_required_files = get_list_required_files(dir_path)
    
    print("-" * 10)
    print("\nCreating post process table...")
    create_post_process_table(dir_path, list_required_files)
    print("\nPost process table created!")
    
    print("-" * 10)
    print("\nPatching eboot.bin...")
    eboot_patch(dir_path)
    print("eboot.bin patched!")
    
    if os.path.exists(os.path.join(dir_path, "patched")):
        shutil.rmtree(os.path.join(dir_path, "patched"), ignore_errors=True)
    
if __name__ == "__main__":
    main()
    input("\nPress enter to exit...")
