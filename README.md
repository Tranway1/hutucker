# Hu-Tucker
Simple implementation of the Hu-Tucker algorithm to produce efficient *ordererd* binary codes. These codes work like Huffman codes, but guarantee that the specified order of symbols and the lexical order of binary strings are the same. Hu Tucker codes are the *optimal* ordered codes, and are at most 1 bit worse
than the corresponding Huffman codes.

## Using

    hutucker.hutucker(sym_table, return_code=False)
    
`sym_table` should be a list of symbols, each of which should be a pair `(symbol,weight)`. Weights do not need to be normalised. For example:

    print hu_tucker([("a",1), ("b", 4), ("c",2), ("d",12)])
    
The result is a binary tree representing the Hu Tucker code, in this case:

    [[['a', 'b'], 'c'], 'd']
    
### return_code
If `return_code` is true, then the return includes the explicit binary codes (useful for debugging). In the case of the example above, this would be:

    {'a': '000', 'c': '01', 'b': '001', 'd': '1'}
    
**License: BSD**


