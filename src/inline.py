import re
from textnode import TextNode, TextType


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return list(map(lambda textnode: textnode.to_html_node(), text_nodes))


def text_to_textnodes(text):
    initial_node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([initial_node], '**', TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, '*', TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, '`', TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    return split_nodes_link(new_nodes)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError("Invalid Markdown Syntax")
        for i in range(len(split_text)):
            text = split_text[i]
            if i % 2 == 0:
                new_nodes.append(TextNode(text, node.text_type, node.url))
            else:
                new_nodes.append(TextNode(text, text_type, node.url))
    return new_nodes


def split_nodes_image(old_nodes):
    return _split_nodes_by_extractor(old_nodes, extract_markdown_images, TextType.IMAGE)


def split_nodes_link(old_nodes):
    return _split_nodes_by_extractor(old_nodes, extract_markdown_links, TextType.LINK)


def _split_nodes_by_extractor(old_nodes, extractor, text_type):
    if text_type not in [TextType.IMAGE, TextType.LINK]:
        raise ValueError("text type must be image or link")
    new_nodes = []
    for node in old_nodes:
        extracts = extractor(node.text)
        if node.text_type != TextType.TEXT or len(extracts) == 0:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for extract in extracts:
            text, link = extract
            delimiter = f"![{text}]({link})" if text_type == TextType.IMAGE else f"[{text}]({link})"
            head_text, remaining_text = remaining_text.split(delimiter, 1)
            if len(head_text) > 0:
                new_nodes.append(TextNode(head_text, TextType.TEXT))
            new_nodes.append(TextNode(text, text_type, link))
        if len(remaining_text) > 0:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)]\((.*?)\)", text)
