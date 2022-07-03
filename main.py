# Brian Kim 001474065

from pyclass.delivery import Delivery
from datetime import datetime as d

# This method will print the menu options for the user to choose
def menu():
    print('\n\n')
    print('**Menu option**')
    print('Choose to view:')
    print('(s)pecific package\n(a)ll packages\n(q)uit\n')

    user_input = input('Your choice: ')
    return user_input

# This method prints the given package
def print_package(package, delivered):
    phrase = ['Leaves at: ', 'Left at: ', 'Delivered at: '][delivered]
    time = [package[8], package[8], package[9]][delivered]
    package_id = format(f'|{package[0]}', '<12')
    address = format(f'{" ".join([package[1],package[2],package[3],package[4]])}', '<67')
    delivery = format(phrase, '<14') + format(time, '>11')
    status = format(f'{package[11]}', '<10')

    print(package_id, address, delivery, status, '', sep=' | ')

# This method checks the time range and whether the package
# was delivered or not
def check_time(start_time, end_time, package):
    try:
        start_time = d.strptime(start_time, '%H:%M:%S')
        end_time = d.strptime(end_time, '%H:%M:%S')

        sent_time = d.strptime(package[8], '%H:%M:%S')
        delivered_time = d.strptime(package[9], '%H:%M:%S')
    except:
        print(package[8], package[9])
        print('Invalid timestamp.')
        return
    if start_time <= end_time:
        if end_time >= sent_time and end_time < delivered_time:
            package[11] = 'En Route'
            return 1
        elif end_time >= delivered_time:
            package[11] = 'Delivered'
            return 2
        else:
            return 0
    else:
        print('Please make sure to use military time.')
        return


# This is the main program where the interface will be provided
# The user will be prompted to enter a specific package to view
# or to view all the packages. Then they will be prompted to enter
# a range of time to view to status of the package between those
# times.
def main():
    # Instantiate Delivery object
    delivery = Delivery()

    hashtable = delivery.get_table()
    user_input = ''
    print('***********************************************************')
    print('*                                                         *')
    print('*                                                         *')
    print('*         Welcome to the WGUPS Delivery Interface         *')
    print('*                                                         *')
    print('*                                                         *')
    print('***********************************************************')
    print()
    print()
    print('-------------------Basic Summary For Today-----------------')
    print('// Total Packages: 40')
    print('// Total Successful Deliveries: 40')
    print('// Total Unsuccessful Deliveries: 0')
    print(f'// Total Mileage Traveled: {delivery.get_total_distance()}')

    # Run the program until the user inputs quit or q
    while user_input.lower() not in ('q', 'quit'):
        user_input = menu()

        if user_input.lower() in ('q', 'quit'): continue

        # Ask about specific package and print it
        if user_input.lower() == 's':
            package_id = input('Please enter the package id: ')

            if not package_id.isdigit():
                print('Invalid entry, package id must be a number.')
                return
            if int(package_id) < 1 or int(package_id) > 40:
                print('Invalid entry, a package with this id does not exist.')
                return

            package = hashtable.get_value(package_id)
            delivered = 0
            print('Package was found.\nPlease enter a time range.')
            start_time = input('Start Time (HH:MM:SS): ')
            end_time = input('End Time (HH:MM:SS): ')
            
            delivered = check_time(start_time, end_time, package)
            print()
            print('-'*125)
            print(format("|Package ID", "<12"), format("Delivery Address", "<67"), format("Delivery Schedule", "<25"), format("Status     |", "<10"), sep=' | ')
            print('-'*125)
            print_package(package, delivered)
            print('-'*125)
            print(f'\nTotal Distance Traveled: {delivery.get_total_distance()}')
            continue
        # Print all packages in the time range
        elif user_input.lower() == 'a':
            print("All packages will be printed.\nPlease enter a time range.")
            start_time = input('Start Time (HH:MM:SS): ')
            end_time = input('End Time (HH:MM:SS): ')

            print()
            print('-'*125)
            print(format("|Package ID", "<12"), format("Delivery Address", "<67"), format("Delivery Schedule", "<25"), format("Status     |", "<10"), sep=' | ')
            print('-'*125)
            for i in range(40):
                package = hashtable.get_value(str(i+1))
                delivered = 0
                delivered = check_time(start_time, end_time, package)
                print_package(package, delivered)
            print('-'*125)
            print(f'\nTotal Distance Traveled: {delivery.get_total_distance()}')    
            continue       

if __name__ == '__main__':
    main()