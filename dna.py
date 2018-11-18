from classes import *
import constants
from random import randint, random
from utility_functions import calc_distance

class Gen:
	def __init__(self, _size, _credit=0):
		self.gen = [0] * _size
		self.fitness = 0
		self.curr_credit = _credit
		self.cost = 0
		self.size = _size

	def set_fitness(self, value):
		self.fitness = value

	def get_fitness(self):
		return self.fitness

	def __str__(self):
		return str(self.gen) + '\n' + str(self.fitness)

	def mate(self, sec_gen):
		index = randint(1, self.size)
		new_gen = Gen(self.size)
		for i in range(self.size):
			if(i < index):
				new_gen.gen[i] = self.gen[i]
			else:
				new_gen.gen[i] = sec_gen.gen[i]
		return new_gen

	def mutate(self, max):
		for i in range(self.size):
			prob = random()
			if prob	< constants.MUTATION_PROB:
				self.gen[i] = randint(0 , max)

class DNA:
	def __init__(self, _credit=1000000000):
		self.aircrafts = {}
		self.airports = {}
		self.trips = {}
		self.aircrafts_size = 0
		self.airports_size = 0
		self.trips_size = 0
		self.credit = _credit

	def create_elements(self):
		aircrafts_file = open('aircrafts.txt', 'r')
		airports_file = open('airports.txt', 'r')
		trips_file = open('passengers.txt', 'r')

		i = 0
		while True:
			try:
				line = aircrafts_file.readline()
				if(line == ''): raise(Exception("End of File of aircrafts!"))
				line = line[:-1]
				line = list(line.split(' '))
				temp_aircraft = Aircraft(line[0], int(line[1]), int(line[2]), int(line[3]), int(line[4]), int(line[5]))
				for _ in range(temp_aircraft.max_available):
					self.aircrafts[i] = temp_aircraft
					i = i + 1
					self.aircrafts_size += 1

			except Exception as e:
				break
			else:
				pass
			finally:
				pass

		while True:
			try:
				line = airports_file.readline()
				if(line == ''): raise(Exception("End of File of airports!"))
				line = line[:-1]
				line = list(line.split(' '))
				temp_airport = Airport(line[0], float(line[1]), float(line[2]));
				self.airports[temp_airport.id] = temp_airport
				self.airports_size += 1

			except Exception as e:
				break
			else:
				pass
			finally:
				pass

		i = 0
		while True:
			try:
				line = trips_file.readline()
				if(line == ''): raise(Exception("End of File of trips!"))
				line = line[:-1]
				line = list(line.split(' '))
				temp_trip1 = Trip(line[0], line[1], int(line[2]))
				temp_trip2 = Trip(line[1], line[0], int(line[3]))
				self.trips[i] = temp_trip1
				i += 1
				self.trips[i] = temp_trip2
				i += 1
				self.trips_size += 2
			except Exception as e:
				self.trips_size -=1
				break
			else:
				pass
			finally:
				pass

	def print_elements(self):
		for elem in self.aircrafts:
			print(self.aircrafts[elem])

		for elem in self.airports:
			print(self.airports[elem])

		# for elem in self.trips:
		# 	print(self.trips[elem])

	def print_population(self):
		for elem in self.population:
			print(elem.gen)
		print('population size is :', len(self.population))

	def create_population(self):
		self.population = []
		gen_size = self.aircrafts_size

		for count in range(constants.POPULATION_SIZE):
			temp_gen = Gen(gen_size, self.credit)
			for i in range(gen_size):
				temp_gen.gen[i] = randint(0, self.trips_size)
			self.population.append(temp_gen)

	def crossover(self):
		self.childs = []

		s = int((80 * constants.POPULATION_SIZE) / 100)

		for i in range(s):
			parent1 = self.population[randint(0, constants.POPULATION_SIZE-1)]
			parent2 = self.population[randint(0, constants.POPULATION_SIZE-1)]
			while(parent2 == parent1):
				parent2 = self.population[randint(0, constants.POPULATION_SIZE-1)]
			child = parent1.mate(parent2)
			child.curr_credit = self.credit
			self.childs.append(child)


	def replace_new_population(self):
		new_population = []
		s = int(20 * constants.POPULATION_SIZE / 100)
		for i in range(constants.POPULATION_SIZE):	
			if(i < s):
				new_population.append(self.population[i])
			else:
				new_population.append(self.childs[i-s])
		self.population = new_population

	def mutate(self):
		for child in self.childs:
			child.mutate(self.trips_size)

	def calc_fitness(self):
		for gen in self.population:
			gen_fitness = 0
			for i in range(self.airports_size):
				self.trips[gen.gen[i]].curr_passengers = self.trips[gen.gen[i]].passengers
				self.aircrafts[i].curr_capacity = self.aircrafts[i].capacity

			for i in range(self.airports_size):
				aircraft = self.aircrafts[i]

				if(gen.curr_credit > aircraft.price):
					trip =  self.trips[gen.gen[i]]
					airport1 = self.airports[trip.airport1]
					airport2 = self.airports[trip.airport2]
					distance = calc_distance(airport1, airport2)
					gen.curr_credit = gen.curr_credit - aircraft.price
					gen.cost += aircraft.price
					if(trip.curr_passengers > 0):
						if(trip.curr_passengers > aircraft.curr_capacity):
							trip.curr_passengers = trip.curr_passengers - aircraft.curr_capacity
							gen_fitness += (aircraft.curr_capacity * aircraft.per_seat_price * distance / 100)
							aircraft.curr_capacity = 0
						else:
							trip.curr_passengers = 0
							gen_fitness += (trip.passengers * aircraft.per_seat_price * distance / 100)
							aircraft.curr_capacity -= trip.passengers
							gen_fitness -= ((aircraft.curr_capacity) * aircraft.per_seat_loss * distance / 100)

			gen.fitness = gen_fitness

	def sort_by_fitness(self):
		self.population.sort(key=lambda x: x.fitness, reverse=True)

	def print_fitness(self):
		for gen in self.population:
			print(gen.fitness, end=', ')
	def get_max_fitness(self):
		return self.population[0].fitness

	def print_answer(self):
		conclusion = answers()
		gen = self.population[0]

		for i in range(self.aircrafts_size):
			aircraft = self.aircrafts[i]
			trip =  self.trips[gen.gen[i]]
			new_answer = answer(trip.airport1, trip.airport2)
			new_answer.aircrafts.append(answer_aircraft(aircraft.id))
			conclusion.add_answer(new_answer)

		print(gen.cost)
		print(gen.fitness)
		conclusion.print_res()


class answers:
	def __init__(self):
		self.answers_list = []

	def add_answer(self, new_answer):
		for answer in self.answers_list:
			if(answer.airport1 == new_answer.airport1 and answer.airport2 == new_answer.airport2):
				answer.add_answer_aircraft(new_answer.aircrafts[0])
		self.answers_list.append(new_answer)
	def sort(self):
		for ans in self.answers_list:
			ans.sort()
		self.answers_list.sort(key=lambda x: x.airport1, reverse=False)

	def print_res(self):
		for ans in self.answers_list:
			print(ans)
	


class answer:
	def __init__(self, _airport1, _airport2):
		self.airport1 = _airport1
		self.airport2 = _airport2
		self.aircrafts = []

	def add_answer_aircraft(self, new_aircraft):
		for aircraft in self.aircrafts:
			if(aircraft.id == new_aircraft.id):
				aircraft.num += 1
				return
		self.aircrafts.append(new_aircraft)		

	def sort(self):
		self.aircrafts.sort(key=lambda x: x.id, reverse=False)

	def __str__(self):
		string = ''
		string = self.airport1 + ' ' + self.airport2 + ' '
		for airc in self.aircrafts:
			string += airc.__str__()
			string += ', '
		return string

class answer_aircraft:
	def __init__(self, _id):
		self.id = _id
		self.num = 1

	def __str__(self):
		return str(self.id) + ' ' + str(self.num)