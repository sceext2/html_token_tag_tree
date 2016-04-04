# tree.py, httt/html_token_tag_tree/

from . import css_selector

class httt_tree(object):
    '''
    html node (element) object
    '''
    def __init__(self):
        
        self._start_tag = None	# (object/httt_token_tag_attr) start tag (token) of this node
        self._close_tag = None	# (object/httt_token_tag) close tag (token) of this node
        self._before_close = None	# (object/httt_token_tag)
        	# NOTE if there is no close_tag, the close_tag should be None, 
        	# and set before_close (tag)
        
        self.parent = None	# (object/httt_tree) parent node of this node, None for root node
        self.children = []	# (object/httt_tree) chlid node list of this node
        self.index = 0		# (int) index of this node in parent.children list
        
        self.name = None	# name of this node (start tag name)
        self.attr = {}		# attributes of this node (start tag)
        
        self._id = None	# (int) id of this node is the whole html document tree
        	# the value should be self.start_tag.index
    
    # private methods
    def _set_parent(self, parent):
        self.parent = parent
        # auto gen index and add to parent
        self.index = len(parent.children)
        parent.children.append(self)
    
    def _set_start_tag(self, tag):
        self._start_tag = tag
        self._id = tag.index
        # set name and attr
        self.name = tag.name
        if hasattr(tag, 'attr'):
            self.attr = tag.attr
    
    # stortcut for read .parent and .children
    @property
    def c(self):
        return self.children
    @property
    def p(self):
        return self.parent
    
    # tree methods
    
    def html(self):
        '''
        get raw html text of this node
        
        -> str
        '''
        # get inner_html first
        raw = self.inner_html()
        # get start_tag text
        host = self._start_tag.host
        start = host.token_text[self._start_tag.index]
        # get close_tag text, NOTE check selfclose tag
        close = ''
        if (self._close_tag != None) and (self._close_tag != self._start_tag):
            close = host.token_text[self._close_tag.index]
        out = start + raw + close
        return out	# done
    
    def inner_html(self):
        '''
        raw inner html text of this node (not include start/close tag)
        
        -> str
        '''
        # get token index info
        host = self._start_tag.host
        start_index = self._start_tag.index + 1
        if self._close_tag == None:
            end_index = self._before_close.index + 1
        else:
            end_index = self._close_tag.index
        # get raw token text
        raw = host.token_text[start_index:end_index]
        
        out = ('').join(raw)
        return out	# done
    
    def text(self):
        '''
        get text list in this node
        
        -> list []
        '''
        # get token index info
        host = self._start_tag.host
        start_index = self._start_tag.index
        if self._close_tag == None:
            end_index = self._before_close.index
        else:
            end_index = self._close_tag.index
        # get raw token object list
        raw_list = host.token_list[start_index:end_index + 1]
        # just output text token
        out = []
        for i in raw_list:
            if i.type == 'text':
                out.append(i.text)
        return out	# done
    
    # for DEBUG, TODO not output raw token (tag) info, TODO not include text token info
    def export(self):
        '''
        export html tree info to list (dict) (JSON) info, used for DEBUG
        '''
        # export this node info
        out = {}
        out['_id'] = self._id
        out['name'] = self.name
        out['index'] = self.index
        if len(self.attr) > 0:
            out['attr'] = self.attr
        # export children node info
        if len(self.children) > 0:
            out['children'] = [c.export() for c in self.children]
        return out	# export done
    
    # for traverse tree
    
    def _get_sibling(self, index_delta=0):
        p, i = self.parent, self.index
        if p == None:
            return None
        i += index_delta
        if (i >= 0) and (i < len(p.children)):
            return p.children[i]
        return None
    
    def prev(self):
        '''
        get previous sibling
        
        -> httt_tree or None
        '''
        return self._get_sibling(-1)
    def next(self):
        '''
        get next sibling
        
        -> httt_tree or None
        '''
        return self._get_sibling(1)
    
    # NOTE important function, select sub-node with CSS selector
    def find(self, selector):
        '''
        
        -> httt_nodelist object, []
        '''
        return css_selector.css_select(self, selector)
    # end httt_tree class

# end tree.py


