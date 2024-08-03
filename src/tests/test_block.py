import unittest
from src.block import block_to_block_type, block_to_html_node, BlockType
from src.htmlnode import HTMLNode


class TestBlock(unittest.TestCase):
    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# test"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```test```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```python\nprint('hello world')\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type(">test\n>test2"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(">test\n```"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("* aaa\n- bbb"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("* aaa\n bbb"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1. aaa\n2. bbb"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. aaa\n1. bbb"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("0. aaa\n1. bbb"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(". aaa\n. bbb"), BlockType.PARAGRAPH)

    def test_block_to_html_node(self):
        # BlockType.HEADING
        self.assertEqual(block_to_html_node("# This is a heading"),
                         HTMLNode("h1", "This is a heading"))
        self.assertEqual(block_to_html_node("## This is a heading"),
                         HTMLNode("h2", "This is a heading"))

        # BlockType.CODE
        self.assertEqual(block_to_html_node("```python\nprint('hello world')\n```"),
                         HTMLNode("pre", children=[
                             HTMLNode("code", "python\nprint('hello world')\n")
                         ]))

        # BlockType.QUOTE
        self.assertEqual(block_to_html_node(">First Quote\n>Second quote"),
                         HTMLNode("blockquote", "First Quote\nSecond quote"))

        # BlockType.UNORDERED_LIST
        self.assertEqual(
            block_to_html_node(
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item"),
            HTMLNode("ul", children=[
                HTMLNode("li", "This is the first list item in a list block"),
                HTMLNode("li", "This is a list item"),
                HTMLNode("li", "This is another list item"),
            ])
        )

        # BlockType.ORDERED_LIST
        self.assertEqual(
            block_to_html_node(
                "1. This is the first list item in a list block\n2. This is a list item\n3. This is another list item"),
            HTMLNode("ol", children=[
                HTMLNode("li", "This is the first list item in a list block"),
                HTMLNode("li", "This is a list item"),
                HTMLNode("li", "This is another list item"),
            ])
        )

        # BlockType.PARAGRAPH with children
        self.assertEqual(
            block_to_html_node("This is a paragraph of text. It has some **bold** and *italic* words inside of it."),
            HTMLNode("p", children=[
                HTMLNode(value="This is a paragraph of text. It has some "),
                HTMLNode("b", "bold"),
                HTMLNode(value=" and "),
                HTMLNode("i", "italic"),
                HTMLNode(value=" words inside of it."),
            ])
        )


if __name__ == '__main__':
    unittest.main()
