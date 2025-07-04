class Top_player:
    def __init__(self,n,s):
        self.__name_P=n
        self.__score_P=s
    @property
    def name_player(self):
        return self.__name_P
    def score_player(self):
        return self.__score_P
    def __str__(self):
       return str(self.__name_P) + " ---" +str(self.__name_P) 
       
        