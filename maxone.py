# REF: https://gist.github.com/bellbind/741853
# REF: http://www.obitko.com/tutorials/genetic-algorithms/ga-basic-description.php

#GROUP NUMBER 1

import random
import numpy as np
from operator import itemgetter

population_size = 100
number_of_bits = 16
prob_crossover = 90
prob_mutation = 10
limit = 100
gen = 1

def run():
    pop_size = population_size
    bits = number_of_bits
    population = initial_population(pop_size, bits) #population[num] = number 0~2^bits
    while True:
        fits_pops = [(fitness(ch),  ch) for ch in population] #count number of ones
        if check_stop(fits_pops): break
        population = breed_population(fits_pops)
    return population
    
def breed_population(fitness_population):
    parent_pairs = select_parents(fitness_population)
    size = len(parent_pairs)
    next_population = []
    for k in range(size) :
        parents = parent_pairs[k]
        cross = random.randint(0, 100) < prob_crossover
        children = crossover(parents) if cross else parents
        for ch in children:
            mutate = random.randint(0,100) < prob_mutation
            next_population.append(mutation(ch) if mutate else ch)
    return next_population

#Initialization
def initial_population(num, bits):
    return [str(format(random.randint(0, pow(2, bits)-1), '0{}b'.format(number_of_bits)))  for i in range(num)]

#Count Number of Ones
def fitness(chromosome):
    return chromosome.count('1')

#Check if Number of Ones = bits
def check_stop(fits_pops):
    global gen
    best = 0
    worst = number_of_bits
    
    #Find best chromosome
    for ch in fits_pops:
        if best < ch[0]:
            best = ch[0]
            best_ch = ch[1]
        if worst > ch[0]:
            worst = ch[0]
            worst_ch = ch[1]

    if gen == 1 or gen % 10 == 0 or best == number_of_bits:
        print("******************************")
        print(gen)
        print("Best:  ", best, best_ch)
        print("Worst: ", worst, worst_ch)
            
    gen += 1


    if best == number_of_bits:
        print("Complete")
        return True
    
    #If over max iterations    
    if gen > limit:
        print("Limit")
        return True
    return False

#Selection
def select_parents(fitness_population):
    parent1 = [] * (int)(population_size / 2)
    parent2 = [] * (int)(population_size / 2)

    #Sort fitness population by number of ones
    fitness_population.sort(key=itemgetter(0))

    #List of only values
    fit_values = [ch[0] for ch in fitness_population]

    #Find unique values for number of ones
    distinct_values = list(set(fit_values))
    #Count number of each unique value and create proportion (weight)
    distinct_count = [fit_values.count(num) for num in distinct_values]
    prop = [fit / sum(distinct_values) for fit in distinct_values]
    print(prop)
    for i in range(0, (int)(population_size / 2)):
        start1 = start2 = end1 = end2 = 0
        #Weighted random choice of unique value
        val1 = np.random.choice(distinct_values, p=prop)
        val2 = np.random.choice(distinct_values, p=prop)

        #Move through list to beginning of certain unique value
        for i in range(0, len(distinct_values)):
            if distinct_values[i] < val1:
                start1 += distinct_count[i]
                end1 += distinct_count[i]
            if distinct_values[i] < val2:
                start2 += distinct_count[i]
                end2 += distinct_count[i]
            if distinct_values[i] == val1:
                end1 += distinct_count[i]
            if distinct_values[i] == val2:
                end2 += distinct_count[i]

        #Random choice of id with certain unique value
        id1 = np.random.choice(np.arange(start1, end1))
        id2 = np.random.choice(np.arange(start2, end2))
        
        parent1.append(fitness_population[id1][1])
        parent2.append(fitness_population[id2][1])

    parents = list(zip(parent1, parent2))
    return parents

#Crossover
def crossover(parents):
    parent1 = parents[0]
    parent2 = parents[1]
    p = random.randint(0, number_of_bits-1)
    child1 = parent1[:p] + parent2[p:]
    child2 = parent2[:p] + parent1[p:]
    return (child1, child2)

#Mutation
def mutation(chromosome):
    p = random.randint(0, number_of_bits-1)
    new = chromosome[:p] + '0' + chromosome[(p+1):] if chromosome[p] == '1' else chromosome[:p] + '1' + chromosome[(p+1):]
    return new

if __name__ == "__main__":
    run()
