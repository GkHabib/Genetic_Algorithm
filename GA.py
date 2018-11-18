from dna import *
import constants
import sys

class GA:
	def __init__(self, credit=10000000000):
		self.dna = DNA(credit)
		self.cycle_without_fitness_change = 0
		self.fitness = 0

	def start(self):
		self.dna.create_elements()
		self.dna.create_population()
		self.dna.calc_fitness()
		self.dna.sort_by_fitness()
		self.fitness = self.dna.get_max_fitness()
		
	def one_cycle_run(self):
		self.dna.crossover()
		self.dna.mutate()
		self.dna.replace_new_population()
		self.dna.calc_fitness()
		self.dna.sort_by_fitness()
		self.fitness = self.dna.get_max_fitness()

	def check_ending_condition(self, prev_fitness):
		if(prev_fitness == self.fitness):
			self.cycle_without_fitness_change += 1
		else:
			self.cycle_without_fitness_change = 0
		
		if(self.cycle_without_fitness_change > constants.CYCLE_NUM):
			return True
		else:
			return False

	def run(self):
		self.start()
		prev_fitness = self.fitness
		while not(self.check_ending_condition(prev_fitness)):
			prev_fitness = self.fitness
			self.one_cycle_run()
		self.dna.print_answer()


algorithm = GA(int(sys.argv[1]))

algorithm.run()