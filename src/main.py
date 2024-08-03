import os
import shutil
from markdown import markdown_to_html_node, extract_title


def main():
    copy_to_dest("static", "public")
    generate_pages_recursively("content", "template.html", "public")


def copy_to_dest(src_path, dest_path):
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.mkdir(dest_path)
    for item in os.listdir(src_path):
        src_item = os.path.join(src_path, item)
        dest_item = os.path.join(dest_path, item)
        if os.path.isfile(src_item):
            shutil.copy(src_item, dest_item)
        else:
            copy_to_dest(src_item, dest_item)


def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        src_item = os.path.join(dir_path_content, item)
        dest_item = os.path.join(dest_dir_path, item)
        if os.path.isfile(src_item):
            dest_item_html = os.path.splitext(dest_item)[0] + '.html'
            generate_page(src_item, template_path, dest_item_html)
        else:
            generate_pages_recursively(src_item, template_path, dest_item)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as from_file:
        markdown = from_file.read()
    with open(template_path) as template_file:
        template = template_file.read()
    html_node = markdown_to_html_node(markdown)
    html_string = html_node.to_html()
    title = extract_title(markdown)
    new_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as dest_file:
        dest_file.write(new_page)


main()
