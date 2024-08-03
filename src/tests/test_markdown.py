import unittest
import textwrap
from src.markdown import markdown_to_blocks, markdown_to_html_node
from src.htmlnode import HTMLNode


class TestMarkdown(unittest.TestCase):
    def setUp(self):
        self.text = textwrap.dedent("""
            # This is a heading
            
            This is a paragraph of text. It has some **bold** and *italic* words inside of it.



            * This is the first list item in a list block
            * This is a list item
            * This is another list item
        """)

    def test_markdown_to_blocks(self):
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            textwrap.dedent("""
            * This is the first list item in a list block
            * This is a list item
            * This is another list item
            """).strip()
        ]
        self.assertEqual(len(markdown_to_blocks(self.text)), len(expected))
        self.assertEqual(markdown_to_blocks(self.text), expected)

    def test_markdown_to_html_node(self):
        expected = HTMLNode("div", children=[
            HTMLNode("h1", "This is a heading"),
            HTMLNode("p", children=[
                HTMLNode(value="This is a paragraph of text. It has some "),
                HTMLNode("b", "bold"),
                HTMLNode(value=" and "),
                HTMLNode("i", "italic"),
                HTMLNode(value=" words inside of it."),
            ]),
            HTMLNode("ul", children=[
                HTMLNode("li", "This is the first list item in a list block"),
                HTMLNode("li", "This is a list item"),
                HTMLNode("li", "This is another list item"),
            ])
        ])
        self.assertEqual(markdown_to_html_node(self.text), expected)


if __name__ == '__main__':
    unittest.main()
