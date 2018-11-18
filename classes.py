class Airport:
	def __init__(self, _id='', _lat=0.0, _lon=0.0):
		self.id = _id
		self.lat = _lat
		self.lon = _lon

	def __str__(self):
		return self.id + ' '

# class Airports_manager:
# 	def __init__(self):
# 		self.airports = {}

# 	def add_airport(self, _airport):
# 		self.airports[airport.id] = _airport

# 	def size(self):
# 		return len(airports)

# 	def find(self, airport):
# 		return self.airports[airport.id]

class Aircraft:
	def __init__(self, _id='', _capacity=0, _price=0, _per_seat_price=0, _per_seat_loss=0, _max_available=0):
		self.id = _id
		self.capacity = _capacity
		self.curr_capacity = 0
		self.price = _price
		self.per_seat_price = _per_seat_price
		self.per_seat_loss = _per_seat_loss
		self.max_available = _max_available

	def __str__(self):
		return self.id + ' ' + str(self.capacity) + ' ' + str(self.price) + ' ' + str(self.per_seat_price) + ' ' + str(self.per_seat_loss) + ' ' + str(self.max_available)

# class Aircrafts_manager:
# 	def __init__(self):
# 		self.aircrafts = {}
# 		self.size = 0

# 	def add_aircraft(self, _aircraft):
# 		self.aircrafts[size] = _aircraft
# 		self.size += 1

class Trip:
	def __init__(self, _airport1='', _airport2='', _passengers1to2=0):
		self.airport1 = _airport1
		self.airport2 = _airport2
		self.passengers = _passengers1to2
		self.curr_passengers = 0

	def __str__(self):
		return self.airport1 + ' ' + self.airport2 + ' ' + str(self.passengers1to2) + ' ' + str(self.currPassengers)

