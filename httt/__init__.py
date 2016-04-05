#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# __init__.py, httt/, httt : html_token_tag_tree entry file
# https://github.com/sceext2/html_token_tag_tree
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

import json as _json

from .html_token_tag_tree import entry as _entry
from .html_token_tag_tree import split_token as _split_token
from .html_token_tag_tree import build_tree as _build_tree
from .html_token_tag_tree import selector_grammar as _selector_grammar
from .html_token_tag_tree import version as _version

# httt entry function
create_tree = _entry.create_tree

# exports attributes
version = _version.httt_version

# other exports functions
get_text_between = _entry.get_text_between
clean_html_text = _entry.clean_html_text

# for DEBUG
debug_split_token = _split_token.split_token
debug_build_tree = _build_tree.start_build
debug_parse_selector = _selector_grammar.parse_selector

# for DEBUG print
def p(o):
    print(_json.dumps(o, indent=4, sort_keys=True, ensure_ascii=False))

# end __init__.py


