import re

text = """
{% include header.html %}
<section id='profile'>
<h1>{{ person.name }}</h1>
<ul id='friends-list'>
</ul>
</section>
{% include footer.html %}
"""

"""
{% for f in person.friends %}
<li class='friend'>
{{ f.name.title() }} {{ f.age }} {% if f.has_nickname() %} ({{ f.nickname }}) {% end if %}
</li>
{% end for %}
"""

def parse(tokens, up_to):
    while up_to < len(tokens):
        token = tokens[up_to]
        if token['label'] == 'expression':

        up_to += 1

def get_tokens(text):
    return re.split(r"({[{%].*?[}%]})", text)

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

for token in get_tokens(text):
    print(identify_token(token))
