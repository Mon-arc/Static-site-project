import unittest

from htmlnode import *
from textnode import *
from markdown_conv import *


class TestHtmlNode(unittest.TestCase):
    def test_props_html(self):
        html_node = HTMLNode(None, None, None, {
                             "href": "https://www.google.com", "target": "_blank"})
        result = html_node.props_to_html()
        self.assertEqual(
            result, " href=\"https://www.google.com\" target=\"_blank\"")
        
    def test_nodes(self):
        child1 = HTMLNode("a", "Meow", None, None)
        child2 = HTMLNode("p", "Paragraph", None, None)
        node = HTMLNode("p", "this is the text in the paragraph", [child1, child2], {"href": "https://www.google.com", "target": "_blank"})
        result = node.__repr__()
        expected = '''tag: p\nvalue: this is the text in the paragraph\nchildren: [tag: a\nvalue: Meow\nchildren: None\nprops: '\', tag: p\nvalue: Paragraph\nchildren: None\nprops: '\']\nprops: ' href=\"https://www.google.com\" target=\"_blank\"\''''
        self.assertEqual(result, expected)
    
    def test_edge(self):
        node = HTMLNode(None, None, None, None)
        result = node.__repr__()
        expected = '''tag: None\nvalue: None\nchildren: None\nprops: '\''''
        self.assertEqual(result, expected)
    

    def test_conversion(self):
        text_node = TextNode("meow", TextType.BOLD)
        text_node2 = TextNode("link", TextType.LINK, "funnyURLhere")
        text_node3 = TextNode("Alt text", TextType.IMAGE, "https://insertfunnypichere")
        leaf_node = LeafNode('b', "meow")
        leaf_node2 = LeafNode('a', "link", {"href": "funnyURLhere"})
        leaf_node3 = LeafNode("img", "", {"src": "https://insertfunnypichere",
                                          "alt": "Alt text"})
        conv = text_node_to_html_node(text_node)
        conv2 = text_node_to_html_node(text_node2)
        conv3 = text_node_to_html_node(text_node3)
        self.assertEqual(conv, leaf_node)
        self.assertEqual(conv2, leaf_node2)
        self.assertEqual(conv3, leaf_node3)





class TestLeafNode(unittest.TestCase):
    def test_leaf_render(self):
        leaf_node = LeafNode("p", "This is a paragraph of text.")
        leaf_node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        leaf_node3 = LeafNode("a", None, {"target": "https://www.github.com/Mon-arc"})
        expected1 = '<p>This is a paragraph of text.</p>'
        expected2 = '<a href="https://www.google.com">Click me!</a>'
        expected3 = '<a target="https://www.github.com/Mon-arc"></a>'
        self.assertEqual(leaf_node.to_html(), expected1)
        self.assertEqual(leaf_node2.to_html(), expected2)
        self.assertRaises(ValueError) 

class TestParentNode(unittest.TestCase):
    def test_recursion(self):
        parent_node = ParentNode(
            'p',
            [
                LeafNode('b', "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode('i', "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = '''<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'''
        parent_node2 = ParentNode(
            'p',
            [
                ParentNode(
                    'p',
                    [
                        LeafNode('b', "Bold text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
            ],
        )
        expected2 = '''<p><p><b>Bold text</b>Normal text</p></p>'''
        parent_node3 = ParentNode('p', None)
        self.assertEqual(parent_node.to_html(), expected)
        self.assertEqual(parent_node2.to_html(), expected2)
        self.assertRaises(ValueError)

class TestNodeConversion(unittest.TestCase):
    def test_convert_node(self):
        text_node = TextNode("Convert *this* node", TextType.TEXT)
        text_node2 = TextNode("Convert **this** node", TextType.TEXT)
        text_node3 = TextNode("Code here: `code block` meow lmao", TextType.TEXT)
        result = split_nodes_delimiter([text_node], '*', TextType.ITALIC)
        result2 = split_nodes_delimiter([text_node2], '**', TextType.BOLD)
        result3 = split_nodes_delimiter([text_node3], '`', TextType.CODE)
        expected = [
            TextNode("Convert ", TextType.TEXT),
            TextNode("this", TextType.ITALIC),
            TextNode(" node", TextType.TEXT)
        ]
        expected2 = [
            TextNode("Convert ", TextType.TEXT),
            TextNode("this", TextType.BOLD),
            TextNode(" node", TextType.TEXT)
        ]
        expected3 = [
            TextNode("Code here: ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" meow lmao", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
        self.assertEqual(result2, expected2)
        self.assertEqual(result3, expected3)
        


if __name__ == "__main__":
    unittest.main()
