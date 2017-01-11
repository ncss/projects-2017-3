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

class ForNode(Node):
    def __init__(self, iterator, iterable):
        self._iterator = iterator
        self._iterable = iterable
        self._child = None

    def __str__(self):
        return self.__repr__()

    def set_child(self, child):
        self._child = child

    def __repr__(self):
        return "<ForNode: '" + self._iterator + '; ' + self._child + "'>"

    def render(self, context):
        iterable = eval(self._iterable, {}, context)
        rendered_children = []
        for i in iterable:
            new_context = dict(context)
            new_context[self._iterator] = i
            rendered = self._child.render(new_context)
            if rendered.strip():
                rendered_children.append(rendered)
        return ''.join(rendered_children)

class HTMLNode(Node):
    def __init__(self, content):
        self._content = content

    def render(self, context):
        return self._content

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<HTMLNode: '" + head(self._content, 20) + "'>"

class IfNode(Node):
    def __init__(self, predicate):
        self._predicate = predicate
        self._children = {'True': GroupNode(), 'False': GroupNode()}

    def render(self, context):

        predicate_result = eval(self._predicate, {}, context)

        if predicate_result:
            true_node = self._children['True']
            return true_node.render(context)
        else:
            false_node = self._children['False']
            return false_node.render(context)

    def add_true_child(self, child):
        true_node = self._children['True']
        true_node.add_child(child)

    def add_false_child(self, child):
        false_node = self._children['False']
        false_node.add_child(child)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<IfNode: '" + str(self._children["True"]) + "' EndIf>"
        #return "<IfNode: '" + head(self._predicate, 20) + "'>"

class GroupNode(Node):
    def __init__(self):
        self._children = []

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
        return "<GroupNode: '" + str(self._children) + "'>"

class CommentNode(Node):
    def __init__(self):
        self._children = []

    def add_child(self, child):
        self._children.append(child)

    def render(self, context):
        out = ''
        return out

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<CommentNode: '" + str(self._children) + "'>"
