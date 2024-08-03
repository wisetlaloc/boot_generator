import unittest
from src.textnode import TextNode, TextType
from src.inline import (text_to_textnodes, split_nodes_delimiter, split_nodes_image, split_nodes_link,
                        extract_markdown_links, extract_markdown_images, text_to_children)
from src.htmlnode import HTMLNode


class TestInline(unittest.TestCase):
    def test_text_to_children(self):
        text = "python\nprint('hello world')\n"
        expected = [HTMLNode(value="python\nprint('hello world')\n"),]
        self.assertEqual(text_to_children(text), expected)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` "\
               "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

        text = "python\nprint('hello world')\n"
        expected = [TextNode("python\nprint('hello world')\n", TextType.TEXT),]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_split_nodes_delimiter_none(self):
        old_nodes = [TextNode("text", TextType.TEXT)]
        delimiter = '`'
        text_type = TextType.CODE
        result = split_nodes_delimiter(old_nodes, delimiter, text_type)
        expected = [TextNode("text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_invalid_markdown(self):
        old_nodes = [TextNode("text`text", TextType.TEXT)]
        delimiter = '`'
        text_type = TextType.CODE
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, delimiter, text_type)

    def test_split_nodes_delimiter_one(self):
        old_nodes = [TextNode("text`code here` blah blah", TextType.TEXT)]
        delimiter = '`'
        text_type = TextType.CODE
        result = split_nodes_delimiter(old_nodes, delimiter, text_type)
        expected = [
            TextNode("text", TextType.TEXT),
            TextNode("code here", TextType.CODE),
            TextNode(" blah blah", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_two(self):
        old_nodes = [TextNode("text`code1`new`code2`etc", TextType.TEXT)]
        delimiter = '`'
        text_type = TextType.CODE
        result = split_nodes_delimiter(old_nodes, delimiter, text_type)
        expected = [
            TextNode("text", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode("new", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode("etc", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_two_text_nodes(self):
        old_nodes = [
            TextNode("text`code here` blah blah", TextType.TEXT),
            TextNode("text`code here` blah blah", TextType.TEXT),
        ]
        delimiter = '`'
        text_type = TextType.CODE
        result = split_nodes_delimiter(old_nodes, delimiter, text_type)
        expected = [
            TextNode("text", TextType.TEXT),
            TextNode("code here", TextType.CODE),
            TextNode(" blah blah", TextType.TEXT),
            TextNode("text", TextType.TEXT),
            TextNode("code here", TextType.CODE),
            TextNode(" blah blah", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_text_and_irrelevant_node(self):
        old_nodes = [
            TextNode("text`code here` blah blah", TextType.TEXT),
            TextNode("aaa", TextType.BOLD)
        ]
        delimiter = '`'
        text_type = TextType.CODE
        result = split_nodes_delimiter(old_nodes, delimiter, text_type)
        expected = [
            TextNode("text", TextType.TEXT),
            TextNode("code here", TextType.CODE),
            TextNode(" blah blah", TextType.TEXT),
            TextNode("aaa", TextType.BOLD)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and "
            "![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and "
            "[to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and " \
               "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(result, expected)

        only_alt = "![alt message](https://example.com"
        self.assertEqual(extract_markdown_images(only_alt), [])

        only_src = "[xxx](https://example.com)"
        self.assertEqual(extract_markdown_images(only_src), [])

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and " \
               "[to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(result, expected)

        only_text = "[alt message](https://example.com"
        self.assertEqual(extract_markdown_links(only_text), [])

        only_href = "xxx](https://example.com)"
        self.assertEqual(extract_markdown_links(only_href), [])


if __name__ == '__main__':
    unittest.main()
