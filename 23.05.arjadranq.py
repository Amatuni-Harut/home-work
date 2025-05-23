def get_content(fname):
    f=open(fname)
    return f.read()
def get_land_words(ml):
    return ml
def full_revers(ml):
    n_ml=ml[::-1]
    return " ".join( n_ml)
def word_revers(ml):
    md=[]
    for el in ml.split():
        n_el=el[::-1]
        md.append(n_el)
    return " ".join( md )
def titllnig(ml):
    md=[]
    for el in ml.split():
        n_el=el.title()
        md.append(n_el)
    return md
def upering(ml):
    md=[]
    for el in ml.split():
        n_el=el.upper()     
        md.append(n_el)
    return " ".join(md)
def up_low_tar(ml):
    v="uaeio"
    md=[]
    for el in ml.split():
        new_el = []
        for el1 in el:
            if el1.lower() in v:  
                new_el.append(el1.upper())
            else:
                new_el.append(el1.lower())
        md.append(''.join(new_el))
    return ' '.join(md)   
def write_into_file(fname, tmp):
    f = open(fname, "a")
    for el in tmp:
        f.write(el )
    f.write("\n")    
    f.close()

data=get_content("23.05.txt")
word=get_land_words(data)
f=full_revers(word)
t=titllnig(word)
u=upering(word)
v=up_low_tar(word)
open("res.txt", "w").close()

write_into_file("res.txt",f)  
write_into_file("res.txt",t)
write_into_file("res.txt",u)
write_into_file("res.txt",v)    