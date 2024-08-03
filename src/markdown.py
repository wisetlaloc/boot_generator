import re
from block import block_to_html_node
from parentnode import ParentNode


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
    return ParentNode("div", children=[block_to_html_node(block) for block in blocks])


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:].strip()
    raise ValueError("Could not find title in markdown")
