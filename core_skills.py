import random

rand_list = [random.randint(1, 20) for _ in range(20)]

list_comprehension_below_10 = [i for i in rand_list if i < 10]

list_comprehension_below_10 = filter(lambda x: x < 10, rand_list)
