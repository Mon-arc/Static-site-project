import os
from pathlib import Path
from gencontent import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_path = os.listdir(dir_path_content)

    for directory in content_path:
        content_path = os.path.join(dir_path_content, directory)

        if os.path.isdir(content_path):
            new_dest_dir = os.path.join(dest_dir_path, directory)
            os.makedirs(new_dest_dir, exist_ok=True)

            generate_pages_recursive(content_path, template_path, new_dest_dir)

        elif directory.endswith('.md'):
            html_file = directory.replace('.md', '.html')
            if html_file == 'index.html':
                dest_path = os.path.join(dest_dir_path, 'index.html')
            else:
                page_dir = os.path.join(dest_dir_path, directory[:-3])
                os.makedirs(page_dir, exist_ok=True)
                dest_path = os.path.join(page_dir, 'index.html')

            generate_page(content_path, template_path, dest_path)

