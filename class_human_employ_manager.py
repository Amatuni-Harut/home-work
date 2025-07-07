from abc import ABC, abstractmethod
class Human(ABC):
    def __init__(self, fn, a, g):
        self.__full_name = fn
        self.__age = a
        self.__gender = g
    @property
    def full_name(self):
        return self.__full_name
    @property
    def age(self):
        return self.__age
    @property
    def gender(self):
        return self.__gender
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
class Manager(Human):
    def __init__(self, fn, a, g, c):
        super().__init__(fn, a, g)
        self.__company = c
        self.__workers = []
    @property
    def company(self):
        return self.__company
    @property
    def workers(self):
        return self.__workers
    def add_worker(self, worker: Worker):
        if worker in self.__workers:
            print(f"{worker.full_name} he working whith {self.full_name}.")
        elif len(self.__workers) >= 10:
            print(f"meneger{self.full_name} dont have 10 workers")
        elif worker.is_hired:
            print(f"{worker.full_name}he working other manager.")
        else:
            self.__workers.append(worker)
            worker.hire()
            print(f"{worker.full_name}he working this manager {self.full_name}.")
def main():
   worker1 = Worker("jhone smit", 25, "male")
   worker2 = Worker("Anna smit", 30, "famale")
   manager1 = Manager("karlos jekson", 40, "Male", "nmda")
   manager2 = Manager("mari manro", 38, "famale", "hpol")
   manager1.add_worker(worker1)
   manager1.add_worker(worker2)
main()
