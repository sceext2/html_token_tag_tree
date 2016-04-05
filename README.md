<!-- README.md, httt/
   - html_token_tag_tree
   - https://github.com/sceext2/html_token_tag_tree
  -->

# html_token_tag_tree
A simple read-only html static parse library. 
(`version 0.1.2.0 test201604042203`)

**html_token_tag_tree** (*httt*) use a simple method to parse html and
build the html tree struct. 
Then you can traverse the tree and get information. 


## Features

+ Traverse the tree with a very simple API. 

+ Simple CSS Selector support. 

+ Pure python3 (*tested on python 3.5.1*), without dependencies. 
  *httt* only use the python standard library. 

+ Output **raw** html text. 

**NOTE**

This library can only parse html and get info from it. 
There is no functions to edit the html tree. 


## Usage (API)

The following examples will use this html text: (*test/t1.html*)

> ```
> <!DOCTYPE html>
> <html>
> <head>
> 	<meta charset="utf-8" >
> <!-- a simple test page for html_token_tag_tree -->
> 	<link rel="stylesheet" type="text/css" href="main.css" >
> 	<title>simple test page</title>
> <style type="text/css" >
> body	{
> 	background-color: #000;
> }
> </style>
> <script type="text/javascript" >
> 	console.log('hello, world! ');
> </script>
> </head>
> <body>
> 	<h1>Hello, world !
> 	<p>Test p1 &lt;p&gt;
> 		<img src="logo.png" >
> 	<h2>test title
> 	<p> test p2 </p>
> 	<section id="main" ><div><div class="test" ><div>
> 		<span class="test" ><a id="test4" ></a></span>
> 		<a href="#" >test 5</a>
> 		<input type="button" >
> 		<input type="text" >
> 	</div></div></div></section>
> </body>
> </html>
> ```

### 1. import *httt* and raw_html text

```
$ python
Python 3.5.1 (default, Mar  3 2016, 09:29:07) 
[GCC 5.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import httt
>>> with open('test/t1.html') as f:
...     raw_html = f.read()
... 
>>> 
```

### 2. parse html and create html tree

```
>>> root = httt.create_tree(raw_html)
>>> root
<httt.html_token_tag_tree.tree.httt_tree object at 0x7f2cb008a080>
>>> 
```

### 3. traverse tree and get info

Use `.children` (or `.c`) and `.parent` (or `.p`)

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
>>> head = root.c[0]
>>> head.name
'head'
>>> head.parent.name
'html'
>>> head.p == head.parent
True
>>> 
```

```
>>> head.c[0].name
'meta'
>>> meta = head.c[0]
>>> meta.html()
'<meta charset="utf-8" >'
>>> meta.attr['charset']
'utf-8'
>>> 
```

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

### 4. CSS Selector

```
>>> script = root.find('script')
>>> script
[<httt.html_token_tag_tree.tree.httt_tree object at 0x7f2cb008ec50>]
>>> len(script)
1
>>> s = script[0]
>>> s
<httt.html_token_tag_tree.tree.httt_tree object at 0x7f2cb008ec50>
>>> s.html()
'<script type="text/javascript" >\n\tconsole.log(\'hello, world! \');\n</script>'
>>> s.inner_html()
"\n\tconsole.log('hello, world! ');\n"
>>> s.text()
["\n\tconsole.log('hello, world! ');\n"]
>>> s.attr['type']
'text/javascript'
>>> 
```

#### 4.1. single CSS selector

+ **1. `*`**
  
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
  >>> e = head.find('*')
  >>> len(e)
  6
  >>> e[0].name
  'head'
  >>> e[-1].name
  'script'
  >>> e[-2].name
  'style'
  >>> 
  ```

+ **2. `element`**
  
  ```
  >>> link = head.find('link')
  >>> len(link)
  1
  >>> link[0].html()
  '<link rel="stylesheet" type="text/css" href="main.css" >'
  >>> 
  ```

+ **3. `#id`**
  
  ```
  >>> e = root.find('#test4')
  >>> len(e)
  1
  >>> e[0].html()
  '<a id="test4" ></a>'
  >>> 
  ```

+ **4. `.class`**
  
  ```
  >>> e = root.find('.test')
  >>> len(e)
  2
  >>> e[0].html()
  '<div class="test" ><div>\n\t\t<span class="test" ><a id="test4" ></a></span>\n\t\t<a href="#" >test 5</a>\n\t\t<input type="button" >\n\t\t<input type="text" >\n\t</div></div>'
  >>> e[1].html()
  '<span class="test" ><a id="test4" ></a></span>'
  >>> 
  ```

+ **5. `[attribute]` `[attribute=value]`**
  
  ```
  >>> a = root.find('a[href]')
  >>> len(a)
  1
  >>> a[0].html()
  '<a href="#" >test 5</a>'
  >>> i = root.find('input[type=text]')
  >>> len(i)
  1
  >>> i[0].html()
  '<input type="text" >'
  >>> 
  ```

#### 4.2. combination selector

+ **1. `element element`**
  
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
  >>> a = body.find('span a')
  >>> len(a)
  1
  >>> a[0].html()
  '<a id="test4" ></a>'
  >>> 
  ```

+ **2. `element>element`**
  
  ```
  >>> div = body.find('#main > div')
  >>> len(div)
  1
  >>> div[0].html()
  '<div><div class="test" ><div>\n\t\t<span class="test" ><a id="test4" ></a></span>\n\t\t<a href="#" >test 5</a>\n\t\t<input type="button" >\n\t\t<input type="text" >\n\t</div></div></div>'
  >>> 
  ```

+ **3. `element,element`**
  
  ```
  >>> e = body.find('a, input')
  >>> len(e)
  4
  >>> e[0].html()
  '<a id="test4" ></a>'
  >>> e[-1].html()
  '<input type="text" >'
  >>> 
  ```

+ **4. ` `**
  
  ```
  >>> len(body.find('div'))
  3
  >>> len(body.find('.test'))
  2
  >>> e = body.find('div.test')
  >>> len(e)
  1
  >>> e[0].html()
  '<div class="test" ><div>\n\t\t<span class="test" ><a id="test4" ></a></span>\n\t\t<a href="#" >test 5</a>\n\t\t<input type="button" >\n\t\t<input type="text" >\n\t</div></div>'
  >>> 
  ```

#### 4.3. a complex example

```
>>> e = root.find('#main div.test > * a[href], input[type=text]')
>>> len(e)
2
>>> e[0].html()
'<a href="#" >test 5</a>'
>>> e[1].html()
'<input type="text" >'
>>> 
```


## LICENSE

**GNU LGPLv3+**

(*GNU Lesser General Public License* either *version 3* of the License, 
or *(at your option)* any later version)

```
    html_token_tag_tree : A simple read-only html static parse library. 
    Copyright (C) 2016  sceext <sceext@foxmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
```


<!-- end README.md -->


