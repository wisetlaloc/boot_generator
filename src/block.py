from enum import Enum
import re
from parentnode import ParentNode
from leafnode import LeafNode
from inline import text_to_children


class BlockType(Enum):
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'
    PARAGRAPH = 'paragraph'


def block_to_block_type(block):
    if re.match(r"#{1,6}\s.*", block):
        return BlockType.HEADING
    elif re.match(r"```.*```", block, flags=re.DOTALL):
        return BlockType.CODE
    elif _check_all_lines(lambda idx, line: line.startswith(">"), block):
        return BlockType.QUOTE
    elif _check_all_lines(lambda idx, line: line.startswith("* ") or line.startswith("- "), block):
        return BlockType.UNORDERED_LIST
    elif _check_all_lines(lambda idx, line: line.startswith(f"{idx + 1}."), block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.HEADING:
            tag, content = _tag_and_content_in_header(block)
            return create_from_content(tag, content)
        case BlockType.CODE:
            return ParentNode("pre", children=[
                create_from_content("code", re.sub(r"^```|```$", "", block))
            ])
        case BlockType.QUOTE:
            content = re.sub(r"^>\s", "", block, flags=re.MULTILINE)
            return create_from_content("blockquote", content)
        case BlockType.UNORDERED_LIST:
            items = re.sub(r"^\*\s|^-\s", "", block, flags=re.MULTILINE).splitlines()
            return ParentNode("ul", children=[create_from_content("li", item) for item in items])
        case BlockType.ORDERED_LIST:
            items = re.sub(r"^\d\.\s*", "", block, flags=re.MULTILINE).splitlines()
            return ParentNode("ol", children=[create_from_content("li", item) for item in items])
        case BlockType.PARAGRAPH:
            return create_from_content("p", block)
    raise ValueError(f"Unknown block type: {block_type}")


def create_from_content(tag, content, props=None):
    children = text_to_children(content)
    if len(children) == 1:
        return LeafNode(tag, children[0].value, None)
    else:
        return ParentNode(tag, children, props)


def _tag_and_content_in_header(block):
    match = re.match(r'^#*', block)
    count = len(match.group(0)) if match else 0
    return f"h{count}", re.sub(r"^#+\s", "", block)


def _check_all_lines(checker, block):
    lines = block.splitlines()
    for idx, line in enumerate(lines):
        if not checker(idx, line):
            return False
    return True
