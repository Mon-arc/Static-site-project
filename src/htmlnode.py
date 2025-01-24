from textnode import *

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError


    def props_to_html(self):
        if self.props == None:
            return ""
        else:
            html = ""
            for prop in self.props:
                html += " " + prop + "=" + '"' + self.props[prop] + '"'

        return html

    def __repr__(self):
        return f"tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: '{self.props_to_html()}'"


class LeafNode(HTMLNode): #Inherit from HTMLNode
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag == None:
            return self.value
        if self.tag == 'a' and self.props != None:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"

    def props_to_html(self):
        return super().props_to_html()


    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

class ParentNode(HTMLNode):
    def __init__(self, tag,  children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("All parent nodes must have a tag")
        if self.children == None:
            raise ValueError("All children of parent nodes must have value")
        
        html = f"<{self.tag}{self.props_to_html()}>"

        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        closing = f"</{self.tag}>"

        return html + children_html + closing


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")
