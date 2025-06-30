import os
import argparse
def get_folder_sort_grup_files(folder):
    md = {}
    for fname in os.listdir(folder):
        fol_file= os.path.join(folder, fname)
        if os.path.isfile(fol_file):
            type_file = os.path.splitext(fname)[1][1:].lower()
            if not type_file:
                type_file = 'other'
            if type_file not in md:
                md[type_file] = []
            md[type_file].append(fname)
    return md
def main():
    parser = argparse.ArgumentParser(description="Grouping files by type in the dictionary.")
    parser.add_argument("-d", "--directory", required=True, help="Path to directory.")
    args = parser.parse_args()
    result = get_folder_sort_grup_files(args.directory)
    for F_type, file in result.items():
        print(f"{F_type}: {file}")
if __name__ == "__main__":
    main()





