import unittest

from src.parentnode import ParentNode
from src.leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_no_tag_init(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode(value='text')])

    def test_no_children_init(self):
        with self.assertRaises(ValueError):
            ParentNode('a')

    def test_to_html_children(self):
        child1 = LeafNode(value='text')
        child2 = LeafNode('p', 'text2')
        parent = ParentNode('div', [child1, child2], {"class": "items"})
        self.assertEqual(parent.to_html(), '<div class="items">text<p>text2</p></div>')

    def test_to_html_nested(self):
        child = LeafNode(value='text')
        parent = ParentNode('div', [child])
        grand_parent = ParentNode('a', [parent], {"href": "https://example.com"})
        self.assertEqual(grand_parent.to_html(), '<a href="https://example.com"><div>text</div></a>')


if __name__ == '__main__':
    unittest.main()
