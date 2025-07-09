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
            print(f"{self.full_name} has been hired.")
        else:
            print(f"{self.full_name} is already hired.")

    def fire(self):
        if self.__is_hired:
            self.__is_hired = False
            print(f"{self.full_name} has been fired.")
        else:
            print(f"{self.full_name} is not working.")

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

    def add_worker(self, worker):
        if worker in self.__workers:
            print(f"{worker.full_name} is already working with {self.full_name}.")
        elif len(self.__workers) >= 10:
            print(f"Manager {self.full_name} cannot have more than 10 workers.")
        elif worker.is_hired:
            print(f"{worker.full_name} is already working with another manager.")
        else:
            self.__workers.append(worker)
            worker.hire()
            print(f"{worker.full_name} now works for manager {self.full_name}.")

    def removing_worker(self, worker):
        if worker in self.__workers:
            self.__workers.remove(worker)
            worker.fire()
            print(f"{worker.full_name} no longer works with {self.full_name}.")
        else:
            print(f"{worker.full_name} does not work with {self.full_name}.")

def main():
    worker1 = Worker("John Smith", 25, "male")
    worker2 = Worker("Anna Smith", 30, "female")
    manager1 = Manager("Carlos Jackson", 40, "male", "NMDA")
    manager2 = Manager("Mary Monroe", 38, "female", "HPOL")

    manager1.add_worker(worker1)
    manager1.add_worker(worker2)
    manager2.add_worker(worker1)  

    manager1.removing_worker(worker1)
    manager2.add_worker(worker1)  

main()
