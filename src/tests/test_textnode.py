import unittest

from src.textnode import TextNode, TextType
from src.leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_2(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a text node2", TextType.LINK, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_print(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        self.assertEqual(node.__repr__(), "TextNode(This is a text node, TextType.LINK, https://example.com)")

    def test_to_html_node(self):
        node = TextNode("This is a text node", TextType.TEXT)
        expected_node = LeafNode(None, "This is a text node")
        self.assertEqual(node.to_html_node(), expected_node)

        node = TextNode("This is a bold text", TextType.BOLD)
        expected_node = LeafNode("b", "This is a bold text")
        self.assertEqual(node.to_html_node(), expected_node)

        node = TextNode("This is an italic text", TextType.ITALIC)
        expected_node = LeafNode("i", "This is an italic text")
        self.assertEqual(node.to_html_node(), expected_node)

        node = TextNode("class HelloWorld\n\tdef main()\n\t\tprint('Hello, World!')", TextType.CODE)
        expected_node = LeafNode("code", "class HelloWorld\n\tdef main()\n\t\tprint('Hello, World!')")
        self.assertEqual(node.to_html_node(), expected_node)

        node = TextNode("example", TextType.LINK, "https://example.com")
        expected_node = LeafNode("a", "example", {"href": "https://example.com"})
        self.assertEqual(node.to_html_node(), expected_node)

        node = TextNode("an image", TextType.IMAGE, "https://example.com/image.png")
        expected_node = LeafNode("img", "", {"src": "https://example.com/image.png", "alt": "an image"})
        self.assertEqual(node.to_html_node(), expected_node)

    def test_to_html_node_invalid_type(self):
        node = TextNode("This is a text node", "invalid")
        with self.assertRaises(ValueError):
            node.to_html_node()


if __name__ == "__main__":
    unittest.main()
