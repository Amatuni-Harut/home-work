from human import Human
class Worker(Human):
    def __init__(self, fn, a, g):
        super().__init__(fn, a, g)
        self.__is_hired = False
    def hire(self):
        if not self.__is_hired:
            self.__is_hired = True
            print(f"{self.full_name} he was hired.")
        else:
            print(f"{self.full_name} hes already hired.")
    def fire(self):
        if self.__is_hired:
            self.__is_hired = False
            print(f"{self.full_name} he was fired.")
        else:
            print(f"{self.full_name} hes dont working.")
    @property
    def is_hired(self):
        return self.__is_hired