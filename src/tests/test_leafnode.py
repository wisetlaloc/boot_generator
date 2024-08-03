import unittest

from src.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_p(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://example.com\">Click me!</a>")

    def test_value_error(self):
        with self.assertRaises(ValueError):
            LeafNode("a")


if __name__ == '__main__':
    unittest.main()
