#1 Գրել ֆունկցիա որը կվերդարձնի ստացած արգումենտներից թվերիգումարը։
"""def sum_numbers(*args):
    total = 0
    for el in args:
        if  type(el) is int:
            total += el
    return total
result = sum_numbers(10, 'abc', 5, 5, True, [1, 2], 3, '7', None)
print(result)"""

#2 Գրել ֆունկցիա որը կվերդարձնի ստացած արգումենտներից տողերի քանակը։
"""def count_str(*args):

    count=0
    for el in args:
        if type(el) is str:
            count+=len(el)
    return count        
result = count_str(10, 'abc', 5, 5, True, [1, 2], 3, '7', None,"ttt")
print(result)"""

#3Գրել ֆունկցիա որը կվերադարձնի ստասած արգումենտների միջին թվաբանականը։
"""def mij_tv(*args):
    summ = 0
    countt = 0
    for el in args:
        if type(el) is int:
            summ += el
            countt += 1
    result = summ / countt        
    return result
ms = mij_tv(True, 12, 3, "hfhf", 4, [12, 3, 3, 5], "kk", 78)
print(ms) """

#4Գրել ֆունկցիա որը կստանա արգումենտ և կվերադարձնի այդ արգումենտերի հետ կատարած մաթեմատիկական գործողությունների
"""def math_oper(x,y):
    result={"sum":x+y,"diff":x-y,"prod":x*y,"div":x/y}
    return result
x=int(input("--"))
y=int(input("--"))
ml=math_oper(x,y)
print(ml)"""

#5.Գրել ֆունկցիա որը որպես արգումենտ կստանա տողը և կվերադարձնի այն դարձված ամբողջությամբ մեծատառ ֆունկցիան օգտագործել չի կարելի ։
"""def uperring(mstr):
    up = "" 
    for el in mstr:
        if "a" <= el <= "z":
            up += chr(ord(el) - 32) 
        else:
            up += el 
    return up
mstr = input("-- ")
ml = uperring(mstr)
print(ml)"""

#6Գրել ֆունկցիա որը որպես արգումենտ կստանա տողը և կվերադարձնի այն դարձված ամբողջությամբ փոքրատառ (lower ֆունկցիան օգտագործել չի կարելի) ։
"""def lowering(mstr):
    low = "" 
    for el in mstr:
        if "A" <= el <= "Z":
            low += chr(ord(el) + 32) 
        else:
            low += el 
    return low
mstr = input("-- ")
ml = lowering(mstr)
print(ml)"""

#7.Գրել ֆունկցիա որը որպես արգումենտ կստանա տողը և կվերադարձնի այն դարձված բոլոր բառերի առաջին տառերը մեծատառ ֆունկցիան օգտագործել չի կարելի ։
"""def title_func(mstr):
    md = []  
    for el in mstr.split():
        if len(el) == 0: 
            continue
        fr = el[0]  
        mn = el[1:]    
        if "a" <= fr <= "z":  
            fr = chr(ord(fr) - 32)  
            mn = mn.lower() 
        elif "A" <= fr <= "Z":  
            mn = mn.lower()  
        md.append(fr + mn)  
    return " ".join(md)
mstr = input("-- ")
l = title_func(mstr)
print(l)"""

#8 , Գրել ֆունկցիա որը որպես արգումենտ կստանա տողը և կվերադարձնի այն դարձված հակառակ։
"""def revers_func(mstr):
    return mstr[::-1]
ms=input()
print(revers_func(ms))"""

#9.Գրել ֆունկցիա որը որպես արգումենտ կստանա տող և թիվ։ Այն պետք է վերադարձնի տրված թվերի արանքում եղած ենթատողը։
"""def veradardz(mstr,start,end):
    return mstr[start:end]
ms=input("input word")
ind1=int(input("input num1"))
ind2=int(input("input num2, num2>num1"))
print(veradardz(ms,ind1,ind2))"""

#10 Գրել ֆունկցիա որը կվերադարձնի նախադասության ամենաերկար բառը։
"""def max_word(mstr):
    maxx=""
    for el in mstr.split():
        if len(el)>len(maxx):
            maxx=el
    return maxx
mstr=input()
print(max_word(mstr))"""        

#11Գրել ֆունկցիա որը կվերադարձնի նախադասության ամենաշատ օգտագործված տառը։
"""def max_letter(mstr):
    md={}
    for el in mstr:
        if el in md:
            md[el]+=1
        else:
            md[el]=1
    maxx=0
    mletter=""        
    for el1,el2 in md.items():
        if el2>maxx:
            maxx=el2
            mletter=el1

    return  mletter              
mstr=input()
print(max_letter(mstr))  """

#12Գրել ֆունկցիա որը կվերադարձնի նախադասության ամենաերկար բառում ամենաշատ օգտագործված տառը։
"""def max_word_max_letter(mstr):
    max_word = ""
    for el in mstr.split():
        if len(el) > len(max_word):
            max_word = el
    md = {}
    for el in max_word:
        if el in md:
            md[el] += 1
        else:
            md[el] = 1
    maxx = 0
    mletter = ""
    for el1, el2 in md.items():
        if el2 > maxx:
            maxx = el2
            mletter = el1
    return mletter
mstr = input()
print(max_word_max_letter(mstr))"""

#13Գրել ֆունկցիա որը որպես արգումենտ կստանա տող և թիվ։ Կվերադարձնի այդ թվին համապատասխն ինդեքսում եղած էլէմենտները  սկզբից և վերջից։
"""def index_letter(mstr,ind):
    if ind<len(mstr):
        return mstr[ind],mstr[-ind-1]
mstr=input()
num=int(input())
print(index_letter(mstr,num))"""

#15․ Գրել ֆունկցիա որը որպես արգումենտ կստանա թիվ և կստուգի պոլինդրոմ է այն թե ոչ
"""def polindrom(num):
    num=str(num)
    if num==num[::-1]:
       return True
    else:
        return False
num=int(input())
print(polindrom(num))"""
#16 Գրել ֆունկցիա որը որպես արգումենտ կստանա թիվ և կվերադարձնի  իրեն ամենամոտ պոլինդրոմ թիվը։
"""def get_polindrom(num):
    def is_polindrom(numm):
        numm=str(numm)
        return numm==numm[::-1]
    if is_polindrom(num):
        return num
    lower=num-1
    while True:
        if is_polindrom(lower):
            break
        lower-=1   
    higth=num+1
    while True:
        if is_polindrom(higth):
            break
        higth+=1
    if num - lower <= higth - num:
        return lower
    else:
        return higth
num=int(input())
print(get_polindrom(num))"""
#17Գրել ֆունկցիա որը որպես արգումենտ կստանա թիվ և կվերադարձնի իր առաջին և վերջին թվանշանների արտադրյալը։
"""def prod_f_l(num):
    numm=str(num)
    return int(numm[0])*int(numm[-1])      
num=int(input())
print(prod_f_l(num))"""
#18 Գրել ֆունկցիա որը որպես արգումենտ կստանա լիստ և կվերադարձնի լիստում եղած տողերի քանակությունը։
"""def count_list(ms):
    count=0
    for el in ms:
        if type(el) is str:
            count+=1
    return count
ms=input().split()
print(count_list(ms))"""       

#19 Գրել ֆունկցիա որը որպես արգումենտ կստանա լիստ և կվերադարձնի լիստում առկա թվերից առավելագույնը։
"""def list_max_dig(ms):
    maxx=0
    ml=[]
    for el in ms:
        if type(el) is int:
            ml.append(el)
    for el in ml:
        if el>maxx:
            maxx=el
    return maxx
ms=[1,3,4,56,"mkl",[3,4,"55"],True]  
print(list_max_dig(ms)) """
#20 Գրել ֆունկցիա որը որպես արգումենտ կստանա լիստ և կվերադարձնի այդ լիստում առկա երկնիշ զույգ թվերը։  
""""def list_dig_zuyg(ms):
    result = []
    for el in ms:
        if type(el) == int and 10 <= el <= 99 and el % 2 == 0:
            result.append(el)
    return result
ms=[67,98,"sdf","sdfk",90,77,63]
print(list_dig_zuyg(ms))"""
#21 Գրել ֆունկցիա որը որպես արգումենտ կստանա լիստ և կվերադարձնի այդ լիստում առկա թվերի միջին թվաբանականը։ 
""""def list_mij_tv(ms):
    for el in ms:
        ml=[]
        if type(el) is int:
           ml.append(el)
    return sum(ml) / len(ml)            
ms=[67,98,"sdf","sdfk",90,77,63]
print(list_mij_tv(ms))"""
#22 Գրել ֆունկցիա որը որպես առգումենտ կստանա տողերի լիստ և կվերադարձնի այդ տողերի երկարությունները պարունակող լիստ։
"""def list_len(ms):
    return [len(el) for el in ms if type(el) is str]
ms=["asd","sdfff","ddddfxsxx",67,900]
print(list_len(ms))"""
#23 Գրել ֆունկցիա որը որպես արգումենտ կստանա լիստ և կվերադարձնի լիստում առկա թվերը դասավորված նվազման կարգով։
"""def num_lower(ms):
    md=[]
    for el in ms:
        if type(el) is int:
            md.append(el)
            md.sort(reverse=True)
    return md        
ms=[887,76,"ddddfxsxx",67,900]
print(num_lower(ms))"""
#24Գրել ֆունկցիա որը որպես արգումենտ կստանա լիստ և կվերադարձնի լիստում առկա տողերը դասավորված երկարությունների նվազման կարգով:
"""def list_len_str_sort(ns):
    md=[]
    for el in ns:
        if type(el) is str:
           md.append(len(el))
    md.sort(reverse=True)
    return md
ms=["qwertyuio","qwerssa","z","qwerty","qrwe","sdf",3,4,5]       
print(list_len_str_sort(ms))"""
#25Գրել ֆունկցիա որը որպես արգումենտ կընդունի կընդունի տողերի լիստ և կվերադարձնի այն բառը որը կպարունակի ամենաշատ ձայնավորները։ 
"""def list_str(ms):
    d="aueoi"
    max_count_d=0
    result=""
    for el in ms:
        count_d=0
        if el in d:
            count_d+=1
    if  count_d>max_count_d:
        max_count_d=count_d
        result=el
    return el
ms=["qwertyuio","qwerssa","z","qwerty","qrwe","sdf","oueassai"]
print(list_str(ms))"""
#26 Գրել ֆունկցիա որը որպես արգումենտ կընդունի նախադասությունների լիստ և կվերադարձնի այն նախադասությունը որը կպարունակի ամենաշատ բառերը։
"""def long_sentence(ms):
    long=""
    maxx=0
    for el in ms:
        word=el.split()
        if len(word)>maxx:
            maxx=len(word)
            long=el
    return long
ms=["qwe ewe retr errf","qwe we werqwe wqer wer weer ere r re","wq we wqe wqe"]  
print(long_sentence(ms)) """
#27 Գրել ֆունկցիա որը որպես արգումենտ կստանա տող իրականում նախադասություն և կվերադարձնիայդ նախադասությունում առկա ամենամեծ թիվը ոչ թե թվանշանը ։
"""def sentence_max_num(ms):
    num = []
    for el in ms.split():  
        md = ''
        for n in el:
            if n.isdigit():
                md += n
        if md:
            num.append(int(md))   
    return max(num) if num else None
text = "sd sdf 234 45 567 45678 ssd 456788765"
print(sentence_max_num(text))"""  
#28 Գրել ֆունկցիա որը որպես արգումենտ կստանա բառարաններիլիստ՝մարդկանց նկարագրող և կվերադարձնի այն բառարանը որում մարդու տարիքն ամենամեծն է։
"""def people_info(people): 
    old = people[0]
    for el in people[1:]:
        if el["age"] > old["age"]:
            old = el
    return old
data = [
    {'name': 'Ani', 'surname': 'jj', 'age': 25},
    {'name': 'Bob', 'surname': 'Ch', 'age': 30},
]
print(people_info(data))"""
#29․ Գրել ֆունկցիա որը որպես արգումենտ կստանա բառարանների լիստ՝ուսանողների նկարագրող և կվերադարձնի այդ ուսանողների լիստըդասավորված աճման կարգով՝ ըստ միասվորների։
"""def student_info(ms):
     return sorted(ms, key=lambda x: x['score'])
data = [
    {'name': 'a','surename': 'aaa', 'score': 85},
    {'name': 'b','surename': 'bbb', 'score': 90},
    {'name': 'c','surename': 'ccc', 'score': 78}
]
print(student_info(data)) """       
#30.Գրել ֆունկցիա որը որպես արգումենտ կստանա բառարանների լիստ՝համալսարանների նկարագրող և կվերադարձնի այն համալսարանը որի ,անվանումն ամենաերկարն է։     
def long_name_univer(ms):
     return max(ms, key=lambda x:x['name'])
data=[{"name":"hfdh","country":"a"},{"name":'fg'}]
print(long_name_univer(data))