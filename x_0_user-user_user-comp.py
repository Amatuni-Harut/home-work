#game 2 players
"""def creating_board(ms):
    for row in ms:
        print("-" * 9)
        print(" | ".join(row))
def get_winer_cheker(ms):
    for row in ms:
        if row[0] == row[1] == row[2] != " ":
                return row[0]
    for col in range(3):
        if ms[0][col] == ms[1][col] == ms[2][col] != " ":
                return  ms[0][col]
    if ms[0][0] == ms[1][1] == ms[2][2] != " ":
        return ms[0][0]
    if ms[0][2] == ms[1][1] == ms[2][0] != " ":
        return ms[0][2]    
    return None
def get_turn_player(ms,f_Player):
    while True:
        print("enter your turn cordinats",f_Player)
        row = int(input("ente number(0-2)"))
        col = int(input("ente number(0-2)"))
        cordinats=[0,1,2]
        if row not in cordinats and col not in cordinats: 
            print("eror")
            continue
        if ms[row][col] !=" ":
            print("enter new cordinats")
            continue
        return row,col 
        
def game_logic():
    ms= [[" "]*3 for _ in range(3)]
    f_Player="x"
    while True:
        creating_board(ms)
        row,col=get_turn_player(ms,f_Player)
        ms[row][col]=f_Player
        winer=get_winer_cheker(ms)
        if winer:
            creating_board(ms)
            return winer
        draw=True
        for row in ms:
            for el in row:
                if el== " ":
                    draw=False
                    break
            if not draw:
                break    
        if    draw:
            creating_board(ms)
            return "draw"
        if f_Player == "x":
            f_Player = "o"
        else:
            f_Player = "x"
 
def main():
    result=game_logic()
    print(result)
main()   """

#game playaer computer       
import random

def creating_board(ms):
    for row in ms:
        print("-" * 9)
        print(" | ".join(row))
def get_winer_cheker(ms):
    for row in ms:
        if row[0] == row[1] == row[2] != " ":
                return row[0]
    for col in range(3):
        if ms[0][col] == ms[1][col] == ms[2][col] != " ":
                return  ms[0][col]
    if ms[0][0] == ms[1][1] == ms[2][2] != " ":
        return ms[0][0]
    if ms[0][2] == ms[1][1] == ms[2][0] != " ":
        return ms[0][2]    
    return None
def get_turn_player(ms,f_Player):
    while True:
        print("enter your turn cordinats",f_Player)
        row = int(input("ente number(0-2)"))
        col = int(input("ente number(0-2)"))
        cordinats=[0,1,2]
        if row not in cordinats and col not in cordinats: 
            print("eror")
            continue
        if ms[row][col] !=" ":
            print("enter new cordinats")
            continue
        return row,col 
def get_turn_computer(ms):
    comp_turn = [(row, col) for row in range(3) for col in range(3) if ms[row][col] == " "]
    return random.choice(comp_turn)   

def game_logic():
    ms= [[" "]*3 for _ in range(3)]
    f_Player="x"
    while True:
        creating_board(ms)
        if f_Player == "x":
            row, col = get_turn_player(ms, f_Player)
        else:
            print("the turn of computer")
            row, col = get_turn_computer(ms)
        ms[row][col] = f_Player  
        winer=get_winer_cheker(ms)
        if winer:
            creating_board(ms)
            return winer
        draw=True
        for row in ms:
            for el in row:
                if el== " ":
                    draw=False
                    break
            if not draw:
                break    
        if    draw:
            creating_board(ms)
            return "draw"
        if f_Player == "x":
            f_Player = "o"
        else:
            f_Player = "x"
def main():
    result = game_logic()
    if result == "draw":
        print("draw")
    elif result == "x":
        print("You win")
    else:
        print("Computer win")
main()