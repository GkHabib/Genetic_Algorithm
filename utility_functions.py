from math import sin, cos, sqrt, atan2, radians

def calc_distance(node1, node2):
	R = 6373.0
	lat1 = radians(node1.lat)
	lon1 = radians(node1.lon)
	lat2 = radians(node2.lat)
	lon2 = radians(node2.lon)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c
	return distance
