# This file will contain the class defintion for Hashtable
# This class is in charge of initiating a hash table and
# allow users to insert and get values using a specific key. 

class Hashtable:
    
    def __init__(self, initial_size=10):
        # Default constructor with an initial hash table size parameter.
        # Initiates all buckets with an empty list.
        # The Space and Time complexity for this function is O(1)
        self.table = []
        for _ in range(initial_size):
            self.table.append([]) # Initialization
    
    def insert(self, key, value):
        # Inserts the passed parameter as a new item in the hash table
        # Determine where the item's index will be and place it in that index
        # The Space and Time complexity for this function is O(n)
        bucket = int(key) % len(self.table)
        bucket_value = [key, value]

        if self.table[bucket] == None:
            self.table[bucket] = [[bucket_value]]
        else:
            for value in self.table[bucket]:
                if value[0] == key:
                    value[1] = bucket_value
                    return
            self.table[bucket].append(bucket_value)
            return

    def get_value(self, key):
        # Gets the value that is located in the hash table using the given key
        # Find the item's index
        # The Space and Time complexity for this function is O(n)
        bucket = int(key) % len(self.table)

        if self.table[bucket] != None:
            for index in self.table[bucket]:
                if key in index:
                    return index[1]
        return None 

    def update(self, key, value):
        # This function updates the value at the current key index with the
        # newly given value.
        # The Space and Time complexity for this function is O(n)
        bucket = int(key) % len(self.table)

        try:
            for index in self.table[bucket]:
                if index[0] == key:
                    index[1] = value
        except:
            print('Error updating value')