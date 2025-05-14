user1_point = 3
user2_point = 3
nums = []
print("each  new number must start with the last digit of the imported one, except for the first one")
while user1_point > 0 and user2_point > 0:
    user1 = input("user1 enter num (100-999):")
    if len(user1) != 3 :
        print("enter a three-digit number")
        user1_point -= 1
    elif user1 in nums:
        print("this num is using")
        user1_point -= 1
    elif nums   and user1[0] != nums[-1][-1]:
        print("enter by condition")
        user1_point -= 1
    else:
        nums.append(user1)
    if user1_point <= 0:
        break
    user2 = input("user2 enter num(100-999):")
    if len(user2) != 3 :
        print("enter a three-digit number")
        user2_point -= 1 
    elif user2 in nums:
        print("this num is using")
        user2_point -= 1
    elif nums and user2[0] != nums[-1][-1]:
        print("enter by condition")
        user2_point -= 1
    else:
        nums.append(user2)
    if user2_point <= 0:
        break
print(user1_point,user2_point)
if user1_point <= 0 and user2_point <= 0:
    print("nothing")
elif user1_point <= 0:
    print("win user2")
else:
    print("win user1")    

    