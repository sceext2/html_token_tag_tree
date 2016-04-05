# selector_grammar.py, httt/html_token_tag_tree/
# parse css selector (text) for httt
'''

TODO support quote " ' or \ chars in css selector text

(14 = 4 + 10) supported css selectors

    [CSS version] [selector name]	[selector pattern]	[eg.]
  
  # (4) combination selector
    N/A		filter.sub					div.hide
    1		filter.tree		element element		div p
    2		filter.children		element>element		div>p
    1		filter.add		element,element		div,p
  
  # (10 == 4 + 6) single CSS selector
    2	all				*			*
    1	element				element			p
    1	id				#id			#firstname
    1	class				.class			.intro
  
  # (6) attribute selectors
    2	attr				[attribute]		[target]		elements has attr 'target'
    2	attr.=				[attribute=value]	[target=_blank]		elements with attr target="_blank"
    2	attr.~				[attribute~=value]	[title~=flower]		attr include words "flower"
    3	attr.^				[attribute^=value]	[src^=https]		attr value startswith "https"
    3	attr.$				[attribute$=value]	[src$=.pdf]		attr value endswith ".pdf"
    3	attr.*				[attribute*=value]	[src*=44lan]		attr include str "44lan"

TODO
    2	attr.|				[attribute|=language]	[lang|=en]		(unknow) 选择一个lang属性的起始值="EN"的所有元素

one css action info
    {
        'filter' : '', 	# in 'sub', 'tree', 'children'
        'type' : '', 	# in 'all', 'element', 'id', 'class', 'attr'
        'name' : '', 	# [optional] no use for 'all'
        'attr' : '', 	# [optional] in '' (attr), '=', '~', '|', '^', '$', '*'
        'value' : '', 	# [optional] only for 'attr'
    }

'''

# first step, raw split token
def _raw_split_token(raw_text):
    # TODO support \ chars in raw_text for split token
    # NOTE replace some bad chars here
    raw_text = raw_text.replace('\r', '\n').replace('\n', ' ')
    # NOTE strip first
    rest = raw_text.strip()
    # scan each char to get tokens
    mode = ''	# scan mode, can be '' (normal), '[' (for attr [])
    one_char_token = ',> #.'
    
    raw = []	# raw token list
    one = ''	# one token text
    while len(rest) > 0:
        # get one rest char
        c, rest = rest[0], rest[1:]
        # check mode
        if mode == '[':	# attr mode
            one += c
            # check end char
            if c == ']':
                # add current token and reset one
                raw.append(one)
                one = ''
                # reset mode
                mode = ''
            # else, nothing to do
        else:	# normal mode
            # NOTE replace \t to space char
            if c == '\t':
                c = ' '
            # check one char token
            if c in one_char_token:
                # add current token, and reset one
                raw.append(one)
                one = ''
                # add this one char token
                raw.append(c)
            elif c == '[':
                # attr token start, add current token, and reset one
                raw.append(one)
                one = c
                # enable mode
                mode = '['
            else:	# normal token
                one += c
    # scan done, add last token
    raw.append(one)
    # remove empty token ('')
    out = [i for i in raw if i != '']
    return out	# done

# clean raw token, remove no use space (' ') tokens
def _clean_raw_token(raw_list):
    # check has tokens
    if len(raw_list) < 1:
        return []
    # add first token first
    out, raw = [raw_list[0]], raw_list[1:]
    for i in raw:
        # check multi-space tokens ('  '), or space tokens after ',', '>' token
        if (i == ' ') and (out[-1] in [' ', ',', '>']):
            continue	# ignore this token
        # check space tokens before ',' and '>' token
        if (i in [',', '>']) and (out[-1] == ' '):
            out[-1] = i	# replace space token
        else:	# normal token
            out.append(i)
    return out	# done

# parse single selectors
def _parse_single_attr(raw_text):
    # remove '[', ']' from raw_text
    raw = raw_text
    if raw[0] == '[':
        raw = raw[1:]
    if raw[-1] == ']':
        raw = raw[:-1]
    out = {
        'name' : '', 
        'attr' : '', 
    }
    # no '=' in attr (eg. [href])
    if not '=' in raw:
        out['name'] = raw
        return out
    # check char before '=' char
    raw_name, out['value'] = raw.split('=', 1)
    # [attribute~=value]
    # [attribute^=value]
    # [attribute$=value]
    # [attribute*=value]
    # [attribute=value]
    out['attr'] = '='
    if len(raw_name) > 0:
        c = raw_name[-1]
        if c in '~^$*':
            out['attr'] = c
            raw_name = raw_name[:-1]
    out['name'] = raw_name
    return out	# done

def _parse_single(raw_text):
    if len(raw_text) < 1:
        out = {
            'type' : 'element', 
            'name' : raw_text, 
        }
        return out
    raw = raw_text
    # check raw_text type
    if raw == '*':
        out = {
            'type' : 'all', 
        }
    elif raw[0] == '#':
        name = raw[1:]
        out = {
            'type' : 'id', 
            'name' : name, 
        }
    elif raw[0] == '.':
        name = raw[1:]
        out = {
            'type' : 'class', 
            'name' : name, 
        }
    elif raw[0] == '[':
        out = _parse_single_attr(raw)
        out['type'] = 'attr'
    else:
        out = {
            'type' : 'element', 
            'name' : raw, 
        }
    # NOTE filter default to 'tree'
    out['filter'] = 'tree'
    return out	# done

# parse combination css selectors from token list

def _split_token_list(token_list, token, add_back=True):
    tmp = []
    one = []
    for i in token_list:
        if i == token:
            tmp.append(one)
            one = []
        else:
            one.append(i)
    if len(one) > 0:
        tmp.append(one)
    if not add_back:
        # not add back tokens
        return tmp
    if len(tmp) < 1:
        return tmp
    # add token back
    out = [tmp[0]]
    for i in tmp[1:]:
        one = [token] + i
        out.append(one)
    return out	# done

def _parse_filter_sub(out, token_list):
    '''
    eg. 
        div.hide[type=text].test#a.b#c
    
    tokens
        ['div', '.', 'hide', '[type=text]', '.', 'test', '#', 'a', '.', 'b', '#', 'c']
    
    '''
    if len(token_list) < 1:
        return
    # first, split '#' tokens
    raw = _split_token_list(token_list, '#')
    # next, split '.' tokens
    tmp = []
    for i in raw:
        one = _split_token_list(i, '.')
        tmp += one
    # finally, split '[]' (attr) tokens
    raw = []
    one = []
    for i in tmp:
        for j in i:
            if j.startswith('['):	# is a attr token
                if len(one) > 0:
                    raw.append(one)
                    one = []
                # add this token
                raw.append([j])
            else:	# normal token
                one.append(j)
        if len(one) > 0:
            raw.append(one)
            one = []
    # generate single selector texts
    to = []
    for i in raw:
        one = ('').join(i)
        to.append(one)
    
    # parse first
    if len(to) < 1:
        return
    one = _parse_single(to[0])
    out.append(one)
    # parse each rest of it, and change its filter to sub
    for i in to[1:]:
        one = _parse_single(i)
        one['filter'] = 'sub'
        out.append(one)
    # done

def _parse_filter_tree(out, token_list):
    '''
    process ' ' (space) tokens
    '''
    if len(token_list) < 1:
        return
    raw = _split_token_list(token_list, ' ', add_back=False)
    # just process each item, NOTE default filter is tree
    for i in raw:
        one = []
        _parse_filter_sub(one, i)
        out += one
    # done

def _parse_filter_children(out, token_list):
    '''
    process '>' tokens
    '''
    if len(token_list) < 1:
        return
    raw = _split_token_list(token_list, '>', add_back=False)
    # process first
    first, raw = raw[0], raw[1:]
    if len(first) > 0:
        one = []
        _parse_filter_tree(one, first)
        out += one
    # process rest
    for i in raw:
        if len(i) > 0:
            one = []
            _parse_filter_tree(one, i)
            # NOTE change filter to 'children'
            one[0]['filter'] = 'children'
            out += one
    # done

def _parse_filter_add(out, token_list):
    '''
    process ',' tokens
    '''
    raw = _split_token_list(token_list, ',', add_back=False)
    for i in raw:
        if len(i) > 0:
            one = []
            _parse_filter_children(one, i)
            out.append(one)
    # done

# entry function
def parse_selector(raw_text):
    '''
    
    -> [] dict
    '''
    # split tokens first
    raw_token = _raw_split_token(raw_text)
    # clean token list
    token_list = _clean_raw_token(raw_token)
    # do parse
    out = []
    _parse_filter_add(out, token_list)
    return out	# done

# end selector_grammar.py


