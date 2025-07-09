#gcayin
"""
def list_gcayin(tmp):
    ms= []
    ml = list(tmp)[::-1] 
    while ml:
        elem = ml.pop()
        if type(elem) is list:  
            ml.extend(elem[::-1]) 
        else:
            ms.append(elem)
    return ms
md=[1,[2,[3,4,[5],5],8],[5],9]
result=list_gcayin(md)
print(result)"""


#rekursiv
"""
def list_rekursiv(tmp):
    ms= []
    for el in tmp:
        if type(el) is list:
            ms.extend(list_rekursiv(el))
        else:
            ms.append(el)
    return ms
md=[1,[2,[3,4,[5],5],8],[5],9]
result=list_rekursiv(md)
print(result)
"""