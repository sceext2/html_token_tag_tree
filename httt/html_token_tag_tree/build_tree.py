# build_tree.py, httt/html_token_tag_tree/

from . import tag_host
from .tree import httt_tree

# base build functions

def filter_tag_token(raw_list):
    '''
    only keep tag needed by build_tree, ignore all other tag (token) types
    only keey tag type: 
    
    + tag.start
    + tag.startclose
    + tag.close
    
    -> [] httt_token_tag (object)
    '''
    out = []
    for i in raw_list:
        if i.type in ['tag.start', 'tag.startclose', 'tag.close']:
            out.append(i)
    return out

# base build actions

def do_add_selfclose_tag(bci, tag):
    # create tree (node)
    tree = httt_tree()
    tree._set_start_tag(tag)
    # add to parent
    tree._set_parent(bci.path[-1])
    # set close tag
    tree._close_tag = tag
    # done
    return tree

def do_add_start_tag(bci, tag):
    tree = httt_tree()
    tree._set_start_tag(tag)
    tree._set_parent(bci.path[-1])
    # add tree to path
    bci.path.append(tree)
    # done
    return tree

def check_conflict(bci, tag):
    '''
    check all tags on current path
    return first conflict
    
    -> tag_name (str) or None
    '''
    conflict = bci.tag.get(tag.name).conflict
    for i in range(len(bci.path) - 1, -1, -1):
        one = bci.path[i]
        if one.name in conflict:
            return one.name
    return None

def get_before_close(tag):
    token_index = tag.index - 1
    before = tag.host.token_list[token_index]
    return before

def _do_close_tag(bci, tag, match=False):
    # to close top tree on current path
    top = bci.path[-1]
    if match:
        top._close_tag = tag
    else:
        top._before_close = get_before_close(tag)
    # remove from path
    return bci.path.pop()	# done

def close_tag(bci, tag_name, tag, match=False):
    '''
    close tag by tag_name on current path
    
        tag		the tag.close to close tag_name
    
        match	if match is False, will get before_close token from tag
    
    -> True if close error, else False
    '''
    # check tag_name on current path
    to_close_tree = None
    for i in range(len(bci.path) - 1, -1, -1):
        one = bci.path[i]
        if one.name == tag_name:
            to_close_tree = one
            to_close_i = i	# NOTE save tree index here
            break
    if to_close_tree == None:
        return True	# close failed
    # check close root tag
    if to_close_tree == bci.root:
        if len(bci.rest) > 0:
            # can NOT close root here
            return True	# should close root after (at) last tag
    # check level
    current_level = bci.tag.get(tag.name).level
    to_check_list = bci.path[to_close_i + 1:]
    for i in to_check_list:
        one_level = bci.tag.get(i.name).level
        if one_level >= current_level:
            # found high level, can NOT close
            return True
    # all checks passed, close after tags
    for i in range(len(bci.path) - 1, to_close_i, -1):
        _do_close_tag(bci, tag)
    # close current tag
    _do_close_tag(bci, tag, match=True)
    # close done

# Build tree Control Info (bci)
class build_control_info(object):
    '''
    '''
    def __init__(self):
        self.path = []	# httt_tree (object)
        	# node list on current path, such as html/body/div/span
        self.token = None	# httt_token_host (object)
        self.tag = None		# httt_tag_host (object)
        
        self.rest = []		# httt_token_tag (object) rest tags (token)
        self.root = None	# httt_tree (object) root node of this document
    # end build_control_info (bci) class

# core build functions

def _build_one_tag(bci, tag):
    # get tag info
    ti = bci.tag.get(tag.name)
    # check tag_type
    to_fix_tag_type = {
        'tag.start' : 'start', 
        'tag.startclose' : 'startclose', 
        'tag.close' : 'close', 
    }
    fix_tag_type = to_fix_tag_type[tag.type]
    
    if ti.type == 'selfclose':
        if fix_tag_type == 'start':
            fix_tag_type = 'startclose'
        elif fix_tag_type == 'close':
            if bci.tag.selfclose_close_tag == 'ignore':
                return	# NOTE ignore this tag
            fix_tag_type = 'startclose'
    elif ti.type == 'struct':
        if fix_tag_type == 'startclose':
            fix_tag_type = 'start'
    # process tag types
    if fix_tag_type == 'startclose':
        tree = do_add_selfclose_tag(bci, tag)
    elif fix_tag_type == 'start':
        # check this tag is in conflict tag
        conflict_tag_name = check_conflict(bci, tag)
        if conflict_tag_name != None:
            # try to close tags
            close_tag(bci, conflict_tag_name, tag)
        # normal start tag process
        tree = do_add_start_tag(bci, tag)
    else:	# fix_tag_type == 'close'
        tree = None
        # try to close it
        if close_tag(bci, tag.name, tag, match=True):
            # close failed
            if bci.tag.isolate_struct_close_tag == 'selfclose':
                # add this tag as selfclose tag
                do_add_selfclose_tag(bci, tag)
    # done
    return tree

def _build_mainloop(bci):
    # process each tag
    while len(bci.rest) > 0:
        one = bci.rest[0]
        bci.rest = bci.rest[1:]
        
        _build_one_tag(bci, one)
    # done

def _do_build(token_host):
    '''
    
    -> bci (build_control_info)
    '''
    # create bci
    bci = build_control_info()
    bci.token = token_host
    # load rule
    bci.tag = tag_host.load_config()
    
    # filter tag tokens
    bci.rest = filter_tag_token(bci.token.token_list)
    last_tag = bci.rest[-1]	# NOTE save last_tag here
    # check has tags
    if len(bci.rest) < 1:
        return bci	# nothing to do
    # set first tag to root tree
    first = bci.rest[0]
    bci.rest = bci.rest[1:]
    bci.root = httt_tree()
    bci.root._set_start_tag(first)
    # add root to path
    bci.path.append(bci.root)
    
    # start build main loop
    _build_mainloop(bci)
    
    # check and close all tags after end of the document
    while len(bci.path) > 0:
        # NOTE just set before_close here
        _do_close_tag(bci, last_tag)
    return bci	# done

# build tree entry function
def start_build(token_host):
    bci = _do_build(token_host)
    # just return root tree
    return bci.root

# end build_tree.py


