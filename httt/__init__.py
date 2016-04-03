#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# __init__.py, httt/, httt : html_token_tag_tree entry file

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


