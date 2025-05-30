def get_conect(fname):
    with open(fname) as f:
        struct=f.read().strip().split("\n\n")
        game=[]
        for el in struct:
            line=el.strip().split("\n")
            gam=[list(el.strip()) for el in line if el.strip()]
            if len(gam)==3:
                game.append(gam)
        return game        

def game_logic(ms):
    for row in ms:
        if row[0] == row[1] == row[2] != " ":
            if row[0] == "x":
                return "win--x"
            elif row[0] == "0":
                return "win--0"
    for col in range(3):
        if ms[0][col] == ms[1][col] == ms[2][col] != " ":
            if ms[0][col] == "x":
                return "win-x"
            elif  ms[0][col]=="0":
                return "win-0"
    return "draw"


game=get_conect("x_and_0.txt")
g_count=1
for el in game:
    result=game_logic(el)
    print(g_count, "--", result)
    g_count+=1


