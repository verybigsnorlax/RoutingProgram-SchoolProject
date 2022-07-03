# This file will define a class Packages, which will take the
# processed data and calculate and sort the packages within each truck
# using the greedy algorithm

from data_reader import get_data
from .hashtable import Hashtable

class Delivery:

    # Default constructor. Get data from data_reader and initialize variables
    # The Time and Space complexity is O(1)
    def __init__(self):
        self.table = Hashtable()
        self.trucks = [[], [], []]
        self.truck_index = [['0'], ['0'], ['0']]
        self.delivery = [[], [], []]
        self.delivery[0], self.delivery[1], self.delivery[2], self.distances, self.places, self.table = get_data()
        self.total_distance = [0, 0, 0]
        self.times = ['08:00:00', '09:05:00', '11:00:00']
        self.time_list = [[], [], []]
        # Call the recursive function for each truck and calculate the total distances
        for i in range(3):
            self.find_shortest_route(i+1, 0)
            for j in range(len(self.truck_index[i])-1):
                self.add_distance(int(self.truck_index[i][j]), int(self.truck_index[i][j+1]), i)
                self.time_taken(self.get_distance(int(self.truck_index[i][j]), int(self.truck_index[i][j+1])), i)
                h, m, s = self.trucks[i][j][8].split(':')
                h = int(h)
                m = int(m)
                h += sum(self.time_list[i]) // 60
                m += sum(self.time_list[i]) % 60

                if m >= 60:
                    m -= 60
                    h += 1
                self.trucks[i][j][9] = ':'.join((f'{["", "0"][len(str(h)) < 2]}{h}', f'{["", "0"][len(str(m)) < 2]}{m}', s))
                self.table.update(self.trucks[i][j][0], self.trucks[i][j])

    # Helper functions for the later recursion function

    # This method returns the total traveled distance when the truck
    # visits the given place
    # The Time and Space complexity is O(1)
    def add_distance(self, row, col, index):
        index = self.distances[row][col] == '-1'
        self.total_distance[index] += float([self.distances[row][col], self.distances[col][row]][index])

    # This method returns the distance between two locations given the row and col
    # The Time and Space complexity is O(1)
    def get_distance(self, row, col):
        index = self.distances[row][col] == '-1'

        return float([self.distances[row][col], self.distances[col][row]][index])
    
    # This method adds to the time list how long aech delivery took
    # The Time and Space complexity is O(1)
    def time_taken(self, distance, index):
        time = distance / 18
        minutes = round(time * 60)
        self.time_list[index].append(minutes)

    # This method is a recursive function that finds the shortest route for each
    # truck using the greedy algorithm. The main focus of the algorithm is to
    # find the next best location to visit based off of the current location
    # The Time and Space complexity is O(n)
    def find_shortest_route(self, truck_num, current_location):
        if self.delivery[truck_num-1] == []:
            return

        closest = 100.0
        location = 0
        optimal_package = None

        # Find the closest location
        for package in self.delivery[truck_num-1]:
            index = int(package[10])
            value = self.get_distance(current_location, index)
            if value <= closest:
                closest = value
                location = index
                optimal_package = package
        
        self.trucks[truck_num-1].append(optimal_package)
        self.truck_index[truck_num-1].append(int(optimal_package[10]))
        self.delivery[truck_num-1].pop(self.delivery[truck_num-1].index(optimal_package))
        self.find_shortest_route(truck_num, location)

    # This method returns the total distance traveled by all 3 trucks
    def get_total_distance(self):
        return sum(self.total_distance)
    
    # This method returns the hash table containing all the packages
    def get_table(self):
        return self.table