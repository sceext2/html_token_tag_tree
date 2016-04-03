# split_token.py, httt/html_token_tag_tree/

import re
import html

from . import token
from .token_host import httt_token_host

# base html text functions

def process_quote(raw_text):
    '''
    unquote raw html text, such as &lt;
    '''
    return html.unescape(raw_text)

def parse_tag_attr(raw_text):
    '''
    parse attr for tag.start and tag.startclose
    '''
    # NOTE this should process ' ' (space), '=' and '"' (quote)
    # eg. <div hidden id=a class="2" style='' >
    
    out = {}
    rest = raw_text.strip()
    # main loop
    while len(rest.strip()) > 0:
        rest = rest.strip()
        # find first ' ' (space) (i) or first '=' (j) char
        i = rest.find(' ')
        j = rest.find('=')
        # check and process ' ' (space) char
        if (i == -1) and (j == -1):
            # NOTE this is the only attribute, but without value
            attr_name = rest
            rest = ''	# reset rest
            
            value = None
        # NOTE process 'id ="abc"' attr, NOTE the space (' ') char before '='
        elif (j != -1) and (i != -1) and (i < j) and (rest[i:j].strip() == ''):
            attr_name = rest[:i]
            rest = rest[j + 1:]
            
            value, rest = _tag_attr_get_value(rest)
        elif ((j == -1) and (i != -1)) or ((j != -1) and (i != -1) and (i < j)):
            attr_name = rest[:i]
            rest = rest[i:]
            # this attribute has no value
            value = None
        else:	# here can only be (j != -1)
            # get attr name
            attr_name = rest[:j]
            rest = rest[j + 1:]	# split '=' char
            
            value, rest = _tag_attr_get_value(rest)
        # NOTE set this attr, TODO support many attr with the same attr_name
        attr_name = attr_name.strip()
        # TODO process value html quote
        out[attr_name] = value
    return out	# done

def _tag_attr_get_value(rest):
    '''
    
    -> value, rest
    '''
    # get value, and process " char
    if len(rest) < 1:
        value = None	# no value
    else:
        # process " quote
        if rest[0] == '\"':
            rest = rest[1:]
            k = rest.find('\"')	# next first " char
        elif rest[0] == '\'':
            rest = rest[1:]
            k = rest.find('\'')
        else:	# no quote
            k = rest.find(' ')
        if k == -1:	# TODO maybe BAD here
            value = rest
            rest = ''	# reset rest
        else:
            value = rest[:k]
            rest = rest[k + 1:]	# split one char
    return value, rest

# split Parse Control Info (pci)
class parse_control_info(object):
    '''
    
    get next tag token mode:
    
    + None	the default mode
    + script	for <script> </script>
    + style	for <style> </style>
    + pre	for <pre> </pre>
    
    '''
    def __init__(self):
        self.rest_html = None	# (str) current rest raw html text
        self.host = None	# (object/httt_token_host) host object for this parse (split)
        self.mode = None	# current get next tag token mode, None means normal mode
        self.flag_quote = True	# if True, do process_quote(), else NOT
    # end parse_control_info (pci) class

# base parse (split) functions

def get_next_close_tag(pci, tag_name):
    '''
    used for find </script> </style> </pre> tags
    support UpperCase, such as </SCRIPT> </Style>, etc. 
    
    -> (raw_text, tag_text)
    '''
    # TODO improve performance, the current method is very slow
    # get all avaliable close tags
    all_list = re.findall('</([^>]+)>', pci.rest_html)
    close_tag = None
    # try to find first tag
    tag_name = tag_name.lower()
    for i in all_list:
        if i.lower() == tag_name:
            close_tag = i
            break
    # check found
    if close_tag == None:
        # not found
        text = pci.rest_html
        pci.rest_html = ''	# reset rest
        
        return text, ''
    # make close tag text, and find its position
    close_text = '</' + close_tag + '>'
    i = pci.rest_html.find(close_text)
    # do split
    raw_text = pci.rest_html[:i]
    pci.rest_html = pci.rest_html[i + len(close_text):]	# just split close tag text
    
    return raw_text, close_text	# done

def get_next_tag(pci):
    '''
    get next tag from pci.rest_html with normal mode (None)
    
    will auto create text token before this tag
    will auto create this tag
    
    -> object/httt_token_tag or None
    '''
    # find first '<' char
    i = pci.rest_html.find('<')
    if i == -1:	# no more tags
        raw_text = pci.rest_html
        pci.rest_html = ''	# reset rest
    else:
        raw_text = pci.rest_html[:i]
        pci.rest_html = pci.rest_html[i:]
    # check to create text token
    if len(raw_text) > 0:
        create_text_token(pci, raw_text)
    # check rest empty
    if len(pci.rest_html) < 1:
        return None
    # check tag type
    if pci.rest_html.startswith('<![CDATA['):
        # CDATA
        tag_type = 'tag.cdata'
        # find end of the tag
        i = pci.rest_html.find(']]>')
        if i == -1:	# tag until end of the document
            tag_text = pci.rest_html
            pci.rest_html = ''	# reset rest
        else:
            i += len(']]>')
            tag_text = pci.rest_html[:i]
            pci.rest_html = pci.rest_html[i:]
        # create CDATA tag
        tag = create_tag_cdata(pci.host, tag_text)
    elif pci.rest_html.startswith('<!--'):
        # comment
        tag_type = 'tag.comment'
        # find end of the tag
        i = pci.rest_html.find('-->')
        if i == -1:
            tag_text = pci.rest_html
            pci.rest_html = ''	# reset rest
        else:
            i += len('-->')
            tag_text = pci.rest_html[:i]
            pci.rest_html = pci.rest_html[i:]
        # create comment tag
        tag = create_tag_comment(pci.host, tag_text)
    else:	# normal tag
        tag_type = 'tag'
        # TODO support quote in normal tag (", ' chars)
        i = pci.rest_html.find('>')
        if i == -1:
            tag_text = pci.rest_html
            pci.rest_html = ''	# reset rest
        else:
            i += 1
            tag_text = pci.rest_html[:i]
            pci.rest_html = pci.rest_html[i:]
        # create normal tag
        tag = create_tag_normal(pci.host, tag_text)
    return tag	# done

# create tag functions

def create_tag_normal(host, raw_tag_text):
    '''
    support token type
    
    + tag		eg. <?xml ?> <!DOCTYPE >
    + tag.start
    + tag.startclose
    + tag.close		eg. </div>
    
    will auto turn tag.name to lowercase if possible
    
    -> object/httt_token_tag
    '''
    # check close tag
    if raw_tag_text.startswith('</'):
        tag_name = raw_tag_text.split('</', 1)[1].rsplit('>', 1)[0].lower()
        tag = token.httt_token_tag(host, 'tag.close')
        tag.raw_text = raw_tag_text
        tag.name = tag_name
        # NOTE add raw_text to host.token_text
        host.token_text.append(raw_tag_text)
        
        return tag
    # check special tag
    # TODO maybe improve
    if raw_tag_text[1] in ['?', '!']:
        tag = token.httt_token_tag(host, 'tag')
        tag.raw_text = raw_tag_text
        # NOTE add raw_text to host.token_text
        host.token_text.append(raw_tag_text)
        
        return tag
    # attr tag
    tag = create_tag_attr(host, raw_tag_text)
    # fix tag.name to lower
    tag.name = tag.name.lower()
    
    return tag	# done

def create_tag_attr(host, raw_tag_text):
    '''
    support token type
    
    tag.start		eg. <div>
    tag.startclose	eg. <br />
    
    -> object/httt_token_tag_attr
    '''
    # check tag type, and split for inner text
    text = raw_tag_text.split('<', 1)[1]
    if raw_tag_text.endswith('/>'):
        tag_type = 'tag.startclose'
        text = text.rsplit('/>', 1)[0]
    else:
        tag_type = 'tag.start'
        text = text.rsplit('>', 1)[0]
    # get tag name
    part = text.split(' ', 1)
    tag_name = part[0]
    if len(part) > 1:
        text = part[1]
    else:
        text = ''
    # create tag
    tag = token.httt_token_tag_attr(host, tag_type)
    tag.raw_text = raw_tag_text
    tag.name = tag_name
    # NOTE add raw_text to host.token_text
    host.token_text.append(raw_tag_text)
    
    # get attr
    tag.attr = parse_tag_attr(text)
    
    return tag	# done

def create_tag_cdata(host, raw_tag_text):
    '''
    support token type
    
    + tag.cdata
    
    -> object/httt_token_tag_text
    '''
    # get inner text
    text = raw_tag_text.split('<![CDATA[', 1)[1].rsplit(']]>', 1)[0]
    # create tag.cdata
    tag = token.httt_token_tag_text(host, 'tag.cdata')
    tag.raw_text = raw_tag_text
    tag.text = text
    # NOTE add raw_text to host.token_text
    host.token_text.append(raw_tag_text)
    
    return tag	# done

def create_tag_comment(host, raw_tag_text):
    '''
    support token type
    
    + tag.comment
    
    -> object/httt_token_tag_text
    '''
    # get inner text
    text = raw_tag_text.split('<!--', 1)[1].rsplit('-->', 1)[0]
    # create tag.comment
    tag = token.httt_token_tag_text(host, 'tag.comment')
    tag.raw_text = raw_tag_text
    tag.text = text
    # NOTE add raw_text to host.token_text
    host.token_text.append(raw_tag_text)
    
    return tag	# done

def create_text_token(pci, raw_text):
    '''
    create text token and add it to host
    '''
    # check quote
    text = raw_text
    if pci.flag_quote:
        text = process_quote(text)
    # create text token
    t = token.httt_token_text(pci.host)
    t.text = text
    # NOTE add raw_text to host.token_text
    pci.host.token_text.append(raw_text)
    
    return t	# done

# main split loop
def _split_loop(pci):
    # split until no raw html text left
    while len(pci.rest_html) > 0:
        # check get next token mode
        if pci.mode == None:
            # normal mode
            tag = get_next_tag(pci)
            if tag == None:
                continue	# no more tags
            # check tag.name to enter other mode, now support 'script', 'style', 'pre'
            if tag.name in ['script', 'style', 'pre']:
                pci.mode = tag.name
                pci.flag_quote = False	# turn off quote here
        else:	# special mode
            raw_text, tag_text = get_next_close_tag(pci, pci.mode)
            # check to add text token
            if len(raw_text) > 0:
                create_text_token(pci, raw_text)
            # check to create tag token, NOTE tag_text maybe also empty
            if len(tag_text) > 0:
                create_tag_normal(pci.host, tag_text)
            
            # NOTE turn off mode here
            pci.mode = None
            pci.flag_quote = True	# turn on quote here
    # done

# parse token entry function
def split_token(raw_html):
    '''
    
    -> httt_token_host
    '''
    # init token split
    pci = parse_control_info()
    pci.host = httt_token_host()
    pci.rest_html = raw_html
    
    pci.host.raw_html = raw_html
    # do split token
    _split_loop(pci)
    
    return pci.host	# done

# end split_token.py


