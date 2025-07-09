class TopPlayer:
    def __init__(self, filename):
        self.__filename = filename

    def saving_score_in_file(self, username, score):
        with open(self.__filename, "a") as f:
            f.write(f"{username}:{score}/10\n")
        print("Score saved")