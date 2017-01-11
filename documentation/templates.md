# Template Language
---
## Importing and serverside use
Importing the render function:
```python
from template_engine.parser import render
```

Creating the template response handler:
```python
def template_handler(response):
  rendered_text = render('template.html', {'variable': 'value'})
  response.write(rendered_text)

```

Registering URLs and starting the server
```python
server = Server()
server.register(r'/template', template_handler)
server.run()
```

---
## Contextual Variable Rendering
Using `{{ x }}` syntax you can pass variables and data to the HTML document.
### Single Variables
Using this render function:
```python
parser.render('template_name.html', {'username': 'Luke' })
```
This HTML:
```html
<p>Username is {{ username }}</p>
```
Becomes:
```html
<p>Username is Luke</p>
```
### Objects
Using this render function:
```python
class User:
  def __init__(self, name, email):
    self.name = name
    self.user = user

luke = User('Luke Tuthill', 'thisisnotmyemail@gmail.com')
parser.render('template_name.html', {'user': luke})
```
This HTML file:
```html
<p>Username is {{ user.name }}</p>
<p>Email is {{ user.email }}</p>
```
Becomes:
```html
<p>Username is Luke Tuthill</p>
<p>Email is thisisnotmyemail@gmail.com</p>
```

### Expression Rendering
You are also able to render Python expressions inside the pair of `{{ }}`s:
```html
<p>
  {{ 'hello ' * (1 + 2) }}
</p>
```
Becomes:
```html
<p>
  hello hello hello
</p>
```

---

## If Statements

Content inside a pair of `{% if %}` and `{% end if %}` tags is only generated if the python expression inside the `{% if expression %}` clause returns true.

```html
{% if expression %}
<p>code if expresion is true</p>
{% end if %}
```
### Else Clause
Optionally, you are able to add a third tag into the if statement that renders the HTML content inside it if the if expression evaluates to False.

```html
{% if expression %}
  <p>code if expresion is true</p>
{% else %}
  <p>code if expresion is false</p>
{% end if %}
```

Note that `else if` or `elif` statements are not supported.

---
## Include Statements
Include statements allow you to include sections of HTML in several files.

File `header.html`:
```html
<h1>This is a header!</h1>
```

File `login.html`:
```html
{% include header.html %}
<form>
  <input type='text'>
  <input type='submit'>
</form>
```
When rendered, `login.html` will become:
```html
<h1>This is a header!</h1>
<form>
  <input type='text'>
  <input type='submit'>
</form>
```
---
## For Statements
For statements iterate through an iterable expression, passing the content returned from the iterable into an iterator variable. These iterator variables can be referenced locally using normal `{{ x }}` expression syntax.

This HTML:
```html
{% for i in range(5) %}
  <p>Your number is {{ i }}!</p>
{% end for %}
```
Becomes:
```html
<p>Your number is 0!</p>
<p>Your number is 1!</p>
<p>Your number is 2!</p>
<p>Your number is 3!</p>
<p>Your number is 4!</p>
```

You may also pass contextual variables to the for statement:
```python
parser.render('some_template.html', {'array': ['hello', 'world']})
```
```html
{% for i in array %}
  <p>{{ i }}</p>
{% end for %}
```
Becomes:
```html
<p>Hello</p>
<p>World</p>
```
---
## Comment Statements
Content inside a pair of `{% comment %}` and `{% end comment %}` tags is ignored and taken out of the HTML.
```html
<p>
  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut ipsum nisi, placerat eu felis vitae, consequat elementum justo.
<p>
<p>
   Curabitur tellus felis, varius ac quam non, malesuada volutpat turpis. Nulla auctor porttitor sagittis. Aliquam quis dictum nulla.
</p>
  {% comment %}
    Can someone change this placeholder text?
  {% end comment %}
<p>
  Vivamus a condimentum metus. Vestibulum tempor erat a rhoncus tristique. Integer blandit nisi sit amet felis ultricies, et gravida est elementum. Praesent tincidunt purus semper, lacinia lectus sed, tincidunt nibh.
</p>
<p>
  Nulla facilisi. Nam luctus, lacus a bibendum tincidunt, purus magna malesuada felis, eget condimentum leo diam eu justo.
</p>
```

---
Author: Luke Tuthill | [github](https://github.com/lyneca) | [linkedin](https://www.linkedin.com/in/lyneca)
