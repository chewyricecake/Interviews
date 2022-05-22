import random
import math
import time

random.seed(1)  # Setting random number generator seed for repeatability

NUM_DRONES = 10000
AIRSPACE_SIZE = 128000 # 128 km
CONFLICT_RADIUS = 500  # Meters.

#Using a 1000x1000 square boundary with target drone in the center
def count_conflicts(drones, conflict_radius):
  start = time.time()
  conflicts = set()
  drones = sort_coordinate(drones) # Sort per x-coordinate
  for i in range(0, NUM_DRONES):
    bound = [] # Saving those who are near the target drone (within 1000X1000 square)
    if tuple(drones[i]) not in conflicts:
      for j in range(i+1, NUM_DRONES):#Travelling right
        x_distance = abs(drones[j][0]-drones[i][0])
        y_distance = abs(drones[j][1]-drones[i][1])
        #Save only those are within the boundary (1000X1000)
        if(x_distance<=CONFLICT_RADIUS and y_distance<=CONFLICT_RADIUS):
          bound.append(drones[j])
        #Stop the loop if the point is too far away
        if(x_distance>CONFLICT_RADIUS):
          break        
      for j in range(i-1,0,-1):#Travelling left
        x_distance = abs(drones[j][0]-drones[i][0])
        y_distance = abs(drones[j][1]-drones[i][1])
        if(x_distance<=CONFLICT_RADIUS and y_distance<=CONFLICT_RADIUS):
          bound.append(drones[j])
        if(x_distance>CONFLICT_RADIUS):
          break          
    for k in range(0, len(bound)):#Iterate through bound to count the # of conflicts
      if calculate_distance(drones[i],bound[k])<=CONFLICT_RADIUS:
        conflicts.add(tuple(drones[i]))
        conflicts.add(tuple(bound[k]))
  end = time.time()
  print ('Using a square boundary: ',end-start)
  return conflicts  

#Using a circular boundary with target drone in the center
def count_conflicts2(drones, conflict_radius):
  start = time.time()
  conflicts = set()
  drones = sort_coordinate(drones) # Sort per x-coordinate
  for i in range(0, NUM_DRONES):
    if tuple(drones[i]) not in conflicts:
      for j in range(i+1, NUM_DRONES):#Travelling right
        x_distance = abs(drones[j][0]-drones[i][0])
        #Using the circle formula (x-h)^2 + (y-k)^2 < r^2
        r_distance = ((drones[i][0]-drones[j][0])**2+(drones[i][1]-drones[j][1])**2)
        #Save only those are within the radius from the center
        if(r_distance<=CONFLICT_RADIUS**2):
          conflicts.add(tuple(drones[j]))
          conflicts.add(tuple(drones[i]))
        #Stop the loop if the point is too far away
        if(x_distance>CONFLICT_RADIUS):
          break       
      for j in range(i-1,0,-1):#Travelling left
        x_distance = abs(drones[j][0]-drones[i][0])
        r_distance = ((drones[i][0]-drones[j][0])**2+(drones[i][1]-drones[j][1])**2)
        if(r_distance<=CONFLICT_RADIUS**2):
          conflicts.add(tuple(drones[j]))
          conflicts.add(tuple(drones[i]))
        if(x_distance>CONFLICT_RADIUS):
          break          
  end = time.time()
  print ('Using a circular boundary: ',end-start)
  return conflicts

#Brute force going through each pair of drones possible
def count_conflicts3(drones, conflict_radius):
  start = time.time()
  conflicts = set()
  drones = sort_coordinate(drones)
  for i in range(0, NUM_DRONES):
    for j in range(i+1, NUM_DRONES):
      if calculate_distance(drones[i],drones[j])<=CONFLICT_RADIUS:
        conflicts.add(tuple(drones[i]))
        conflicts.add(tuple(drones[j]))
  end = time.time()
  print ('Using a brute force: ',end-start)
  return conflicts

def calculate_distance(drone_A, drone_B):#Eucledian distance between two points
  return abs(math.sqrt((drone_A[0]-drone_B[0])**2+(drone_A[1]-drone_B[1])**2))

def sort_coordinate(drones):#Quicksort
  if len(drones) <= 1:
    return drones
  pivot = drones[len(drones) // 2]
  lesser, equal, greater = [], [], []
  for drone in drones:
      if drone[0] < pivot[0]:
          lesser.append(drone)
      elif drone[0] > pivot[0]:
          greater.append(drone)
      else:
          equal.append(drone)
  return sort_coordinate(lesser) + equal + sort_coordinate(greater)

  
def gen_coord():
    return int(random.random() * AIRSPACE_SIZE)

positions = [[gen_coord(), gen_coord()] for i in range(NUM_DRONES)]
conflicts = count_conflicts(positions, CONFLICT_RADIUS)
print("Drones in conflict2: {}".format(len(conflicts)))
conflicts2 = count_conflicts2(positions, CONFLICT_RADIUS)
print("Drones in conflict: {}".format(len(conflicts2)))
conflicts3 = count_conflicts3(positions, CONFLICT_RADIUS)
print("Drones in conflict3: {}".format(len(conflicts3)))