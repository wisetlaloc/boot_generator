import unittest

from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "_target": "_blank"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" _target=\"_blank\"")

    def test_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "_target": "_blank"})
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode(props={"href": "https://www.google.com", "_target": "_blank"})
        self.assertEqual(node.__repr__(),
                         "HTMLNode(None, None, None, {'href': 'https://www.google.com', '_target': '_blank'})")


