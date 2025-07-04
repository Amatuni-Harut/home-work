class MyList:
    def __init__(self, iterable=None):
        if iterable is None:
            self.data = []
        else:
            self.data = [x for x in iterable]

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        self.data[index] = value

    def append(self, value):
        new_data = [0] * (len(self.data) + 1)
        for i in range(len(self.data)):
            new_data[i] = self.data[i]
        new_data[-1] = value
        self.data = new_data

    def __str__(self):
        return str(self.data)
ml = MyList([1, 2, 3])
ml[1] = 10
print(ml) 