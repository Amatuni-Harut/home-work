#milonater game using def funct and files

import random
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
write_file("top.txt",username,count)


class Questions:
    def __init__(self,Qline):
        self.text
        answer=Qline.split("?",1)
        self.answer= [el.strip()for el in answer.spit(",")]
        self.true_answer = self.answers[0]
    def  shuffle_question(self):
        random.shuffle(self.answer)
    def  Questions_struktur(self,num_question):
        self.shuffle_question() 
        print(f"\nQuestion {num_question}: {self.text}?") 
        el = 1
        for answ in self.answers:
            print(f"{el}. {answ}")
        el += 1
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