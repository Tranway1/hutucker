
# return the huffman code of a symbol -> probability dictionary
def huffman_encode(sym_prob_table):                                       
    # sort table by probability. Queue is form (p, leaf=True, symbol)
    q1 = sorted([(sym_prob_table[k],True,k) for k in sym_prob_table])
    q2 = []        
    # while there's still more than one element
    while len(q1)+len(q2)>1:                  
            # pop the smallest two elements and  append a new node, (p=p(left)+p(right), leaf=False, (left, right))
            elts = [q1.pop(0) if (len(q2)<=0 or (len(q1)>0 and q1[0][0]<q2[0][0])) 
                    else q2.pop(0) for i in range(2)]
            elts = (elts[1], elts[0])
            q2.append((sum([x[0] for x in elts]), False, elts))           
    # create the dictionary mapping symbols to binary strings        
    return q2[0]
    
    
def simplify(tree):
    if tree[1]:
        return tree[2]
    else:
        return [simplify(tree[2][0]),simplify(tree[2][1])]

# phase I
def find_min_compat(nodes,i,dir=1):
    compatible = True
    min = 1e6
    minarg = None
    while ((dir==-1 and i>0) or (dir==1 and i<len(nodes)-1)) and compatible:
        i=i+dir
        if nodes[i][0]<min:
            min = nodes[i][0]
            minarg = i            
        compatible = not nodes[i][1]        
    return minarg
            
    
def find_compatible(nodes, i):
    left = find_min_compat(nodes,i,-1)
    right = find_min_compat(nodes,i,1)
    if left==None and right==None:
        return None        
    if right==None or (left!=None and nodes[left]<=nodes[right]):
        return left
    else:
        return right

        
def merge_nodes(nodes, x, y):
    nx, ny = nodes[x], nodes[y]    
    nodes[x] = (nx[0]+ny[0], False, (nx,ny))    
    nodes.remove(ny) 
    
        
# merge all nodes according to the hu-tucker rule
def merge(sym_prob_table):
    nodes = [(k[1],True,k[0]) for k in sym_prob_table]            
    while len(nodes)>1:
        i = 0
        while i<len(nodes):
            min = find_compatible(nodes, i)            
            mincom = find_compatible(nodes,min)
            if min!=None and mincom!=None and mincom==i:
                merge_nodes(nodes,i,min)
            i = i + 1    
    return nodes[0]
                            
# Phase II
# get the code word lengths
def get_lengths(tree, d, l=0):    
    if tree[1]==True:
        d[tree[2]] = l
    else:
        get_lengths(tree[2][0], d, l+1)
        get_lengths(tree[2][1], d, l+1)
    
# Phase III
# code each word
def code(sym_prob_table, d):
    codes = {}   
    sym = sym_prob_table[0][0]
    code  = "0" * d[sym]
    codes[sym] = code    
    
    for s in sym_prob_table[1:]:            
            sym = s[0]
            code = code.rstrip("1")
            last_one = code.rfind("0")
            
            if last_one>=0:
                code = code[:last_one] + "1" + code[last_one+1:]            
            diff_len = d[sym]-len(code)
            if diff_len>0:
                code = code + ("0" * diff_len)            
            codes[sym] = code
    return codes
    
# insert a code into a tree
def insert_code(f, code, tree):    
    if tree==None and len(code)>0:
        tree = [None,None]
    if len(code)==0:
        tree = f    
    else:    
        if code[0]=="0":
            tree[0] = insert_code(f, code[1:], tree[0])
        else:
            tree[1] = insert_code(f, code[1:], tree[1])
    return tree
        
  
# Wrappers   
# convert a code table into a tree
def treeify(code_table):
    tree = [None, None]
    [insert_code(f, code_table[f], tree) for f in code_table]
    return tree
        
        
def hu_tucker_unordered(sym_prob_table):
    return hu_tucker_ordered(hu_tucker_ordered(sorted(sym_prob_table.items)))
    
# hu tucker code a list of (symbol, probability) pairs    
def hu_tucker(sym_prob_table, return_code=False):    
    """Takes a symbol probability table, and returns the HuTucker tree representations.
    
    Parameters:
    ---
        sym_prob_table: should be a list of symbols, each of which should be a pair `(symbol,weight)`. Weights do not need to be normalised. Example: [("a",1), ("b", 4), ("c",2), ("d",12)]
        return_code: if True, return the binary codes as well, as a dictionary mapping symbols to binary sequences (as strings)
        
    Returns:
    ---
        tree, [symbols]
        tree is the binary tree form of the code (e.g. [[['a', 'b'], 'c'], 'd'] for the example above)
        symbols (only returned if return_code=True) is a dictionary, mapping symbols to binary strings. {'a': '000', 'c': '01', 'b': '001', 'd': '1'}, in the 
                                example above
    """
    d = {}
    get_lengths(merge(sym_prob_table), d)
    
    c = code(sym_prob_table, d)
    
    # return the raw codes if required
    if return_code:
        return treeify(c), c
    else:
        return treeify(c)
      
    
    
if __name__=="__main__":
    print hu_tucker([("a",1), ("b", 4), ("c",2), ("d",12)], return_code=True)

