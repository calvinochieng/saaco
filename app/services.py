from  string import ascii_letters as letters, digits
from random import choice

def idshortener():
    a, b = letters, digits
    chars = "".join([a,b,'_-'])
    id = "".join( [choice(chars) for _ in range(10)])
    return id







