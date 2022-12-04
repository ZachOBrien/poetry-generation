"""
Utilities for working with lists

"""

def remove_leading_and_trailing(lst, pred):
    """Remove leading and trailing items from a list that pass some predicate

    Args:
        lst (list): A list
        pred (Callable[Any, bool]): A predicate to apply to items in `lst`

    Returns:
        list: The original list, but with the longest continuous chain of items
        at the beginning of the list and end of the list that pass the predicate
        removed  
    """
    i = 0
    while i < len(lst) and pred(lst[i]):
        i += 1
    leading_removed = lst[i:]
    
    j = 1
    while j < len(lst) and pred(leading_removed[-j]):
        j += 1
    trailing_removed = leading_removed[: len(leading_removed) - j + 1]
    
    return trailing_removed
    

def split_into_blocks(lst, is_block_header, read_block):
    """Split a list into blocks

    Args:
        lst (list): A list
        is_block_header (Callable[Any, bool]): True if a value is the header of a block
        read_block (Callable[list, list[Any]]): Reads a block of data after a header was found

    Returns:
        list: A list of blocks
    """
    blocks = []
    i = 0
    while True:
        if i >= len(lst):
            return blocks
        
        if is_block_header(lst[i]):
            block = (lst[i], read_block(lst[i+1:]))
            blocks.append(block)
            i += len(block[1]) + 1
        else:
            i += 1 
