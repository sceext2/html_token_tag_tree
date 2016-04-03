# token_host.py, httt/html_token_tag_tree/

class httt_token_host(object):
    '''
    '''
    
    def __init__(self):
        self.raw_html = None	# raw html text (str)
        self.token_text = []	# raw token text
        self.token_list = []	# token object list
    
    def export(self):
        '''
        export token_list (with token_text) to list (dict) (JSON)
        format, used for DEBUG
        
        -> list []
        '''
        out = [t.export() for t in self.token_list]
        return out
    # end httt_token_host class

# end token_host.py


