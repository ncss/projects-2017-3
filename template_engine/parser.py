import re
import os
from .nodes import GroupNode, ExpressionNode, HTMLNode, IfNode, ForNode, CommentNode

class TemplateSyntaxException(Exception):
    pass

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates')

TOKEN_REGEX = re.compile(r'({[{%].*?[}%]})')

def parse(tokens, up_to, parent, parent_type=None):
    """
    Parses the tokens and converts them into Nodes

    Args:
        tokens (list): A list of all the tokens
        up_to (int): A counter to remember what token we should be looking up
        parent (Node): A parent node which all the parsed tokens will be added to
        parent_type (optional str): If this is not None, then we are parsing until we find the end version of the parent_type

    Returns:
        Node: The updated parent node
        up_to: Where the parser finished looking up.
    """
    while up_to < len(tokens):
        token = tokens[up_to]
        if token['label'] is None: # Something bad happened. We'll skip it :)
            print('TOKEN! ' + token)
        if token['label'] == 'expression': # Convert the token into an Expression
            node = ExpressionNode(token['contents'])
            parent.add_child(node)
            up_to += 1
        elif token['label'] == 'html': # Convert the token into some HTML
            node = HTMLNode(token['contents'])
            parent.add_child(node)
            up_to += 1
        elif token['label'] == 'include': # Convert the token into an IncludeNode
            with open(os.path.join(TEMPLATE_DIR, token['contents'])) as f:
                # Open the template included and parse it
                # Because we specify the current parent as the parent, all parsed nodes will be added to our parent
                node = parse(lexer(f.read()), 0, parent)[0]
            up_to += 1
        elif token['label'] == 'if': # Convert the token into an IfNode
            # Create the IfNode with our condition
            node = IfNode(token['contents'])
            parent.add_child(node)
            up_to += 1
            # Parse the block of tokens for the True block
            parse_results = parse(tokens, up_to, node._children['True'], 'if')
            up_to = parse_results[1]
            next_token = tokens[up_to]
            # If the next token is an else token, we have to parse it again, but add the Nodes to the False block
            if next_token['label'] == 'else':
                up_to += 1
                parse_results = parse(tokens, up_to, node._children['False'], 'else')
                up_to = parse_results[1]
        elif token['label'] == 'end_if' :
            if parent_type == 'if' or parent_type == 'else':
                up_to += 1
                return parent, up_to
            else:
                raise TemplateSyntaxException('Unexpected end of if')
        elif token['label'] == 'else':
            if parent_type == 'if':
                return parent, up_to
            else:
                raise TemplateSyntaxException('Unexpected else')
        elif token['label'] == 'for':
            # Fancy kwargs because our dictionary matches the args
            node = ForNode(**token['contents'])
            parent.add_child(node)
            up_to += 1
            # Parse the for body and set it to the ForNode
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
            # Just parse everything until the end of the comment, but just don't do anything with the result
            parse_results = parse(tokens, up_to, GroupNode(), 'comment')
            up_to = parse_results[1]
        elif token['label'] == 'end_comment':
            if parent_type == 'comment':
                up_to += 1
                return parent, up_to
            else:
                raise TemplateSyntaxException('Unexpected end of comment')
        else:
            raise TemplateSyntaxException('Invalid template tag: {}'.format(token['label']))
    return parent, up_to

def lexer(text):
    """
    Otherwise known as a "tokenizer". Finds all the tokens within the template.

    Args:
        text (string): The template

    Returns:
        list: A list of all the tokens
    """
    tags = TOKEN_REGEX.split(text)
    tokens = [identify_token(token) for token in tags]
    return tokens

def create_token(label, contents):
    """
    Helper function to create a token.

    Args:
        label (string): What the token is actually called
        contents (any): What the contents of the token should be

    Returns:
        dict of (str: any): A dict representation of the token
    """
    return {'contents': contents, 'label': label}

def identify_token(token):
    """
    Identifies what sort of token a given inout is.

    Args:
        token (string): A string of HTML or template language

    Returns:
        dict of (str: any): A dict representation of the token
    """

    # If the token is a tag ({% ... %})
    if token.startswith('{%') and token.endswith('%}'):
        # We remove the first and last 2 characters since they are the tag identifiers
        # We also split the token so we can see what the keyword (first word) is
        term_list = token[2:-2].strip().split()
        keyword = term_list[0]
        if keyword == 'include':
            # The contents is the file we want to import
            return create_token('include', term_list[1])
        elif keyword == 'if':
            # The contents is the condition
            return create_token('if', ' '.join(term_list[1:]))
        elif ' '.join(term_list) == 'end if':
            return create_token('end_if', None)
        elif keyword == 'for':
            # The contents is a dictionary which contains the iterator and the iterable
            in_loc = term_list.index('in')
            # get the location of the in to split the query into iterator and iterable
            return create_token('for', {'iterator': "".join(term_list[1:in_loc]), 'iterable': ' '.join(term_list[in_loc+1:])})
        elif ' '.join(term_list) == 'end for':
            return create_token('end_for', None)
        elif keyword == 'comment':
            return create_token('comment', None)
        elif ' '.join(term_list) == 'end comment':
            return create_token('end_comment', None)
        elif keyword == 'else':
            return create_token('else', None)
        else: # Bad tag
            raise TemplateSyntaxException('Invalid template tag: {}'.format(token))
    # If the token is an expression ({{ ... }})
    elif token.startswith('{{') and token.endswith('}}'):
        # We remove the first and last 2 characters since they are the expression identifiers
        return create_token('expression', token[2:-2].strip())
    # Otherwise it's HTML
    else:
        return create_token('html', token)

def render(fname, context):
    """
    Evaluates the template at 'fname' to generate valid HTML.

    Args:
        fname (string): The file name of the target template in '../templates/'
        context (dict of str: any): A context so that the template can access Python variables

    Returns:
        string: Valid HTML with all the template language evaluated
    """
    template_path = os.path.join(TEMPLATE_DIR, fname)
    with open(template_path) as template:
        eval_tree = parse(lexer(template.read()), 0, GroupNode())[0]
    return eval_tree.render(context)

if __name__ == '__main__':
    print(render('test_template.html', {'a': ['hello', 'world']}))
