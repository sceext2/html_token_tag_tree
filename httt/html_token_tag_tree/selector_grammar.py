# selector_grammar.py, httt/html_token_tag_tree/
# parse css selector (text) for httt
'''

TODO support quote " in css selector text

supported css selectors

    [selector name]	[eg.]

    single.all		*
    single.element	a
    single.class	.hide
    single.id		#main
    single.attr		[href] [type=text]
    
    multi.tree		a img
    multi.children	a > img
    multi.add		a, img
    multi.sub		div.hide.test#a.b#c

css action arg (eg.)
    {
    	'multi' : 'tree', 
    	'single' : 'attr', 
        'name' : 'type', 
        'value' : 'text', 
    }

'''

# parse single selectors

def _parse_single_attr(raw_text):
    raw = raw_text.strip()
    if raw == '':
        return
    if raw[0] == '[':
        raw = raw[1:]
    if raw[-1] == ']':
        raw = raw[:-1]
    out = {
        'name' : '', 
    }
    raw = raw.strip()
    if raw == '':
        return out
    if not '=' in raw:
        out['name'] = raw
        return out
    out['name'], out['value'] = raw.split('=')
    return out

def _parse_single(raw_text):
    raw = raw_text.strip()
    if raw == '':
        return
    # check raw_text type
    if raw == '*':
        out = {
            'single' : 'all', 
        }
    elif raw[0] == '#':
        name = raw[1:]
        out = {
            'single' : 'id', 
            'name' : name, 
        }
    elif raw[0] == '.':
        name = raw[1:]
        out = {
            'single' : 'class', 
            'name' : name, 
        }
    elif raw[0] == '[':
        out = _parse_single_attr(raw)
        out['single'] = 'attr'
    else:
        out = {
            'single' : 'element', 
            'name' : raw, 
        }
    # set multi default to 'tree'
    out['multi'] = 'tree'
    return out	# done

# parse multi selectors

def _parse_multi_sub(out, raw_text):
    '''
    eg. 
    
    div.hide[type=text].test#a.b#c
    
    '''
    # TODO this split method maybe BUG here
    raw_text = raw_text.strip()
    if raw_text == '':
        return
    # first, split #
    tmp = raw_text.split('#')
    raw = [tmp[0]]
    for i in tmp[1:]:
        one = '#' + i
        raw.append(one)
    tmp = raw
    raw = []
    for i in tmp:
        one = i.strip()
        if one != '':
            raw.append(one)
    # next, split .
    tmp = []
    for i in raw:
        one = i.split('.')
        tmp.append(one[0])
        for j in one[1:]:
            tmp.append('.' + j)
    raw = []
    for i in tmp:
        one = i.strip()
        if one != '':
            raw.append(one)
    # finally, split [
    tmp = []
    for i in raw:
        one = i.split('[')
        tmp.append(one[0])
        for j in one[1:]:
            tmp.append('[' + j)
    to = []
    for i in tmp:
        one = i.strip()
        if one != '':
            to.append(one)
    # parse first
    if len(to) < 1:
        return
    one = _parse_single(to[0])
    out.append(one)
    # parse each rest of it, and change its type to multi.sub
    for i in to[1:]:
        one = _parse_single(i)
        one['multi'] = 'sub'
        out.append(one)
    # done

def _parse_multi_tree(out, raw_text):
    '''
    eg. 
    
    a img
    
    '''
    raw = raw_text.strip().split(' ')
    # process each item
    for i in raw:
        if i.strip() != '':
            one = []
            _parse_multi_sub(one, i)
            # NOTE no need to change 'multi' type, the default is 'tree'
            out += one
    # done

def _parse_multi_children(out, raw_text):
    '''
    eg. 
    
    > a
    
    a > img
    
    '''
    # do split
    raw = raw_text.strip().split('>')
    # process first
    first, raw = raw[0], raw[1:]
    if first.strip() != '':
        one = []
        _parse_multi_tree(one, first)
        out += one
    # process rest
    for i in raw:
        if i.strip() != '':
            one = []
            _parse_multi_tree(one, i)
            # NOTE update first.multi to 'children'
            one[0]['multi'] = 'children'
            out += one
    # done

def _parse_multi_add(out, raw_text):
    '''
    eg. 
    
    a, img
    '''
    raw = raw_text.strip().split(',')
    for i in raw:
        if i.strip() != '':
            one = []
            _parse_multi_children(one, i)
            out.append(one)
    # done

# entry function
def parse_selector(raw_text):
    '''
    
    -> [] dict
    '''
    out = []
    _parse_multi_add(out, raw_text)
    return out

# end selector_grammar.py


