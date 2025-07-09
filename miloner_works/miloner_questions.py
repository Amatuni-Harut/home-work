import random
class Questions:
    def __init__(self, line_separatel):
        split_line = line_separatel.split('?', 1)
        self.__text = split_line[0].strip()
        self.__answers = [el.strip() for el in split_line[1].split(',')]
        self.__true_answer = self.__answers[0]

    def __answers_randoming(self):
        random.shuffle(self.__answers)
    def game_logic(self, q_number):
        self.__answers_randoming()
        print(f"\nQuestion {q_number}: {self.__text}?")
        for i, answer in enumerate(self.__answers, 1):
            print(f"{i}. {answer}")
        num = input("Enter number (1-4): ")
        while not (num.isdigit() and 1 <= int(num) <= 4):
            print("Please enter a valid number between 1 and 4.")
            num = input("Enter number (1-4): ")
        num = int(num)
        if self.__answers[num - 1] == self.__true_answer:
            print("You win!")
            return 1
        else:
            print("Nope!")
            return 0
