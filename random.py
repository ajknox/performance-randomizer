import random


# how many people are in each show
show_sizes = [8, 8]

improvers = [
    'Alice',
    'Bob',
    'Carol',
    'Eve',
    ]

random.shuffle(improvers)
go_twice = []
for i in [1,2,3]:
    go_twice.append(improvers.pop())
print(go_twice)


import random
seed = 91823712309487123 + 17
people = [
    'Alice',
    'Bob',
    'Carol',
    'Eve',
    ]
people.sort()
random.seed(seed)
random.shuffle(people)
print(people)
