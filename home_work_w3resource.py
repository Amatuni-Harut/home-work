""" Write a Python class Employee with attributes like emp_id, emp_name, emp_salary,
 and emp_department and methods like calculate_emp_salary, emp_assign_department, and print_employee_details.
Use 'assign_department' method to change the department of an employee.
Use 'print_employee_details' method to print the details of an employee.
Use 'calculate_emp_salary' method takes two arguments: salary and hours_worked,
 which is the number of hours worked by the employee. If the number of hours
   worked is more than 50, the method computes overtime and adds it to the salary. Overtime is calculated as following formula  :"""
class Employee:
    def __init__(self, id, n, s, d):
        self.__empId = id
        self.__empName = n
        self.__empSalary = s
        self.__empDepartment = d
    @property
    def empId(self):
        return self.__empId
    @property
    def empName(self):
        return self.__empName
    @property
    def empSalary(self):
        return self.__empSalary
    @property
    def empDepartment(self):
        return self.__empDepartment
    def __str__(self):
        return f"{self.__empId} {self.__empName} {self.__empSalary} {self.__empDepartment}"
    def emp_assign_department(self, new_department):
        self.__empDepartment = new_department
        print(f"changing department to-- {self.__empDepartment}")
    def print_employee_details(self):
        print(f"Employee ID is {self.__empId}, name is {self.__empName}, salary is {self.__empSalary}, department is {self.__empDepartment}")
    def calculate_emp_salary(self, work_time):
            overtime = 0
            if work_time > 50:
                overtime = work_time - 50
                self.__empSalary =self.__empSalary+ (overtime*(self.__empSalary/50))
def main():
        worker1 = Employee(1, "John", 3500, "MDA")
        worker2 = Employee(2, "Anna", 4500, "NDA")
        worker3 = Employee(3, "Cris", 4800, "FDA")
        worker1.print_employee_details()
        worker2.calculate_emp_salary(55)
        worker3.emp_assign_department("RlA")
        worker2.print_employee_details()
        worker3.print_employee_details()
if __name__ == "__main__":
    main()
