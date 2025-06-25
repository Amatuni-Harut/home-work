class Number:
    def __init__(self,n):
        self.num=n
    def __str__(self):
        return str(self.num)  
    def __add__(self,other):
        summ=self.num+other.num
        return Number(summ)
    def __sub__(self, other):
        tar=self.num-other.num
        return Number(tar)
    def __mul__(self, other):         
        baz=self.num*other.num
        return Number(baz)
    def __truediv__(self, other): 
        baj=self.num/other.num
        return Number(baj)
n1=Number(10)
n2=Number(5)    
print(n1+n2)
print(n1-n2)
print(n1*n2)
print(n1/n2)