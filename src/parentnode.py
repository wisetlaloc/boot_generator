from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if children is None:
            raise ValueError("children cannot be None")
        if tag is None:
            raise ValueError("tag cannot be None")
        super().__init__(tag, None, children, props)

    def to_html(self):
        children_to_html = ''.join(map(lambda x: x.to_html(), self.children))
        return f"<{self.tag}{self.props_to_html()}>{children_to_html}</{self.tag}>"
