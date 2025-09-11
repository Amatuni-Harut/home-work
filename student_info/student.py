class Student:
    def __init__(self, id, name, grades):
        self.id = id
        self.name = name

        if type(grades) == str:
            self.grades = [int(x) for x in grades.split(",") if x]
        elif grades is None:
            self.grades = []
        else:
            self.grades = grades

    def calculate_average(self):
        if not self.grades:
            return 0
        average = sum(self.grades) / len(self.grades)
        return average

    def add_grade(self, grade):
        self.grades.append(grade)
        return {"msg": "grade added"} 

    def __str__(self):
        average = self.calculate_average()
        return f"the name student is {self.name}, id is {self.id} and average is {average:.2f}"