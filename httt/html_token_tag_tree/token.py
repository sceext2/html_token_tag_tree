# token.py, httt/html_token_tag_tree/
'''
token class

    object
        httt_token
            httt_token_text
            httt_token_tag
                httt_token_tag_text
                httt_token_tag_attr

'''

# httt token class-es

class httt_token(object):
    '''
    httt token base class
    
    token type:		in text token and tag token
    
    + text		normal text token
    
    NOTE do NOT support zero-length text token, ''
    
    + tag		unknow type tag, <>, such as '<!DOCTYPE >'
    + tag.start		start tag, such as <div>
    + tag.startclose	self-close tag, such as '<br />'
    + tag.close		end tag, such as </div>
    + tag.cdata		CDATA tag, <![CDATA[ ]]>
    + tag.comment	comment tag, <!-- -->
    
    '''
    def __init__(self, host, token_type):
        self.type = None	# (str) token type
        self.index = None	# (int) index of this token in httt_token_host.token_list
        self.host = None	# (object) reference of the httt_token_host object
        
        # NOTE set host and token_type
        self.host = host
        self.type = token_type
        # auto make index and add self to host.token_list
        self.index = len(host.token_list)
        host.token_list.append(self)
    
    def export(self):
        '''
        export this token to dict (JSON) format, used for DEBUG
        
        -> dict {}
        '''
        out = {}
        out['type'] = self.type
        return out
    # end httt_token class

class httt_token_text(httt_token):
    '''
    only for token_type : 'text'
    '''
    def __init__(self, host):
        super().__init__(host, 'text')	# NOTE token type is 'text'
        
        self.text = None	# (str) text of this text token
    
    def get_raw_text(self):
        '''
        get raw text of this token, maybe different from self.text
        
        because of html quote, such as &lt;
        
        -> str
        '''
        return self.host.token_text[self.index]
    
    # overwrite
    def export(self):
        out = super().export()
        out['text'] = self.text
        return out
    # end httt_token_text class

class httt_token_tag(httt_token):
    '''
    for token type : 'tag' and 'tag.*'
    '''
    def __init__(self, host, token_type):
        super().__init__(host, token_type)
        
        self.raw_text = None	# raw text of this tag token
        self.name = None	# name of this tag, only for
        	# token type : 'tag.start', 'tag.startclose', 'tag.close'
        	# other type tag should be None
    
    # overwrite
    def export(self):
        out = super().export()
        out['raw_text'] = self.raw_text
        if self.name != None:
            out['name'] = self.name
        return out
    # end httt_token_tag class

class httt_token_tag_text(httt_token_tag):
    '''
    for tag with inner text, token type : 'tag.comment', 'tag.cdata'
    '''
    def __init__(self, host, token_type):
        super().__init__(host, token_type)
        
        self.text = None	# inner text of this tag
    # overwrite
    def export(self):
        out = super().export()
        out['text'] = self.text
        return out
    # end httt_token_tag_text class

class httt_token_tag_attr(httt_token_tag):
    '''
    tag with attributes, token type : 'tag.start', 'tag.startclose'
    '''
    def __init__(self, host, token_type):
        super().__init__(host, token_type)
        
        self.attr = {}	# attributes of this tag
    
    # overwrite
    def export(self):
        out = super().export()
        if len(self.attr) > 0:
            out['attr'] = self.attr
        return out
    # end httt_token_tag_attr class

# end token.py


