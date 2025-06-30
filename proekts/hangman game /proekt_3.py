"""3 Hangman Game: Implement the classic word-guessing game, Hangman, where
players try to guess a hidden word one letter at a time. Display the current state
of the word, the letters guessed so far, and allow a limited number of incorrect
guesses before the game ends."""

import random
import os
gallows_picture = [  
    r"""
    +---+
    |   |
        |
        |
        |
       ===
    """,
    r"""
    +---+
    |   |
    O   |
        |
        |
       ===
    """,
    r"""
    +---+
    |   |
    O   |
    |   |
        |
       ===
    """,
    r"""
    +---+
    |   |
    O   |
   /|   |
        |
       ===
    """,
    r"""
    +---+
    |   |
    O   |
   /|\  |
        |
       ===
    """,
    r"""
    +---+
    |   |
    O   |
   /|\  |
   /    |
       ===
    """,
    r"""
    +---+
    |   |
    O   |
   /|\  |
   / \  |
       ===
    """
]
def get_conect(fname):
    try:
        with open(fname, "r") as f:
            word=[line.strip().lower() for line in f if line.strip()]
            return word
    except FileNotFoundError:
        print(f"Error: file '{fname}' not found at path: {os.path.abspath(fname)}")
        return None
def get_game_logic(ms): 
    if not ms:
        print("dont word in file")
    correct_word=random.choice(ms)    
    used_letters=[]       
    fales=0
    true_letter=["_"]*len(correct_word)
    while fales < 6 and "_" in true_letter:
        print(gallows_picture[fales])
        print("Word:", " ".join(true_letter))
        print("Used letters:", ", ".join(used_letters))

        letter=input("enter the letter").lower()
        if len(letter) != 1 or not letter.isalpha():
            print("Please enter a single letter")
            continue
        if letter in used_letters:
            print("This letter is already used")
            continue
        used_letters.append(letter)
        if letter in correct_word:
            for i in range(len(correct_word)):
                if correct_word[i]==letter:
                    true_letter[i]=letter
            print("this letter already there")
        else:
            fales+=1
            print("not this letter in word")
    if "_" not in true_letter:
        print("you win word is",correct_word)
    else:
        print(gallows_picture[6])
        print("you lose, the word is--",correct_word)    
def main():
    file_path = os.path.join(os.getcwd(), r"h_g.txt")
    data = get_conect(file_path)
    if data:   
       get_game_logic(data)
if __name__ == "__main__":       
    main()    


   




