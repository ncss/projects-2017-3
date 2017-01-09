import re
import os
from nodes import GroupNode, ExpressionNode, HTMLNode

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates')

TOKEN_REGEX = re.compile(r"({[{%].*?[}%]})")

"""
{% for f in person.friends %}
<li class='friend'>
{{ f.name.title() }} {{ f.age }} {% if f.has_nickname() %} ({{ f.nickname }}) {% end if %}
</li>
{% end for %}
"""

def parse(tokens, up_to=0, parent=GroupNode()):
    while up_to < len(tokens):
        token = tokens[up_to]
        if token['label'] == 'expression':
            node = ExpressionNode(token['contents'])
            parent.add_child(node)
        elif token['label'] == 'html':
            node = HTMLNode(token['contents'])
            parent.add_child(node)
        elif token['label'] == 'include':
            with open(token['contents']) as f:
                node = parse(lexer(f.read()), 0, parent)
        up_to += 1
    return parent

def lexer(text):
    tags = TOKEN_REGEX.split(text)
    tokens = [identify_token(token) for token in tags]
    return tokens

def create_token(contents, label):
    return {"contents": contents, "label": label}

def identify_token(token):
    if token.startswith("{%") and token.endswith("%}"):
        # Not expression
        term_list = token[2:-2].strip().split()
        keyword = term_list[0]
        if keyword == "include":
            return create_token(term_list[1], "include")
        # TODO The rest of the keywords
    elif token.startswith("{{") and token.endswith("}}"):
        # expression
        return create_token(token[2:-2].strip(), "expression")
    else:
        return create_token(token, "html")

def render(fname, context):
    template_path = os.path.join(TEMPLATE_DIR, fname)
    with open(template_path) as template:
        eval_tree = parse(lexer(template.read()))
    return eval_tree.render(context)


print(render('test_template.html', {'a': 10}))
