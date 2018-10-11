# IAML Maxone Project
# 
# Members:
# 	Toshiki Kawai
# 	Edgar Handy
# 
# REF: https://gist.github.com/bellbind/741853
# REF: http://www.obitko.com/tutorials/genetic-algorithms/ga-basic-description.php

import random
import numpy as np

population_size = 100
number_of_bits = 32
max_iterations = 100
prob_crossover = 90
prob_mutation = 10
worst_fitness = -1
best_fitness = number_of_bits

class Chromosome:
	def __init__(self, bits):
		self.bits = bits
		self.fitness = self.bits.count('1')

	def __repr__(self):
		return '[Bits=%s, Score=%d]' % (self.bits, self.fitness)

	def __str__(self):
		return '[Bits=%s, Score=%d]' % (self.bits, self.fitness)

	def getBits(self):
		return self.bits

	def getFitness(self):
		return self.fitness

# Initialization
def initialize():
	return [Chromosome(str(format(random.randint(0, pow(2, number_of_bits)-1), '0{}b'.format(number_of_bits)))) for i in range(population_size)]

# Selection of parents
def select(population):
	parent_1 = []
	parent_2 = []

	# Sort list by fitness value to choose chromosome with a certain fitness value
	population.sort(key=lambda x: x.getFitness())
	fitness_list = [ch.getFitness() for ch in population]

	# Random sampling with weight to choose chromosome with a higher fitness vlaue
	distinct_fitness = list(set(fitness_list))
	distinct_count = [fitness_list.count(num) for num in distinct_fitness]
	prop = [fit / sum(distinct_fitness) for fit in distinct_fitness]
	
	for i in range(0, (int(population_size / 2))):
		start_1 = 0
		start_2 = 0
		end_1 = 0
		end_2 = 0

		val_1 = np.random.choice(distinct_fitness, p=prop)
		val_2 = np.random.choice(distinct_fitness, p=prop)

		for j in range(0, len(distinct_fitness)):
			if distinct_fitness[j] < val_1:
				start_1 += distinct_count[j]
				end_1 += distinct_count[j]
			if distinct_fitness[j] < val_2:
				start_2 += distinct_count[j]
				end_2 += distinct_count[j]
			if distinct_fitness[j] == val_1:
				end_1 += distinct_count[j]
			if distinct_fitness[j] == val_2:
				end_2 += distinct_count[j]

		id_1 = np.random.choice(np.arange(start_1, end_1))
		id_2 = np.random.choice(np.arange(start_2, end_2))

		parent_1.append(population[id_1])
		parent_2.append(population[id_2])

	return list(zip(parent_1, parent_2))

# Crossover
def crossover(parents):
	splice_index = int(number_of_bits / 2)
	child_1 = Chromosome(parents[0].getBits()[:splice_index] + parents[1].getBits()[splice_index:])
	child_2 = Chromosome(parents[1].getBits()[:splice_index] + parents[0].getBits()[splice_index:])
	return [child_1, child_2]

# Mutation
def mutate(chromosome):
	mut_index = random.randint(0, number_of_bits-1)
	mut_ch = Chromosome(chromosome.getBits()[:mut_index] + '0' + chromosome.getBits()[(mut_index+1):] if chromosome.getBits()[mut_index] == '1' else chromosome.getBits()[:mut_index] + '1' + chromosome.getBits()[(mut_index+1):])
	return mut_ch

def getBest(population):
	cur_best = population[0]

	for ch in population:
		if ch.getFitness() > cur_best.getFitness():
			cur_best = ch

	return cur_best

def getWorst(population):
	cur_worst = population[0]

	for ch in population:
		if ch.getFitness() < cur_worst.getFitness():
			cur_worst = ch

	return cur_worst


def main():
	# Initialize population
	pop = initialize()
	
	index = 0

	while index < max_iterations:
		next_pop = []

		parents = select(pop)
		
		for pair in parents:
			children = crossover(pair) if random.randint(0, 100) < prob_crossover else pair

			for ch in children:
				ch = mutate(ch) if random.randint(0, 100) < prob_mutation else ch
				next_pop.append(ch)

		pop = next_pop
		index = index + 1

		print('Gen ' + str(index) + '\n\t' + 'Best: ' + str(getBest(pop)) + '\n\tWorst: ' + str(getWorst(pop)))

		if getBest(pop).getFitness() == number_of_bits: 
			print('Found max value')
			quit()

	print('Reached max iterations')

if __name__ == '__main__':
	main()
