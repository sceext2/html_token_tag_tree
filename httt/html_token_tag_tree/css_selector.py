# css_selector.py, httt/html_token_tag_tree/
# support some CSS selectors for httt

import functools

from . import nodelist
from .selector_grammar import parse_selector

# filter functions

def filter_list(raw_list, worker=lambda x: False):
    out = []
    for i in raw_list:
        if worker(i):
            out.append(i)
    return out

def filter_children(raw_list, worker=lambda x: False):
    out = []
    for node in raw_list:
        one = filter_list(node.children, worker=worker)
        out += one
    return out

def filter_tree(root, worker=lambda x: True, include_root=True):
    out = []
    # filter root first
    if include_root and worker(root):
        out.append(root)
    # filter each sub-tree
    for i in root.children:
        one = filter_tree(i, worker=worker)
        out += one
    return out	# done

# base single selectors

def select_all(node):
    '''
    selector
        *
    '''
    return True

def select_element(node, name):
    '''
    selector eg.
    	a
    '''
    if node.name == name:
        return True
    return False

def select_class(node, name):
    '''
    selector eg.
        .hide
    '''
    if ('class' in node.attr) and (name in node.attr['class'].split(' ')):
        return True
    return False

def select_id(node, name):
    '''
    selector eg.
        #main
    '''
    if ('id' in node.attr) and (name == node.attr['id']):
        return True
    return False

def select_attr(node, name, value=None):
    '''
    selector eg.
        a[href]
        input[type=text]
    '''
    if not name in node.attr:
        return False
    if value == None:
        return True
    if value == node.attr[name]:
        return True
    return False

# execute CSS select process

def do_one_select(raw_set, action, tree_include_root=False):
    '''
    
    NOTE default not include tree root
    
    NOTE action
        {
            'multi' : '', 	# can be 'tree', 'children', 'sub'
            'single' : '', 	# can be 'all', 'element', 'class', 'id', 'attr'
            'name' : '', 	# str or empty
            'value' : '', 	# str or empty
        }
    '''
    # make worker for single
    single = action['single']
    if single == 'element':
        worker = functools.partial(select_element, name=action['name'])
    elif single == 'class':
        worker = functools.partial(select_class, name=action['name'])
    elif single == 'id':
        worker = functools.partial(select_id, name=action['name'])
    elif single == 'attr':
        value = None
        if 'value' in action:
            value = action['value']
        worker = functools.partial(select_attr, name=action['name'], value=value)
    else:	# single == 'all'
        worker = functools.partial(select_all)
    # do select with filter for multi
    multi = action['multi']
    if multi == 'sub':
        out = filter_list(raw_set, worker=worker)
    elif multi == 'children':
        out = filter_children(raw_set, worker=worker)
    else:	# multi == 'tree'
        out = []
        for i in raw_set:
            one = filter_tree(i, worker=worker, include_root=tree_include_root)
            out += one
    return out	# done

def do_select(raw_set, actions):
    # loop to do each select
    for i in actions:
        raw_set = do_one_select(raw_set, i)
        # clean select after each action
        raw_set = nodelist.join_with_tree_id([raw_set])
    return raw_set	# done

# css selector entry function
def css_select(root, selector):
    '''
        root		httt_tree (object)
        selector	(str) CSS selector
    
    -> httt_nodelist (object)
    '''
    raw_set = [root]
    actions = parse_selector(selector)
    # do each multi.add select
    raw_out = []
    for a in actions:
        raw_out.append(do_select(raw_set, a))
    # join set
    out = nodelist.join_with_tree_id(raw_out)
    out = nodelist.httt_nodelist(out)
    return out	# done

# end css_selector.py


