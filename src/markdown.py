import re
from src.block import block_to_html_node
from src.htmlnode import HTMLNode


def markdown_to_blocks(markdown):
    return list(filter(
        lambda block: len(block) > 0,
        map(
            lambda block: block.strip(),
            re.split(r"\s*(\n\s*){2,}", markdown)
        )
    ))


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    return HTMLNode("div", children=[block_to_html_node(block) for block in blocks])
