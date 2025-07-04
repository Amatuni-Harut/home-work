import os
import argparse
def create_folder(folder_path):
    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
        except:
            print(f"Error creating folder '{folder_path}'")
def move_file(file, folder):
    fname = os.path.basename(file)
    npath = os.path.join(folder, fname)
    try:
        os.rename(file, npath)
        print(f"Moved '{fname}' to '{folder}/'")
    except:
        print(f"Error moving file '{fname}'")

def sort_filees_by_type(folder):
    if not os.path.isdir(folder):
        print("not folder")
        return
    try:
        files = os.listdir(folder)
    except:
        print("Error reading folder.")
        return
    for fname in files:
        Nfile = os.path.join(folder, fname)
        if os.path.isfile(Nfile):
            ml = os.path.splitext(fname)[1][1:].lower()
            if not ml:
                ml = "other"
            target_folder = os.path.join(folder, ml)  
            create_folder(target_folder)
            move_file(Nfile, target_folder)  
def main():
    parser = argparse.ArgumentParser(description="Sort files by extension.")
    parser.add_argument("folder", help="Path to the folder")
    args = parser.parse_args()
    sort_filees_by_type(args.folder)
if __name__ == "__main__":
    main()
