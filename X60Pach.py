# Post Process Table Generator by @aryrk
# PSARC extractor by @Cyan
# eboot.bin patched by ????

import os
import shutil
import tkinter as tk
from tkinter import filedialog

def dir_getter():
    root = tk.Tk()
    root.withdraw()
    dir_path = filedialog.askdirectory(initialdir=os.getcwd(), title="Select Project Diva X folder")
    return dir_path

def get_list_required_files(dir_path):
    psarc_path = dir_path+"/rom/data.psarc"
    txt_psarc_path = dir_path+"/rom/data.psarc.txt"
    os.system("lib\PSARC -l "+'"'+psarc_path+'"')
    
    with open(txt_psarc_path, 'r') as file:
        lines = file.readlines()
        names = [line.split('|')[2].strip() for line in lines[1:]]

    unique_sorted_names = sorted(set(names))
    
    os.remove(txt_psarc_path)

    return [os.path.splitext(name)[0] for name in unique_sorted_names]

def create_post_process_table(dir_path, list_required_files):
    table_path = dir_path+"/rom/post_process_table"
    if os.path.exists(table_path):
        shutil.rmtree(table_path, ignore_errors=True)
    os.makedirs(table_path)
    
    i=0

    for filename in list_required_files:
        with open(table_path + "\\" + filename + ".dft", 'w') as fp:
            pass
        i+=1
        print(f"Created: {filename[:50]:<50} ({i}/{len(list_required_files)})", end='\r')

    return

def eboot_patch(dir_path):
    eboot_path = dir_path+"/eboot.bin"
    if os.path.exists(dir_path+"/eboot.bin.bak"):
        os.remove(dir_path+"/eboot.bin.bak")
    shutil.copyfile("lib\\eboot.bin", eboot_path)
    return
    
def header():
    print("-"*92)
    print("  _____           _           _     _____  _             __   __                 _ _        ")
    print(" |  __ \         (_)         | |   |  __ \(_)            \ \ / /                (_) |       ")
    print(" | |__) | __ ___  _  ___  ___| |_  | |  | |___   ____ _   \ V /   ______  __   ___| |_ __ _ ")
    print(" |  ___/ '__/ _ \| |/ _ \/ __| __| | |  | | \ \ / / _` |   > <   |______| \ \ / / | __/ _` |")
    print(" | |   | | | (_) | |  __/ (__| |_  | |__| | |\ V / (_| |  / . \            \ V /| | || (_| |")
    print(" |_|   |_|  \___/| |\___|\___|\__| |_____/|_| \_/ \__,_| /_/ \_\            \_/ |_|\__\__,_|")
    print("                _/ |                                                                        ")
    print("               |__/                                                                         ")
    print("\nProject Diva X PSVita 60fps patcher")
    print("-"*92)


def main():
    header()
    
    print("\nPlease select Project Diva X folder.\n(where eboot.bin located)")

    dir_path = dir_getter()

    print("\nFolder used: "+dir_path)

    if (not os.path.isfile(dir_path+"/rom/data.psarc")) or (not os.path.isfile(dir_path+"/eboot.bin")):
        print("Error: directory not valid!")
        return
    else:
        print("VALID!")
        
    print("-"*10)

    list_required_files = get_list_required_files(dir_path)
    
    print("-"*10)
    

    print("\nCreating post process table...")
    create_post_process_table(dir_path, list_required_files)
    print("\nPost process table created!")
    
    print("-"*10)

    print("\nPatching eboot.bin...")
    eboot_patch(dir_path)
    print("eboot.bin patched!")
    
main()
input("\nPress enter to exit...")