def euclid(a, b):
    '''
        parameters:
            a -- int
            b -- int
        returns:
            path_length -- int
        description:
            using Euclid's algorithm
    '''
    if (a < 0) or (b < 0) or (b > a):
        if a < 0:
            a = -a
        if b < 0:
            b = -b
        if b > a:
            tmp = b
            b = a
            a = tmp
        ret_val = euclid(a, b)
    elif (b==0) and (a>0):
        ret_val = a
    elif (b!=0) and (a!=0):
        d = a // b
        new_a = b
        new_b = a - d * b
        ret_val = euclid(new_a, new_b)
    else:
        ret_val = 0
    return ret_val
