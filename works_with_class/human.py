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