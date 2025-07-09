import random
from miloner_questions import Questions
from miloner_top_player import TopPlayer
def get_content(fname):
    with open(fname) as f:
        return f.readlines()
def get_land_words(ml):
    return [el.strip() for el in ml if el.strip()]
def add_question(fname):
    question = input("Add a question: ").strip()
    true = input("Add true answer: ").strip()
    false1 = input("Add wrong answer 1: ").strip()
    false2 = input("Add wrong answer 2: ").strip()
    false3 = input("Add wrong answer 3: ").strip()
    question_line = f"{question}? {true},{false1},{false2},{false3}\n"
    with open(fname, "a") as f:
        f.write(question_line)
    print("Question is added!\n")
def game(md):
    count = 0
    question_num = 1
    for line in md:
        data = Questions(line)
        count += data.game_logic(question_num)
        question_num += 1
    return count
def main():
    print(" 1 - Play game 2 - Add question")
    choice = input("Your choice: ").strip()
    while choice not in ['1', '2']:
        choice = input("Enter 1 or 2: ").strip()
    if choice == '1':
        username = input("Enter username: ")
        lines_text = get_content("questions.txt")
        questions = get_land_words(lines_text)
        random.shuffle(questions)
        questions = questions[:10]
        count = game(questions)
        top = TopPlayer("top_game_miloner.txt")
        top.saving_score_in_file(username, count)
    elif choice == '2':
        add_question("questions.txt")
if __name__ == "__main__":
    main()
