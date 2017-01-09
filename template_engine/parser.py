import re
from nodes import GroupNode, ExpressionNode, HTMLNode

TOKEN_REGEX = re.compile(r"({[{%].*?[}%]})")

text = """
<section id='profile'>
<h1>{{ a }}</h1>
<ul id='friends-list'>
</ul>
</section>
"""

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

def render(contents, context):
    eval_tree = parse(lexer(contents))
    return eval_tree.render(context)


print(render(text, {'a': 10}))
