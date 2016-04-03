# tree_rule.py, httt/html_token_tag_tree/rule/
# configurable rules to build html tree, default tree_rule for httt

rule_set = {
    ## define tag set
    'force_selfclose_tag' : [
        'meta', 	# 定义关于 HTML 文档的元信息
        'link', 	# 定义文档与外部资源的关系
        
        'br', 		# 定义简单的折行
        'hr', 		# 定义水平线
        'wbr', 		# 规定在文本中的何处适合添加换行符
        
        'img', 		# 定义图像
        'input', 	# 定义一个输入控件
        
        # force close
        'acronym', 	# HTML5不再支持 定义只取首字母的缩写
        'applet', 	# HTML5不再支持 HTML 4.01 已废弃 定义嵌入的 applet
        'basefont', 	# HTML5不再支持 HTML 4.01 已废弃 定义页面中文本的默认字体 颜色或尺寸
        'dir', 		# HTML5不再支持 HTML 4.01 已废弃 定义目录列表
        'frame', 	# HTML5不再支持 定义框架集的窗口或框架
        'frameset', 	# HTML5不再支持 定义框架集
        'noframes', 	# HTML5不再支持 定义针对不支持框架的用户的替代内容
        'tt', 		# HTML5不再支持 定义打字机文本
        
        'center', 	# HTML5不再支持 HTML 4.01 已废弃 定义居中文本
        'strike', 	# HTML5不再支持 HTML 4.01 已废弃 定义加删除线的文本
        
        'base', 	# 定义页面中所有链接的默认地址或默认目标
        'param', 	# 定义对象的参数
        'menu', 	# 定义菜单列表
        
        # 表单
        'select', 	# 定义选择列表 下拉列表
        'optgroup', 	# 定义选择列表中相关选项的组合
        'option', 	# 定义选择列表中的选项
        'label', 	# 定义 input 元素的标注
        'fieldset', 	# 定义围绕表单中元素的边框
        'legend', 	# 定义 fieldset 元素的标题
        
        # 表格
        'col', 		# 定义表格中一个或多个列的属性值
        'colgroup', 	# 定义表格中供格式化的列组
        # 图像
        'map', 		# 定义图像映射
        'area', 	# 定义图像地图内部的区域
        
        # Audio/Video
        'source', 	# New 定义media元素 <video> 和 <audio> 的媒体资源
        'track', 	# New 为媒体 <video> 和 <audio> 元素定义外部文本轨道
        
        'command', 	# New 定义用户可能调用的命令 比如单选按钮 复选框或按钮
        'datalist', 	# New 规定了 input 元素可能的选项列表
        'details', 	# New 定义了用户可见的或者隐藏的需求的补充细节
        'dialog', 	# New 定义一个对话框或者窗口
        'embed', 	# New 定义了一个容器 用来嵌入外部应用或者互动程序 插件
        'figcaption', 	# New 定义一个 caption for a <figure> element
        'keygen', 	# New 规定用于表单的密钥对生成器字段
        'output', 	# New 定义一个计算的结果
        'progress', 	# New 定义运行中的任务进度 进程
        'summary', 	# New 定义一个可见的标题 当用户点击标题时会显示出详细信息
    ], 
    
    'force_struct_tag' : [
        # level 19000
        'script', 	# 定义客户端脚本
        'style', 	# 定义文档的样式信息
        'pre', 		# 定义预格式文本
        
        # level 9000
        'html', 	# 定义一个 HTML 文档
        # level 8500
        'head', 	# 定义关于文档的信息
        'body', 	# 定义文档的主体
        # level 8000
        'title', 	# 为文档定义一个标题
        
        # level 4000
        'div', 		# 定义文档中的节
        'noscript', 	# 定义针对不支持客户端脚本的用户的替代内容
        
        'nav', 		# New 定义导航链接
        'header', 	# New 定义一个文档头部部分
        'footer', 	# New 定义一个文档底部
        'section', 	# New 定义了文档的某个区域
        'article', 	# New 定义一个文章内容
        'aside', 	# New 定义其所处内容之外的内容
        
        # level 2300
        'table', 	# 定义一个表格
        
        'ul', 	# 定义一个无序列表
        'ol', 	# 定义一个有序列表
        'dl', 	# 定义一个定义列表
        
        # level 2200
        'tbody', 	# 定义表格中的主体内容
        'thead', 	# 定义表格中的表头内容
        'tfoot', 	# 定义表格中的表注内容 脚注
        # level 2100
        'tr', 	# 定义表格中的行
        'dt', 	# 定义一个定义定义列表中的项目
        
        # level 2000
        'th', 	# 定义表格中的表头单元格
        'td', 	# 定义表格中的单元
        
        'li', 	# 定义一个列表项
        'dd', 	# 定义定义列表中项目的描述
        
        'iframe', 	# 定义内联框架
        'form', 	# 定义一个 HTML 表单 用于用户输入
        'textarea', 	# 定义多行的文本输入控件
        
        # level 1900
        'span', 	# 定义文档中的节
    ], 
    
    ## define tag level
    'tag_level' : {
        # force struct tags
        19000 : [
            'script', 	# 定义客户端脚本
            'style', 	# 定义文档的样式信息
            'pre', 	# 定义预格式文本
        ], 
        9000 : [
            'html', 	# 定义一个 HTML 文档
        ], 
        8500 : [
            'head', 	# 定义关于文档的信息
            'body', 	# 定义文档的主体
        ], 
        8000 : [
            'title', 	# 为文档定义一个标题
        ], 
        4000 : [
            'noscript', # 定义针对不支持客户端脚本的用户的替代内容
            'div', 	# 定义文档中的节
            
            'nav', 	# New 定义导航链接
            'header', 	# New 定义一个文档头部部分
            'footer', 	# New 定义一个文档底部
            'section', 	# New 定义了文档的某个区域
            'article', 	# New 定义一个文章内容
            'aside', 	# New 定义其所处内容之外的内容
        ], 
        2300 : [
            'table', 	# 定义一个表格
            
            'ul', 	# 定义一个无序列表
            'ol', 	# 定义一个有序列表
            'dl', 	# 定义一个定义列表
        ], 
        2200 : [
            'tbody', 	# 定义表格中的主体内容
            'thead', 	# 定义表格中的表头内容
            'tfoot', 	# 定义表格中的表注内容 脚注
        ], 
        2100 : [
            'tr', 	# 定义表格中的行
            'dt', 	# 定义一个定义定义列表中的项目
        ], 
        2000 : [
            'th', 	# 定义表格中的表头单元格
            'td', 	# 定义表格中的单元
            
            'li', 	# 定义一个列表项
            'dd', 	# 定义定义列表中项目的描述
            
            'iframe', 	# 定义内联框架
            'form', 	# 定义一个 HTML 表单 用于用户输入
            'textarea', # 定义多行的文本输入控件
        ], 
        1900 : [
            'span', 	# 定义文档中的节
        ], 
        
        # normal tags
        # NOTE known tag base level 1000
        1500 : [
            'object', 	# 定义嵌入的对象
            'audio', 	# New 定义声音 比如音乐或其他音频流
            'video', 	# New 定义一个音频或者视频
            'canvas', 	# New 通过脚本 通常是 JavaScript 来绘制图形 比如图表和其他图像
            'figure', 	# New figure 标签用于对元素进行组合
        ], 
        # low level normal tag
        1100 : [
            'h1', 	# 定义 HTML 标题
            'h2', 
            'h3', 
            'h4', 
            'h5', 
            'h6', 
            'p', 	# 定义一个段落
            'address', 	# 定义文档作者或拥有者的联系信息
        ], 
        1060 : [
            'a', 	# 定义一个链接
        ], 
        # low low level normal tag
        1050 : [
            'big', 	# HTML5不再支持 定义大号文本
            'font', 	# HTML5不再支持 HTML 4.01 已废弃 定义文本的字体 尺寸和颜色
            
            'abbr', 	# 定义一个缩写
            'b', 	# 定义粗体文本
            'bdi', 	# 允许您设置一段文本 使其脱离其父元素的文本方向设置
            'bdo', 	# 定义文本的方向
            'blockquote', 	# 定义块引用
            'button', 	# 定义按钮
            'caption', 	# 定义表格标题
            'cite', 	# 定义引用 (citation)
            'code', 	# 定义计算机代码文本
            'del', 	# 定义被删除文本
            'dfn', 	# 定义定义项目
            'em', 	# 定义强调文本
            'i', 	# 定义斜体文本
            'ins', 	# 定义被插入文本
            'kbd', 	# 定义键盘文本
            'mark', 	# 定义带有记号的文本
            'q', 	# 定义短的引用
            'ruby', 	# 定义 ruby 注释 中文注音或字符
            's', 	# 定义加删除线的文本
            'samp', 	# 定义计算机代码样本
            'small', 	# 定义小号文本
            'strong', 	# 定义语气更为强烈的强调文本
            'sub', 	# 定义下标文本
            'sup', 	# 定义上标文本
            'u', 	# 定义下划线文本
            'var', 	# 定义文本的变量部分
            
            'meter', 	# New 定义度量衡 仅用于已知最大和最小值的度量
            'rp', 	# New 定义不支持 ruby 元素的浏览器所显示的内容
            'rt', 	# New 定义字符 中文注音或字符 的解释或发音
            'time', 	# New 定义一个日期/时间
        ], 
    }, 
    
    ## define conflict tag groups, all tags in one conflict group can not be nested
    'conflict_group' : [
        [	# conflict group 1
            'h1', 	# 定义 HTML 标题
            'h2', 
            'h3', 
            'h4', 
            'h5', 
            'h6', 
            
            'p', 	# 定义一个段落
        ], 
        [	# conflict group 2
            'form', 	# 定义一个 HTML 表单 用于用户输入
        ], 
    ], 
    
    ## define special tag
    'tag' : {	# TODO
    }, 
    
    ## special rules and default rules
    
    # process self-close tag.close, such as </br>; can be 'selfclose', 'ignore'
    'selfclose_close_tag' : 'selfclose', 
    # process isolate struct tag.close (no match tag.start); can be 'selfclose', 'ignore'
    'isolate_struct_close_tag' : 'ignore', 
    
    # default_tag_level (int)
    'default_tag_level' : 0, 
    # tag_type can be None (normal), 'selfclose' (force), 'struct' (force)
    'unknow_tag_type' : 'selfclose', 
}

# end tree_rule.py


