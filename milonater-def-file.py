#milonater game using def funct and files

"""import random
def get_content(fname):
    f=open(fname)
    return f.readlines()
def get_land_words(ml):
    return [el.strip() for el in ml if el.strip()]
def game_logic(i, question_num):
    i_txt, ans1 = i.split('?', 1)  
    answers = [el.strip() for el in ans1.split(',')]
    true_answer = answers[0]
    random.shuffle(answers)
    print(f"\nQuestion {question_num}: {i_txt.strip()}?")
    print("1.", answers[0])
    print("2.", answers[1])
    print("3.", answers[2])
    print("4.", answers[3])
    num = input("input (1-4): ")
    while not (num.isdigit() and 1 <= int(num) <= 4):
        print("Please enter a valid number between 1 and 4.")
        num = input("input (1-4): ")
    num = int(num)
    if answers[num - 1] == true_answer:
        print("you win")
        return 1
    else:
        print("no")
        return 0
def write_file(fname,username,count):
        f=open(fname,"a")
        f.write(f"{username}:{count}/10\n")
        f.close()    
username=input("input username--")
questions = get_content("questions.txt")
questions = get_land_words(questions)
random.shuffle(questions)
questions = questions[:10]
count = 0
question_num = 1
for i in questions:
    count += game_logic(i, question_num)
    question_num += 1
#username=input("input username--")
write_file("top.txt",username,count)"""



import random
from miloner_top_player import Top_player
class Questions:
    def __init__(self, line_separatel):
        split_line = line_separatel.split('?', 1)
        questions_Miloner = split_line[0]
        answers_Miloner = split_line[1]
        self.text = questions_Miloner.strip()
        self.answers = [el.strip() for el in answers_Miloner.split(',')]
        self.true_answer = self.answers[0]
    def answers_randoming(self):
        random.shuffle(self.answers)
    def game_logic(self, q_number):
        self.answers_randoming()
        print(f"\nQuestion {q_number}: {self.text}?")
        el = 1
        for answer in self.answers:
            print(f"{el}. {answer}")
            el += 1
        num = input("enter number  (1-4): ")
        while not (num.isdigit() and 1 <= int(num) <= 4):
            print("Please enter a valid number between 1 and 4.")
            num = input("input (1-4): ")
        num = int(num)
        if self.answers[num - 1] == self.true_answer:
            print("you win")
            return 1
        else:
            print("no")
            return 0
def get_content(fname):
    with open(fname) as f:
        return f.readlines()
def get_land_words(ml):
    return [el.strip() for el in ml if el.strip()]
def write_file(fname, username, count):
    with open(fname, "a") as f:
        f.write(f"{username}:{count}/10\n")

        
def game(md):
    count = 0
    question_num = 1
    for line in md:
        data = Questions(line)
        count += data.game_logic(question_num)
        question_num += 1
    return count
def add_question(fname):
    question = input("add a questin): ").strip()
    true = input("add true reply ").strip()
    false1 = input("add reply 1 ").strip()
    false2 = input("add rely 2 ").strip()
    false3= input("add repy 3 ").strip()
    question_line = f"{question}? {true},{false1},{false2},{false3}\n"
    with open(fname, "a") as f:
        f.write(question_line)
    print("question is added!\n")
def main():
    def main():
    print("make a choice, 1 is game, 2 is redoction and add question ")
    choice = input("your choice ").strip()
    while choice not in ['1', '2']:
        choice = input("enter 1 or 2").strip()
    if choice == '1':  
        username = input("input username--")
        lines_text = get_content("questions.txt")
        questions = get_land_words(lines_text)
        random.shuffle(questions)
        questions = questions[:10]
        count=game(questions)
        write_file("top_game_miloner.txt", username, count)     
    elif  choice == '2':
        add_question("questions.txt")
if __name__ == "__main__":
    main()

















