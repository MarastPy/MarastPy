import random

num_1 = random.randint(1,6)
num_2 = random.randint(1,6)


print("Press enter to throw a dice")
input()
input(num_1)
print("Press again to throw second dice")
input()
input(num_2)
soucet = num_1 + num_2
if soucet < 6:
    print("Your total is " + str(num_1 + num_2) + " silly buns")
else:
    print("Your total is " + str(num_1 + num_2) + " and you win silly buns")


