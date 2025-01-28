import os
from os.path import isfile
from textnode import *
import shutil

def main():
    copy_static_to_public("static/", "public")



def copy_static_to_public(src_dir, dest_dir, first_call=True):
    if first_call and os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    if first_call:
        os.mkdir(dest_dir)
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            print(src_path)
        else:
            os.mkdir(dest_path)
            copy_static_to_public(src_path, dest_path, False)




if __name__ == "__main__":
    main()
