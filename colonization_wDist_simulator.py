#!/usr/bin/env python

#This script simulates the process of island colonization.  Specifically, it treats 
#colonization as a geographically explicit process with the probability of colonization 
#proportional to the distance from the source.  It calculates the number of events 
#necessary to achieve a given distribution---say to colonize 10 of 15 islands.

#The script requires an input file that provides (in the first line) the approapriate values
#for the number of islands potentially colonizable, followed by the number of islands to be
#colonized.  Following those two integers should be a white-space delimted table of 
#inter-island distances.  The matrix should be full, with 0's in the diagonal.  If there are
#10 islands, then the matrix should be a 10x10.


import random
import sys

nCells = 0	#the number of islands that can potentially be colonized
nPres = 0	#the number of islands to be colonized
nEvents = [] #the number of colonization events
origin = []	#list for storing the first island
avg = 0.0	#average number of colonization events required to generate the desired distribution
nReps = 10000	#the number of simulation replicates to carry out
file = open("Colonization.5of6islands.WithArea.txt", "a")	#the file that holds the number of events per replicate
x = 0	#index
v = 0	#index
dist = {}	#empty dictionary to hold distances
area = []	#empty list for island areas... will be used in selecting the colonist
nDists = 0	#the number of distances in the dataset
DistScaler = 1 #set to 2 to square distances, otherwise, use 1

#Distances among islands
distFile = open('Dist.NoOceanic.txt', "r")
areaFile = open('areas6islands.txt', 'r')

#populate the list of areas
for line in areaFile:
	line = line.strip()
	area.append(float(line))


z = 0
for line in distFile:
	values = line.split() #split the lines in the distFile on white space
	if z == 0:	#for the first line, read the values of nCells and nPres
		if len(values) != 2: #make sure there are exactly 2 values in the first line
			sys.exit("Expecting two values in first line of distance file.")
		nCells = int(values[0])
		nPres =  int(values[1])
	else:
		distances = [] #temporary container for distances
		if z > 0 and len(values) != nCells: #verify that the distance matrix has the correct dimensions
			sys.exit("The number of pairwise distances (" + str(len(values)) + ") in row " + str(z) + " is incorrect given the number of islands (" + str(nCells) + ").")
		for element in values:
			distances.append(float(element)**DistScaler)
		dist[z] = distances	#populate the dictionary of distances
	z = z + 1


##rescale the distances so that their sum is 1
y = 1
z = 0
for key in dist.keys():
	for i in dist[key]:
		if dist[y][z] != 0:
			dist[y][z] = 1.0/dist[y][z]	#first, invert the distances
		z = z + 1
	z = 0
	y = y + 1

y = 1
z = 0
for key in dist.keys():
	for i in dist[key]:
		if z != 0: #skip the sum for the first value in the list
			dist[y][z] = dist[y][z] + dist[y][z-1]	#calculate the cumulative sum on inverted distances
		z = z + 1
	z = 0
	y = y + 1

y = 1
z = 0
for key in dist.keys():
	scaler = 1.0/max(dist[y])
	for i in dist[key]:
		dist[y][z] = dist[y][z] * scaler #multiply by constant (scaler), so last value in the list is 1.0
		z = z + 1
	z = 0
	y = y + 1

# from dendropy import Tree, Node
# tree = Tree()
# extant_pop = []

###########################
###colonization stuff begins here
for z in range(nReps):
	k = 0 #counter of colonization events
	occupancy = []	#the list indicating whether the island (index = name) is occuppied or not
	colonized = []	#list of colonized islands
	
# 	Total_Area = 0
# 	for element in colonized:
# 		Total_Area = Total_Area + area('element')
# 	for element in 
	
	#first, fill the list with 1, then 0's.  1 means species present, 0 absent.
	firstIsland = random.randint(1, nCells) #randomly select an island to start from
	origin.append(firstIsland) #store the island where the process starts

# 	tree.seed_node.island_number = firstIsland
# 	extant_pop.append(tree.seed_node)

	for i in range(nCells):
		if (i + 1) == firstIsland:
			occupancy.append(1)
		else:
			occupancy.append(0)

	while len(colonized) < nPres: #run until all islands to be colonized have been colonized
		k = k + 1
		colonized = []	#list of colonized islands
		area_of_colonized_islands = [] #probabilites for selecting source of colonist
		for j in range(len(occupancy)):
			if occupancy[j] == 1:
				colonized.append(j + 1) #island names are 1 to n, not 0 to n

		if len(colonized) == 1:
			colonist = colonized[0]
		else:
			for element in colonized:
				area_of_colonized_islands.append(area[element-1])
			z = 0
			for element in area_of_colonized_islands:
				if z > 0:
					area_of_colonized_islands[z] = area_of_colonized_islands[z] + area_of_colonized_islands[z-1]
				z += 1
			
			z = 0
			for element in area_of_colonized_islands:
				area_of_colonized_islands[z] = area_of_colonized_islands[z] / area_of_colonized_islands[len(area_of_colonized_islands)-1]
				z += 1
				
			colonist = random.random()	#select a colonist
			z = 0
			for element in area_of_colonized_islands:
				if colonist <= element:
					colonist = colonized[z]
					break
				z += 1
	
# 		parent_pop = this_is_the_function_that_returns_the_source_population(extant_pop, colonist)
# 		stationary_child = Node()
# 		migrating_child = Node()
# 		stationary_child.island_number = parent_pop.island_number
#  
# 	
 		select_the_recipient = random.random()	#select the receiving island
# 
# 		migrating_child.island_number = select_the_recipient
#  
# 		parent_pop.add_child(migrating_child)
# 		parent_pop.add_child(stationary_child)
#  
# 		extant_pop.remove(parent_pop)
# 		extant_pop.append(migrating_child)
# 		extant_pop.remove(stationary_child)
		
		z = 0
		for i in dist[colonist]:
			if z > 0:
				if select_the_recipient <= dist[colonist][z]:
					if select_the_recipient > dist[colonist][z-1]:
						recipient = z + 1
						break
			else:
				if select_the_recipient < dist[colonist][z]:
						recipient = z + 1
						break
			z = z + 1

		if occupancy[recipient - 1] == 0:
			occupancy[recipient - 1] = 1

	nEvents.append(k)
#	print colonized
#	print occupancy
#	print k

#######colonization ends here
#######summary statistics are calculated below

#calculate the average number of colonization events necessary to fill the archipelago
#to the desired degree
for y in nEvents:
	avg = avg + y
avg = avg/len(nEvents)

#calculate the standard deviation of the mean # of colonization events
for r in nEvents:
	x = (r - avg) ** 2
	v = v + x
stdev = v / len(nEvents)
stdev = stdev ** 0.5

print "The average number of colonization events, given",
print nPres,
print "out of",
print nCells,
print "islands colonized is",
print avg
print "The standard deviation under these settings is",
print stdev
#print tree
for s in range(len(nEvents)):
	file.write(str(nEvents[s]) + "\t" + str(origin[s]) + "\n")
