#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# __init__.py, httt/, httt : html_token_tag_tree entry file
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

import json

from .html_token_tag_tree import (
    entry, 
    split_token, 
    build_tree, 
    selector_grammar, 
)

# httt entry function
create_tree = entry.create_tree

# other exports functions
get_text_between = entry.get_text_between

# for DEBUG
debug_split_token = split_token.split_token
debug_build_tree = build_tree.start_build
debug_parse_selector = selector_grammar.parse_selector

# for DEBUG print
def p(o):
    print(json.dumps(o, indent=4, sort_keys=True, ensure_ascii=False))

# end __init__.py


