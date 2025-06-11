import os
def open_folder_reed_file(folder):
    data=[]
    if not os.path.exists(folder):
        print("not folder")
        return data
    for fname in os.listdir(folder):
        md=os.path.join(folder,fname)
        with open(md, "r") as f:
            file_line=f.readlines()
            data.extend([el.strip( ) for el in file_line if el.strip()])
    return data            

def write_info_file(md, fname):
    with open(fname,"w",encoding="utf-8") as f:
        for el in md:
            f.write(el + '\n')
def main():
    folder="/home/harutyun/Desktop/home-work/dir1"
    prog_logic=open_folder_reed_file(folder)
    write_info_file(prog_logic,"result_06.05.txt")
main()