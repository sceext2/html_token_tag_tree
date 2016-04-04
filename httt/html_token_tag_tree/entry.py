# -*- coding: utf-8 -*-
# entry.py, httt/html_token_tag_tree/
# httt entry file
#
#    html_token_tag_tree : A simple read-only html static parse library. 
#    Copyright (C) 2016  sceext <sceext@foxmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
'''
httt : html_token_tag_tree

version 0.1.1.1 test201604041718

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


