<!-- api.md, httt/doc/, httt : html_token_tag_tree
   - author: sceext <sceext@foxmail.com>
   - https://github.com/sceext2/html_token_tag_tree
  -->

# API of html_token_tag_tree
(*httt*: html_token_tag_tree)

`httt version 0.1.3.0`


## Contents

+ **[1. (module) `httt`](#1-module-httt)**
  
  + **[1.1 `httt.create_tree()`](#11-htttcreate_tree)**
  + **[1.2 `httt.get_text_between()`](#12-htttget_text_between)**
  + **[1.3 `httt.clean_html_text()`](#13-htttclean_html_text)**

+ **[2. (object) `httt_tree`](#2-object-httt_tree)**
  
  + **[2.1 Attributes](#21-attributes)**
    
    + `.name`
    + `.attr`
    + `.children`, `.c`
    + `.parent`, `.p`
    + `.index`
    + `._start_tag`
    + `._close_tag`
    + `._before_close`
  
  + **[2.2 `.html()`](#22-httt_treehtml)**
  + **[2.3 `.inner_html()`](#23-httt_treeinner_html)**
  + **[2.4 `.text()`](#24-httt_treetext)**
  + **[2.5 `.prev()`](#25-httt_treeprev)**
  + **[2.6 `.next()`](#26-httt_treenext)**
  + **[2.7 `.find()`](#27-httt_treefind)**
  + **[2.8 Debug function](#28-debug-function)**
    
    + `httt_tree.export()`

+ **[3. (object) `httt_nodelist`](#3-object-httt_nodelist)**
  
  + **[3.1 `httt_nodelist.text()`](#31-httt_nodelisttext)**
  + **[3.2 `httt_nodelist.html()`](#32-httt_nodelisthtml)**
  + **[3.3 `httt_nodelist.name()`](#33-httt_nodelistname)**
  + **[3.4 `httt_nodelist.find()`](#34-httt_nodelistfind)**
  + **[3.5 Set operations](#35-set-operations)**
    
    + `+`
    + `-`

+ **[4. CSS selectors supported by `httt` (14)](4-css-selectors-supported-by-httt-14)**

+ **[5. Debug functions for `httt`](#5-debug-functions-for-httt)**
  
  + `httt.p()`
  + `httt.debug_split_token()`
  + `httt.debug_build_tree()`
  + `httt.debug_parse_selector()`


## 1. (module) `httt`

Entry module of html_token_tag_tree. 

```
>>> import httt
>>> httt
<module 'httt' from '~/httt/httt/__init__.py'>
>>> 
```

+ *Attribute* : `httt.version` <br />
  version *str* of the *httt* library. 
  
  ```
  >>> httt.version
  'httt version 0.1.3.0 test201604051914'
  >>> 
  ```

### 1.1 `httt.create_tree()`
```
def create_tree(html_text): -> httt_tree
```

+ `html_text` : *str* <br />
  The raw html text

+ *return* httt_tree (object)

Parse the html text and build the html tree struct. 

Example: 

```
>>> with open('test/t1.html') as f:
...     raw_html = f.read()
... 
>>> root = httt.create_tree(raw_html)
>>> root
<httt.html_token_tag_tree.tree.httt_tree object at 0x7fb703f02320>
>>> 
```

### 1.2 `httt.get_text_between()`
```
def get_text_between(tag_a, tag_b): -> [] str
```

+ `tag_a`, `tag_b` : httt_token_tag (object)

+ *return* [] str

Get all text tokens between the two tags. 

Example: 

```
>>> print(head.html())
<head>
	<meta charset="utf-8" >
<!-- a simple test page for html_token_tag_tree -->
	<link rel="stylesheet" type="text/css" href="main.css" >
	<title>simple test page</title>
<style type="text/css" >
body	{
	background-color: #000;
}
</style>
<script type="text/javascript" >
	console.log('hello, world! ');
</script>
</head>
>>> title = head.find('title')[0]
>>> script = head.find('script')[0]
>>> text = httt.get_text_between(title._close_tag, script._start_tag)
>>> text
['\n', '\nbody\t{\n\tbackground-color: #000;\n}\n', '\n']
>>> 
```

### 1.3 `httt.clean_html_text()`
```
def clean_html_text(raw, strip=False): -> str or [] str
```

+ `raw` : *str* or [] str <br />
  Raw text (or text list) to clean

+ `strip` : *bool* <br />
  `strip()` html text after clean or not

Clean raw text (or text list) with html text rules. 
(eg. will replace all `\n`, `\t`, etc. to `' '` (space) chars. )

Example: 

```
>>> text = root.text()
>>> text
['\n', '\n\t', '\n', '\n\t', '\n\t', 'simple test page', '\n', '\nbody\t{\n\tbackground-color: #000;\n}\n', '\n', "\n\tconsole.log('hello, world! ');\n", '\n', '\n', '\n\t', 'Hello, world !\n\t', 'Test p1 <p>\n\t\t', '\n\t', 'test title\n\t', ' test p2 ', '\n\t', '\n\t\t', '\n\t\t', 'test 5', '\n\t\t', '\n\t\t', '\n\t', '\n', '\n']
>>> httt.clean_html_text(text)
[' ', ' ', ' ', ' ', ' ', 'simple test page', ' ', ' body { background-color: #000; } ', ' ', " console.log('hello, world! '); ", ' ', ' ', ' ', 'Hello, world ! ', 'Test p1 <p> ', ' ', 'test title ', ' test p2 ', ' ', ' ', ' ', 'test 5', ' ', ' ', ' ', ' ', ' ']
>>> httt.clean_html_text(text, strip=True)
['simple test page', 'body { background-color: #000; }', "console.log('hello, world! ');", 'Hello, world !', 'Test p1 <p>', 'test title', 'test p2', 'test 5']
>>> 
```


## 2. (object) `httt_tree`

One node (element) of the html tree. 

```
>>> root = httt.create_tree(raw_html)
>>> root
<httt.html_token_tag_tree.tree.httt_tree object at 0x7fb703f069b0>
>>> 
```

### 2.1 Attributes

+ `httt_tree.name` : *str* <br />
  Tag name (or element name) of this element (node). 
  
  Example: 
  
  ```
  >>> link = root.find('link')[0]
  >>> link.html()
  '<link rel="stylesheet" type="text/css" href="main.css" >'
  >>> link.name
  'link'
  >>> 
  ```

+ `httt_tree.attr` : {} <br />
  Attributes of this element. 
  
  Example: 
  
  ```
  >>> link.attr['type']
  'text/css'
  >>> link.attr
  {'href': 'main.css', 'rel': 'stylesheet', 'type': 'text/css'}
  >>> 
  ```

+ `httt_tree.children`, `httt_tree.c` : [] <br />
  Children elements of this element. 
  
  Used to traverse the html tree. 
  
  Example: 
  
  ```
  >>> root.name
  'html'
  >>> len(root.children)
  2
  >>> root.children[0].name
  'head'
  >>> root.children[1].name
  'body'
  >>> root.c == root.children
  True
  >>> link.html()
  '<link rel="stylesheet" type="text/css" href="main.css" >'
  >>> link.c
  []
  >>> 
  ```

+ `httt_tree.parent`, `httt_tree.p` : httt_tree or None <br />
  Parent element of this element. 
  
  Used to traverse the html tree. 
  
  Example: 
  
  ```
  >>> head = root.c[0]
  >>> head.name
  'head'
  >>> head.parent == root
  True
  >>> head.parent.name
  'html'
  >>> root.parent
  >>> head.parent == head.p
  True
  >>> 
  ```

+ `httt_tree.index` : *int* <br />
  Index of this element in its' parent.children list. 
  
  Example: 
  
  ```
  >>> root.name
  'html'
  >>> head = root.c[0]
  >>> head.name
  'head'
  >>> body = root.c[1]
  >>> body.name
  'body'
  >>> head.index
  0
  >>> body.index
  1
  >>> 
  ```

*Private attributes*

+ `httt_tree._start_tag` : httt_token_tag_attr (object) <br />
  Start tag (token) of this element. 

+ `httt_tree._close_tag` : httt_token_tag (object) <br />
  Close tag (token) of this element. 
  
  NOTE: the close tag maybe the same with the start tag. <br />
  NOTE: the close tag may not exist. (None)
  
  Example: 
  
  ```
  >>> root._start_tag
  <httt.html_token_tag_tree.token.httt_token_tag_attr object at 0x7fb703f03a58>
  >>> root._close_tag
  <httt.html_token_tag_tree.token.httt_token_tag object at 0x7fb703f068d0>
  >>> root._start_tag == root._close_tag
  False
  >>> 
  >>> link = root.find('link')[0]
  >>> link.html()
  '<link rel="stylesheet" type="text/css" href="main.css" >'
  >>> link._start_tag
  <httt.html_token_tag_tree.token.httt_token_tag_attr object at 0x7fb703f03b70>
  >>> link._close_tag
  <httt.html_token_tag_tree.token.httt_token_tag_attr object at 0x7fb703f03b70>
  >>> link._start_tag == link._close_tag
  True
  >>> 
  ```

+ `httt_tree._before_close` : httt_token_tag (object) <br />
  If the close tag not exist, this will referer to the tag (token) just
  before this element close. 
  
  Example: 
  
  ```
  >>> print(body.html())
  <body>
  	<h1>Hello, world !
  	<p>Test p1 &lt;p&gt;
  		<img src="logo.png" >
  	<h2>test title
  	<p> test p2 </p>
  	<section id="main" ><div><div class="test" ><div>
  		<span class="test" ><a id="test4" ></a></span>
  		<a href="#" >test 5</a>
  		<input type="button" >
  		<input type="text" >
  	</div></div></div></section>
  </body>
  >>> h1 = body.find('h1')[0]
  >>> h1.html()
  '<h1>Hello, world !\n\t'
  >>> h1.text()
  ['Hello, world !\n\t']
  >>> h1._start_tag
  <httt.html_token_tag_tree.token.httt_token_tag_attr object at 0x7fc2a5b3bb38>
  >>> h1._close_tag
  >>> h1._before_close
  <httt.html_token_tag_tree.token.httt_token_text object at 0x7fc2a5b3bb70>
  >>> h1._start_tag == h1._before_close
  False
  >>> 
  ```

### 2.2 `httt_tree.html()`
```
def html(self): -> str
```

+ *return* *str*

Get the **raw** html text of this element. 

### 2.3 `httt_tree.inner_html()`
```
def inner_html(self): -> str
```

+ *return* *str*

Get the raw inner html text of this element. 
Not include start tag and close tag text. 

Example: 

```
>>> print(head.html())
<head>
	<meta charset="utf-8" >
<!-- a simple test page for html_token_tag_tree -->
	<link rel="stylesheet" type="text/css" href="main.css" >
	<title>simple test page</title>
<style type="text/css" >
body	{
	background-color: #000;
}
</style>
<script type="text/javascript" >
	console.log('hello, world! ');
</script>
</head>
>>> print(head.inner_html())

	<meta charset="utf-8" >
<!-- a simple test page for html_token_tag_tree -->
	<link rel="stylesheet" type="text/css" href="main.css" >
	<title>simple test page</title>
<style type="text/css" >
body	{
	background-color: #000;
}
</style>
<script type="text/javascript" >
	console.log('hello, world! ');
</script>

>>> 
```

### 2.4 `httt_tree.text()`
```
def text(self): -> [] str
```

+ *return* [] str

Get all text tokens in this element. 

Example: 

```
>>> head.text()
['\n\t', '\n', '\n\t', '\n\t', 'simple test page', '\n', '\nbody\t{\n\tbackground-color: #000;\n}\n', '\n', "\n\tconsole.log('hello, world! ');\n", '\n']
>>> 
```

### 2.5 `httt_tree.prev()`
```
def prev(self): -> httt_tree (object) or None
```

+ *return* httt_tree (object) or None

Get the previous sibling element of this element. 
If no such elemnt, return None. 

### 2.6 `httt_tree.next()`
```
def next(self): -> httt_tree (object) or None
```

+ *return* httt_tree (object) or None

Get the next sibling element of this element. 
If no such element, return None. 

Example: 

```
>>> root.name
'html'
>>> root.prev()
>>> root.next()
>>> head = root.c[0]
>>> head.name
'head'
>>> head.prev()
>>> head.next().name
'body'
>>> head.next().next()
>>> head.next().prev().name
'head'
>>> 
```

### 2.7 `httt_tree.find()`
```
def find(self, selector): -> httt_nodelist (object)
```

+ `selector` : *str* <br />
  The CSS selector expression

+ *return* httt_nodelist (object)

Get elements by CSS selector in the tree of this element. 

Example: 

```
>>> link = root.find('link')
>>> len(link)
1
>>> link[0].html()
'<link rel="stylesheet" type="text/css" href="main.css" >'
>>> 
```

### 2.8 Debug function

+ `httt_tree.export()` <br />
  ```
  def export(self): -> {}
  ```
  
  Export tree info of this element for DEBUG. 
  
  Example: 
  
  ```
  >>> span = root.find('span')[0]
  >>> span.html()
  '<span class="test" ><a id="test4" ></a></span>'
  >>> e = span.export()
  >>> httt.p(e)
  {
      "_id": 45,
      "attr": {
          "class": "test"
      },
      "children": [
          {
              "_id": 46,
              "attr": {
                  "id": "test4"
              },
              "index": 0,
              "name": "a"
          }
      ],
      "index": 0,
      "name": "span"
  }
  >>> 
  ```


## 3. (object) `httt_nodelist`

```
>>> root
<httt.html_token_tag_tree.tree.httt_tree object at 0x7fc2a5b40208>
>>> e = root.find('*')
>>> isinstance(e, httt.html_token_tag_tree.nodelist.httt_nodelist)
True
>>> httt.html_token_tag_tree.nodelist.httt_nodelist
<class 'httt.html_token_tag_tree.nodelist.httt_nodelist'>
>>> len(e)
21
>>> 
```

### 3.1 `httt_nodelist.text()`
```
def text(self): -> [] str
```

Get all text tokens in this element set. 

### 3.2 `httt_nodelist.html()`
```
def html(self): -> [] str
```

Get raw html text of each element in this set. 

### 3.3 `httt_nodelist.name()`
```
def name(self): -> [] str
```

Get name of each element in this set. 

Example: 

```
>>> a = root.find('a')
>>> len(a)
2
>>> a.html()
['<a id="test4" ></a>', '<a href="#" >test 5</a>']
>>> a.name()
['a', 'a']
>>> a.text()
['test 5']
>>> 
```

### 3.4 `httt_nodelist.find()`
```
def find(self, selector): -> httt_nodelist (object)
```

+ `selector` : *str* <br />
  The CSS selector expression text

Find elements in this set. 

Example: 

```
>>> section = root.find('section')
>>> section.html()
['<section id="main" ><div><div class="test" ><div>\n\t\t<span class="test" ><a id="test4" ></a></span>\n\t\t<a href="#" >test 5</a>\n\t\t<input type="button" >\n\t\t<input type="text" >\n\t</div></div></div></section>']
>>> i = section.find('input')
>>> i.html()
['<input type="button" >', '<input type="text" >']
>>> 
```

### 3.5 Set operations

+ **`+`**
+ **`-`**

You can do set operations by `+` or `-` two *httt_nodelist* objects. 

Example: 

```
>>> print(body.html())
<body>
	<h1>Hello, world !
	<p>Test p1 &lt;p&gt;
		<img src="logo.png" >
	<h2>test title
	<p> test p2 </p>
	<section id="main" ><div><div class="test" ><div>
		<span class="test" ><a id="test4" ></a></span>
		<a href="#" >test 5</a>
		<input type="button" >
		<input type="text" >
	</div></div></div></section>
</body>
>>> div = body.find('div')
>>> div.html()
['<div><div class="test" ><div>\n\t\t<span class="test" ><a id="test4" ></a></span>\n\t\t<a href="#" >test 5</a>\n\t\t<input type="button" >\n\t\t<input type="text" >\n\t</div></div></div>', '<div class="test" ><div>\n\t\t<span class="test" ><a id="test4" ></a></span>\n\t\t<a href="#" >test 5</a>\n\t\t<input type="button" >\n\t\t<input type="text" >\n\t</div></div>', '<div>\n\t\t<span class="test" ><a id="test4" ></a></span>\n\t\t<a href="#" >test 5</a>\n\t\t<input type="button" >\n\t\t<input type="text" >\n\t</div>']
>>> t = body.find('.test')
>>> t.html()
['<div class="test" ><div>\n\t\t<span class="test" ><a id="test4" ></a></span>\n\t\t<a href="#" >test 5</a>\n\t\t<input type="button" >\n\t\t<input type="text" >\n\t</div></div>', '<span class="test" ><a id="test4" ></a></span>']
>>> 
```

```
>>> len(div)
3
>>> len(t)
2
>>> tmp = div + t
>>> len(tmp)
4
>>> tmp.html()
['<div><div class="test" ><div>\n\t\t<span class="test" ><a id="test4" ></a></span>\n\t\t<a href="#" >test 5</a>\n\t\t<input type="button" >\n\t\t<input type="text" >\n\t</div></div></div>', '<div class="test" ><div>\n\t\t<span class="test" ><a id="test4" ></a></span>\n\t\t<a href="#" >test 5</a>\n\t\t<input type="button" >\n\t\t<input type="text" >\n\t</div></div>', '<div>\n\t\t<span class="test" ><a id="test4" ></a></span>\n\t\t<a href="#" >test 5</a>\n\t\t<input type="button" >\n\t\t<input type="text" >\n\t</div>', '<span class="test" ><a id="test4" ></a></span>']
>>> 
```

```
>>> e = body.find('*')
>>> e.name()
['h1', 'p', 'img', 'h2', 'p', 'section', 'div', 'div', 'div', 'span', 'a', 'a', 'input', 'input']
>>> len(e)
14
>>> div = body.find('div')
>>> div.name()
['div', 'div', 'div']
>>> len(div)
3
>>> e -= div
>>> len(e)
11
>>> e.name()
['h1', 'p', 'img', 'h2', 'p', 'section', 'span', 'a', 'a', 'input', 'input']
>>> 
```


## 4. CSS selectors supported by `httt` (14)

| `#`  | Selector pattern | Example | CSS version |
| :--: | :--------------- | :------ | :---------: |
|  1 | `*`                  | `*`               | 2 |
|  2 | `element`            | `p`               | 1 |
|  3 | `#id`                | `#main`           | 1 |
|  4 | `.class`             | `.show`           | 1 |
|  5 | `[attribute]`        | `[href]`          | 2 |
|  6 | `[attribute=value]`  | `[href=#]`        | 2 |
|  7 | `[attribute~=value]` | `[title~=flower]` | 2 |
|  8 | `[attribute^=value]` | `[src^=https]`    | 3 |
|  9 | `[attribute$=value]` | `[src$=.png]`     | 3 |
| 10 | `[attribute*=value]` | `[src*=player]`   | 3 |
|    |                      |                   |   |
| 11 |                      | `div.hide`        |   |
| 12 | `selector selector`  | `div p`           | 1 |
| 13 | `selector>selector`  | `#main > div`     | 2 |
| 14 | `selector,selector`  | `div, a[href]`    | 1 |


## 5. Debug functions for `httt`

+ `httt.p()` <br />
  ```
  def p(o): -> None
  ```
  
  + `o` : *object*
  
  + *return* `None`
  
  Print function for *httt*. 
  Used to print some DEBUG objects of *httt*. 

+ `httt.debug_split_token()` <br />
  ```
  def split_token(raw_html): -> httt_token_host
  ```
  
  + `raw_html` : *str* <br />
    Raw html text
  
  + *return* httt_token_host (object)
  
  Split raw_html text to *httt* **token**s. 
  
  Then you can use `.export()` method for DEBUG: 
  Example: 
  
  ```
  >>> host = httt.debug_split_token('<head><meta charset="utf-8" ><title>hello test</title></head>')
  >>> host
  <httt.html_token_tag_tree.token_host.httt_token_host object at 0x7fb703ef3978>
  >>> e = host.export()
  >>> httt.p(e)
  [
      {
          "name": "head",
          "raw_text": "<head>",
          "type": "tag.start"
      },
      {
          "attr": {
              "charset": "utf-8"
          },
          "name": "meta",
          "raw_text": "<meta charset=\"utf-8\" >",
          "type": "tag.start"
      },
      {
          "name": "title",
          "raw_text": "<title>",
          "type": "tag.start"
      },
      {
          "text": "hello test",
          "type": "text"
      },
      {
          "name": "title",
          "raw_text": "</title>",
          "type": "tag.close"
      },
      {
          "name": "head",
          "raw_text": "</head>",
          "type": "tag.close"
      }
  ]
  >>> 
  ```

+ `httt.debug_build_tree()` <br />
  ```
  def start_build(token_host): -> httt_tree
  ```
  
  + `token_host` : httt_token_host (object)
  
  + *return* httt_tree (object)
  
  Build html tree struct from tokens. 
  
  Example: 
  
  ```
  >>> root = httt.debug_build_tree(host)
  >>> root
  <httt.html_token_tag_tree.tree.httt_tree object at 0x7fb703ef3e48>
  >>> e = root.export()
  >>> httt.p(e)
  {
      "_id": 0,
      "children": [
          {
              "_id": 1,
              "attr": {
                  "charset": "utf-8"
              },
              "index": 0,
              "name": "meta"
          },
          {
              "_id": 2,
              "index": 1,
              "name": "title"
          }
      ],
      "index": 0,
      "name": "head"
  }
  >>> 
  ```

+ `httt.debug_parse_selector()` <br />
  ```
  def parse_selector(raw_text): -> [] dict
  ```
  
  + `raw_text` : *str* <br />
    Raw text of the CSS selector expression
  
  + *return* [] dict
  
  Parse the CSS selector expression. 
  
  Example: 
  
  ```
  >>> s = httt.debug_parse_selector('#main > div.hide, a[target=_blank]')
  >>> httt.p(s)
  [
      [
          {
              "multi": "tree",
              "name": "main",
              "single": "id"
          },
          {
              "multi": "children",
              "name": "div",
              "single": "element"
          },
          {
              "multi": "sub",
              "name": "hide",
              "single": "class"
          }
      ],
      [
          {
              "multi": "tree",
              "name": "a",
              "single": "element"
          },
          {
              "multi": "sub",
              "name": "target",
              "single": "attr",
              "value": "_blank"
          }
      ]
  ]
  >>> 
  ```


<!-- end api.md -->


