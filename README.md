<!-- README.md, httt/
   - html_token_tag_tree
   - https://github.com/sceext2/html_token_tag_tree
  -->

# html_token_tag_tree
A simple read-only html static parse library. 
(`httt version 0.1.3.1 test201604061445`)

**html_token_tag_tree** (*httt*) use a simple method to parse html and
build the html tree struct. 
Then you can traverse the tree and get information. 


## Features

+ Traverse the tree with a very simple API. 

+ Support 14 useful CSS (1, 2, 3) selectors! 

+ Pure python3 (*tested on python 3.5.1*), without dependencies. 
  *httt* only use the python standard library. 

+ Output **raw** html text. 

**NOTE**

This library can only parse html and get info from it. 
There is no functions to edit the html tree. 


## Usage (API)

(Full API document of *httt* please see 
[`doc/api.md`](https://github.com/sceext2/html_token_tag_tree/blob/master/doc/api.md). )

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

+ **1. import *httt* and raw_html text**

```
$ python
Python 3.5.1 (default, Mar  3 2016, 09:29:07) 
[GCC 5.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import httt
>>> httt.version
'httt version 0.1.3.0 test201604051914'
>>> with open('test/t1.html') as f:
...     raw_html = f.read()
... 
>>> 
```

+ **2. parse html and create html tree**

```
>>> root = httt.create_tree(raw_html)
>>> root
<httt.html_token_tag_tree.tree.httt_tree object at 0x7f98c3313780>
>>> 
```

+ **3. traverse tree and get info**

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


### CSS selector support

*httt* support these CSS selectors: (14)

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


### Some examples

```
>>> script = root.find('script')
>>> len(script)
1
>>> script.html()
['<script type="text/javascript" >\n\tconsole.log(\'hello, world! \');\n</script>']
>>> script[0].name
'script'
>>> s = script[0]
>>> s.text()
["\n\tconsole.log('hello, world! ');\n"]
>>> s.attr['type']
'text/javascript'
>>> 
```

```
>>> e = root.find('#test4')[0]
>>> e.html()
'<a id="test4" ></a>'
>>> 
>>> root.find('#main div.test > * a[href], input[type=text]').html()
['<a href="#" >test 5</a>', '<input type="text" >']
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


