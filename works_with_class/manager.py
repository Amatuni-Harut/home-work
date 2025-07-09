from human import Human
from workers import Worker
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