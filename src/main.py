import os
import shutil
from markdown import markdown_to_html_node, extract_title


def main():
    copy_to_dest("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


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
    with open(dest_path, "w") as dest_file:
        dest_file.write(new_page)


main()
