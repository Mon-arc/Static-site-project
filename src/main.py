import os
import shutil

from genpages import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    os.makedirs(dir_path_public, exist_ok=True)

    generate_pages_recursive(dir_path_content, template_path, dir_path_public)

main()
