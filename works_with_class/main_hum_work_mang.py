from workers import Worker
from manager import Manager
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
if __name__ == "__main__":
    main()
