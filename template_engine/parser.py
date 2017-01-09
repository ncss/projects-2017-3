import re
import os
from nodes import GroupNode, ExpressionNode, HTMLNode, IfNode

class TemplateSyntaxException(Exception):
    pass

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates')

TOKEN_REGEX = re.compile(r'({[{%].*?[}%]})')

'''
{% for f in person.friends %}
<li class='friend'>
{{ f.name.title() }} {{ f.age }} {% if f.has_nickname() %} ({{ f.nickname }}) {% end if %}
</li>
{% end for %}
'''

def parse(tokens, up_to=0, parent=GroupNode(), parent_type=None):
    while up_to < len(tokens):
        token = tokens[up_to]
        if token['label'] == 'expression':
            node = ExpressionNode(token['contents'])
            parent.add_child(node)
            up_to += 1
        elif token['label'] == 'html':
            node = HTMLNode(token['contents'])
            parent.add_child(node)
            up_to += 1
        elif token['label'] == 'include':
            with open(os.path.join(TEMPLATE_DIR, token['contents'])) as f:
                node = parse(lexer(f.read()), 0, parent)[0]
            up_to += 1
        elif token['label'] == 'if':
            node = IfNode(token['contents'])
            parent.add_child(node)
            up_to += 1
            parse_results = parse(tokens, up_to, node._children['True'], 'if')
            up_to = parse_results[1]
        elif token['label'] == 'end_if' :
            if parent_type == 'if':
                up_to += 1
                return parent, up_to
            else:
                raise TemplateSyntaxException('Unexpected end of if')
    return parent, up_to

def lexer(text):
    tags = TOKEN_REGEX.split(text)
    tokens = [identify_token(token) for token in tags]
    return tokens

def create_token(contents, label):
    return {'contents': contents, 'label': label}

def identify_token(token):
    if token.startswith('{%') and token.endswith('%}'):
        # Not expression
        term_list = token[2:-2].strip().split()
        keyword = term_list[0]
        if keyword == 'include':
            return create_token(term_list[1], 'include')
        elif keyword == 'if':
            return create_token(' '.join(term_list[1:]), 'if')
        elif ' '.join(term_list) == 'end if':
            return create_token(None, 'end_if')
        # TODO The rest of the keywords
    elif token.startswith('{{') and token.endswith('}}'):
        # expression
        return create_token(token[2:-2].strip(), 'expression')
    else:
        return create_token(token, 'html')

def render(fname, context):
    template_path = os.path.join(TEMPLATE_DIR, fname)
    with open(template_path) as template:
        eval_tree = parse(lexer(template.read()))[0]
    return eval_tree.render(context)


print(render('test_template.html', {'a': 1}))
