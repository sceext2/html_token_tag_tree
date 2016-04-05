<!-- css_selector.md, httt/doc/
   -
  -->

# CSS selector examples of httt


## 1. single CSS selector

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

## 2. combination selector

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

## 3. Complex example

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


TODO
<!-- end css_selector.md -->


