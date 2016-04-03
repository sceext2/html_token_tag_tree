# -*- coding: utf-8 -*-
# entry.py, httt/html_token_tag_tree/
# httt entry file
'''
httt : html_token_tag_tree

version 0.1.0.0 test201604032257

'''

from . import build_tree
from .split_token import split_token

# httt entry function
def create_tree(html_text):
    '''
    parse raw html text (str)
    
    -> httt_tree (object)
    '''
    # split token first
    host = split_token(html_text)
    # build tree next
    root = build_tree.start_build(host)
    
    return root	# done

# convenient methods

def get_text_between(tag_a, tag_b):
    '''
    get text between two tags
    
        tag_a, tag_b	httt_token_tag
    
    -> [] (str)
    '''
    host = tag_a.host
    start_index = tag_a.index
    end_index = tag_b.index
    
    out = []
    for i in host.token_list[start_index:end_index]:
        if i.type == 'text':
            out.append(i.text)
    return out

# end entry.py


