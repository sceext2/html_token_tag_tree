# tag_host.py, httt/html_token_tag_tree/

from .rule import tree_rule

# one tag info
class httt_one_tag(object):
    '''
    '''
    def __init__(self):
        self.name = None	# (str) name of this tag
        self.type = None	# (str or None) tag type, can be None (normal), 
        	# 'selfclose' (force selfclose), 'struct' (force struct)
        self.level = 0	# (int) level (index) of this tag, bigger is higher
        self.conflict = []	# conflict list of this tag
        	# conflict tags can not be nested
    # end httt_one_tag class

class httt_tag_host(object):
    '''
    '''
    def __init__(self):
        self.tag_index = {}	# name -> httt_one_tag index
        
        self.unknow_tag = httt_one_tag()
        
        # bad tree tag actions
        self.selfclose_close_tag = 'ignore'	# process self-close tag.close, such as </br>
        	# can be 'ignore', 'selfclose'
        self.isolate_struct_close_tag = 'ignore'
        	# process isolate struct tag.close (no match tag.start)
        	# can be 'ignore', 'selfclose'
    
    def get(self, tag_name):
        '''
        get tag info
        
        -> httt_one_tag (object)
        '''
        if tag_name in self.tag_index:
            return self.tag_index[tag_name]
        return self.unknow_tag
    
    # private functions
    def _check_create_tag(self, tag_name):
        if not tag_name in self.tag_index:
            one = httt_one_tag()
            one.name = tag_name
            self.tag_index[tag_name] = one
    
    # create (init) set functions
    def set_type(self, tag_name, tag_type):
        self._check_create_tag(tag_name)
        self.tag_index[tag_name].type = tag_type
    
    def set_level(self, tag_name, level):
        self._check_create_tag(tag_name)
        self.tag_index[tag_name].level = level
    
    def _set_one_conflict(self, tag_name, conflict):
        self._check_create_tag(tag_name)
        self.tag_index[tag_name].conflict = conflict
    
    def set_conflict(self, conflict_group):
        for i in conflict_group:
            self._set_one_conflict(i, conflict_group)
    # end httt_tag_host class

# read rules and create httt_tag_host
def load_config(rule_set=tree_rule.rule_set):
    '''
    
    -> httt_tag_host
    '''
    host = httt_tag_host()
    # set tag type
    if 'force_selfclose_tag' in rule_set:
        rule = rule_set['force_selfclose_tag']
        for i in rule:
            host.set_type(i, 'selfclose')
    if 'force_struct_tag' in rule_set:
        rule = rule_set['force_struct_tag']
        for i in rule:
            host.set_type(i, 'struct')
    # set tag level
    if 'tag_level' in rule_set:
        rule = rule_set['tag_level']
        for j in rule:
            for i in rule[j]:
                host.set_level(i, j)
    # set conflict
    if 'conflict_group' in rule_set:
        rule = rule_set['conflict_group']
        for i in rule:
            host.set_conflict(i)
    # set special tag
    if 'tag' in rule_set:
        rule = rule_set['tag']
        for tag_name in rule:
            one = rule[tag_name]
            if 'type' in one:
                host.set_type(tag_name, one['type'])
            if 'level' in one:
                host.set_level(tag_name, one['level'])
            if 'conflict' in one:
                host.tag_index[tag_name].conflict = one['conflict']
    # set default (unknow) tag
    if 'selfclose_close_tag' in rule_set:
        host.selfclose_close_tag = rule_set['selfclose_close_tag']
    if 'isolate_struct_close_tag' in rule_set:
        host.isolate_struct_close_tag = rule_set['isolate_struct_close_tag']
    if 'default_tag_level' in rule_set:
        host.unknow_tag.level = rule_set['default_tag_level']
    if 'unknow_tag_type' in rule_set:
        host.unknow_tag.type = rule_set['unknow_tag_type']
    # load config done
    return host

# end tag_host.py


