# nodelist.py, httt/html_token_tag_tree/

class httt_nodelist(list):
    '''
    node list for httt, return-ed by httt_tree.find() and httt_nodelist.find()
    '''
    
    # NOTE set operations for httt_nodelist, add and sub
    def __add__(self, nodelist):
        # just join with tree id
        out = join_with_tree_id([self, nodelist])
        out = httt_nodelist(out)
        return out	# done
    def __iadd__(self, nodelist):
        return self.__add__(nodelist)
    
    def __sub__(self, nodelist):
        # create set with self
        tmp = {}
        for i in self:
            tmp[i._id] = i
        # sub nodelist from current set
        for i in nodelist:
            if i._id in tmp:
                tmp.pop(i._id)	# do remove it
        # make output and sort result
        out = httt_nodelist(tmp.values())
        out.sort(key=lambda x: x._id)
        return out	# done
    
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
    
    def html(self):
        '''
        
        -> [] str
        '''
        out = [i.html() for i in self]
        return out
    
    def name(self):
        '''
        
        -> [] str
        '''
        out = [i.name for i in self]
        return out
    
    # find from current set
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
            # NOTE no need to check, only one ._id can be in the set
            tmp[i._id] = i
    out = list(tmp.values())
    out.sort(key=lambda x: x._id)
    return out

# end nodelist.py


