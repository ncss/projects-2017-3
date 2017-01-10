import re
import os
from .nodes import GroupNode, ExpressionNode, HTMLNode, IfNode, ForNode, CommentNode

class TemplateSyntaxException(Exception):
    pass

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates')

TOKEN_REGEX = re.compile(r'({[{%].*?[}%]})')

def parse(tokens, up_to, parent, parent_type=None):
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
        elif token['label'] == 'for':
            node = ForNode(**token['contents'])
            parent.add_child(node)
            up_to += 1
            parse_results = parse(tokens, up_to, GroupNode(), 'for')
            node.set_child(parse_results[0])
            up_to = parse_results[1]
        elif token['label'] == 'end_for':
            if parent_type == 'for':
                up_to += 1
                return parent, up_to
            else:
                raise TemplateSyntaxException('Unexpected end of for')
        elif token['label'] == 'comment':
            node = CommentNode()
            parent.add_child(node)
            up_to += 1
            parse_results = parse(tokens, up_to, GroupNode(), 'comment')
            up_to = parse_results[1]
        elif token['label'] == 'end_comment':
            if parent_type == 'comment':
                up_to += 1
                return parent, up_to
            else:
                raise TemplateSyntaxException('Unexpected end of comment')
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
        elif keyword == 'for':
            return create_token({'iterator': term_list[1], 'iterable': ' '.join(term_list[3:])}, 'for')
        elif ' '.join(term_list) == 'end for':
            return create_token(None, 'end_for')
        elif keyword == 'comment':
            return create_token(None, 'comment')
        elif ' '.join(term_list) == 'end comment':
            return create_token(None, 'end_comment')
        # TODO The rest of the keywords
    elif token.startswith('{{') and token.endswith('}}'):
        # expression
        return create_token(token[2:-2].strip(), 'expression')
    else:
        return create_token(token, 'html')

def render(fname, context):
    template_path = os.path.join(TEMPLATE_DIR, fname)
    with open(template_path) as template:
        eval_tree = parse(lexer(template.read()), 0, GroupNode())[0]
    return eval_tree.render(context)

if __name__ == '__main__':
    print(render('test_template.html', {'a': ['hello', 'world']}))
