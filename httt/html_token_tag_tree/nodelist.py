# nodelist.py, httt/html_token_tag_tree/

class httt_nodelist(list):
    '''
    node list for httt, return-ed by httt_tree.find() and httt_nodelist.find()
    '''
    
    # add some easy functions
    
    def text(self):
        '''
        
        -> [] (str)
        '''
        # just get each text
        out = []
        for i in self:
            out += i.text()
        return out
    
    def find(self, selector):
        '''
        
        -> httt_nodelist
        '''
        # just find each item, and join with tree.id
        out = []
        for i in self:
            one = i.find(selector)
            out.append(one)
        out = join_with_tree_id(out)
        out = httt_nodelist(out)
        return out
    
    # end httt_nodelist class

# join with tree id
def join_with_tree_id(old_list):
    tmp = {}
    for old in old_list:
        for i in old:
            if not i._id in tmp:
                tmp[i._id] = i
    out = list(tmp.values())
    out.sort(key=lambda x: x._id)
    return out

# end nodelist.py


