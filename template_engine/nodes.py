import html

def head(string, n):
    return string[:n] if len(string) >= n else string

class Node:
    def __init__(self):
        pass

    def render(self, context):
        raise NotImplementedError()

class ExpressionNode(Node):
    def __init__(self, expression):
        self._expression = expression

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<ExpressionNode: '" + head(self._expression, 20) + "'>"

    def render(self, context):
        return html.escape(str(eval(self._expression, {}, context)))


class HTMLNode(Node):
    def __init__(self, content):
        self._content = content

    def render(self, context):
        return self._content

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<HTMLNode: '" + head(self._content, 20) + "'>"


class GroupNode(Node):
    def __init__(self, children=[]):
        self._children = children

    def add_child(self, child):
        self._children.append(child)

    def render(self, context):
        out = ''
        for child in self._children:
            out += child.render(context)
        return out

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<GroupNode: '" + self._children + "'>"
