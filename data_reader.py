# This file reads the 3 csv files to filter the data and process the data
# into information that can be sent to the class Packages.

from pyclass.hashtable import Hashtable
import csv

# This section will open the packages.csv file that contains the basic information
# about each package and store each package data into the hash table instance.

with open('./data/packages.csv') as file:
    data = csv.reader(file, delimiter=',')

    # Instantiate a hashtable object
    hashtable = Hashtable()

    # 3 lists to hold the package for each of the 3 trucks
    truck1 = []
    truck2 = []
    truck3 = []

    # Iterate through each line of the csv file and store each tuple
    # into the hashtable and into the trucks
    # The Space and Time complexity for this is O(N)
    for line in data:
        package_id, address, city, state, zipcode, delivery, size, note = line
        time = ""
        delivered_time = ""
        location = ""
        status = "At hub"

        key = package_id
        value = [package_id, address, city, state, zipcode, delivery, size, note, time, delivered_time, location, status]

        # The packages will now be placed in the truck that meets the requirements
        # such as some packages requiring to be in the same truck as other specific
        # packages and some packages may be delayed or may have a required delivery
        # time. The if and else conditions will help filter out which packages will
        # go on which trucks.
        # The Space and Time complexity for each if statement is O(1)
        # If the package has a required delivered by time add to the first truck
        if value[5] != 'EOD' and ('Must be delivered' in value[7] or 'None' in value[7]):
            value[8] = '08:00:00'
            truck1.append(value)
        
        # If the flight is delayed and package arrives late or the note says "Can only be on truck 2"
        # then add the package to the second truck
        elif 'Delayed' in value[7] or 'Can only be on truck 2' in value[7]:
            value[8] = '09:05:00'
            truck2.append(value)
        
        # The package with the incorrect address information gets filtered here
        elif 'Wrong address listed' in value[7]:
            # Fix the address to the correct address
            value[2], value[5] = '410 S State St', '84111'
            value[8] = '11:00:00'
            truck3.append(value)
        
        # Finally, some packages do not have a specific requirement so those
        # packages can be delivered a little later, so they will be added to the final truck
        # Check to make sure that the package gets placed in the truck with less packages
        else:
            if len(truck3) <= 16:
                value[8] = '11:00:00'
                truck3.append(value)
            else:
                value[8] = '09:05:00'
                truck2.append(value)
        
        hashtable.insert(package_id, value)

# This section will unpack the distances and places csv

with open('./data/distances.csv') as file:
    distances = list(csv.reader(file, delimiter=','))

# Get the location index value for each package
with open('./data/places.csv') as file:
    places = list(csv.reader(file, delimiter=','))

    trucks = truck1 + truck2 + truck3
    for package in trucks:
        for value in places:
            if package[1] == value[2]:
                package[10] = value[0]

# This method will return the lists of data that were unpacked above
def get_data():
    return truck1, truck2, truck3, distances, places, hashtable