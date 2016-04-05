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

https://github.com/sceext2/html_token_tag_tree
'''

import re

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

def clean_html_text(raw, strip=False):
    '''
    clean raw text token with html text rules
    
    replace \n \t etc. to ' ' (space), etc. 
    
        raw	str or list ([] str)
    
    -> str or [] str
    '''
    if isinstance(raw, str):
        out = _clean_one_html_text(raw)
        if strip:
            out = out.strip()
        return out
    out = [_clean_one_html_text(i) for i in raw]
    if strip:
        out = _strip_html_text(out)
    return out

def _clean_one_html_text(raw):
    # replace chars to ' ' space (\r, \n, tab)
    out = raw.replace('\r', '\n').replace('\n', ' ').replace('\t', ' ')
    # NOTE replace Chinese ' ' big space to space
    out = out.replace('　', ' ')
    # replace multi spaces to only one space
    out = (' ').join(re.split(' +', out))
    return out	# clean done

def _strip_html_text(raw):
    out = []
    for i in raw:
        one = i.strip()
        if one != '':
            out.append(one)
    return out

# end entry.py


