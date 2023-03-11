import random


# Stage 2 simulation
for i in range (1000):
    output = ""
    output += str(random.randrange(80, 100))
    output += " "
    output += str(random.randrange(0, 50))
    output += " "
    output += str(random.randrange(3, 5))
    output += " "
    output += output[-2]
    output += " "
    output += str(random.randrange(3, 5))
    print(output)


# # Stage 3 simulation
# for i in range (1000):
#     output = ""
#     output += str(random.randrange(50, 100))
#     output += " "
#     output += str(random.randrange(0, 60))
#     output += " "
#     output += str(random.randrange(4, 7))
#     output += " "
#     output += output[-2]
#     output += " "
#     output += str(random.randrange(4, 7))
#     print(output)

# # Stage 4 simulation
# for i in range (1000):
#     output = ""
#     output += str(random.randrange(1, 100))
#     output += " "
#     output += str(random.randrange(0, 50))
#     output += " "
#     output += str(random.randrange(7, 8))
#     output += " "
#     output += output[-2]
#     output += " "
#     output += str(random.randrange(7, 8))
#     print(output)