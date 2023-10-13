import random
import csv


class Station:
    """
        This is a class for replicating a train Station.

        Attributes:
            link_colour (String): The link_colour between this station and the connected one.
            direction (String): The current direction of the train
            connection (Station): The connected station

    """
    stations_graph = []  # map to hold all connections. First element is station name, second element is delay

    # followed by all the connections a station has. It is a list of list structure

    def __init__(self, name, colour, direction, connection, delay=0):  # parameterized constructor with delay 0 as
        # default parameter

        """
                The constructor for Station class.

                Parameters:
                   name (String): The name of the station.
                   colour (String): The link_colour between this station and the connected one.
                   direction (String): The current direction of the train
                   connection (Station): The connected station
                   delay (double): The probability of delay at the station
        """

        self.link_colour = colour
        self.direction = direction
        self.connection = connection

        station = Station.find_station(name)  # checking if station already exists in the map structure
        if station is None:  # if not then add a new list element having name,delay and the station object
            lst = [name, delay, self]
            Station.stations_graph.append(lst)
        else:  # if yes then simply append the new station to it
            station.append(self)

    @staticmethod
    def create_station(name, colour, direction, connection):  # creating a new station
        """
                        The function for creating two station from A to B and B to A.

                        Parameters:
                           name (String): The name of the station.
                           colour (String): The link_colour between this station and the connected one.
                           direction (String): The current direction of the train
                           connection (String): The connected station
        """
        Station(name, colour, direction, connection)  # adding edge from A to B
        if direction == "N":  # adding edge from B to A
            Station(connection, colour, "S", name)
        else:
            Station(connection, colour, "N", name)

    @staticmethod
    def set_delay(name, delay):  # adding station delays
        """
                        The function for setting the delay probability at the station.

                        Parameters:
                           name (String): The name of the station.
                           delay (double): The probability of delay at the station
        """
        station = Station.find_station(name)  # finding station
        if station is not None:
            station[1] = delay  # setting delay

    @staticmethod
    def find_station(name):
        """
                        The function for finding a specific station.

                        Parameters:
                           name (String): The name of the station.

                        Returns:
                           list: The found station details.

        """
        for station in Station.stations_graph:
            if station:
                if station[0] == name:
                    return station
        return None


class Train:
    """
           This is a class for a Train.

           Attributes:
               colour (String): The link colour on which the train is travelling
               train_number (int): The number of the train
               direction (String): The current direction of the train
               delay (boolean): Whether the train is delayed at the station or not
       """

    train_number = 1

    def __init__(self):
        """
                          The constructor for Train class.
        """
        self.current_station = Station.stations_graph.__getitem__(random.randint(0, len(Station.stations_graph) - 1))
        # setting current station randomly from the map structure
        rand = random.randint(0, 1)  # giving random direction to the train
        if rand == 0:
            self.direction = "N"
        else:
            self.direction = "S"

        self.train_number = Train.train_number
        Train.train_number += 1
        self.delay = False
        self.colour = ""
        self.colour = self.get_random_colour()  # giving random colour line to train

    def get_random_colour(self):
        """
                                The method for associating a random link colour with the train at the start

                                Returns:
                                    String: random colour
        """
        all_stations = self.get_all_stations_in_same_direction_and_line()  # check all the connected stations
        #  having the same direction as of the train
        if len(all_stations) == 0:
            self.invert_direction()  # invert direction in case no such stations exist
            all_stations = self.get_all_stations_in_same_direction_and_line()  # find connected stations again
            if len(all_stations) == 0:  # if still no station found this means no line exists around this station
                return "NO"

        rand = random.randint(0, len(all_stations) - 1)  # return a random colour from the connection stations
        return all_stations[rand].link_colour

    def get_all_stations_in_same_direction_and_line(self):
        """
                                The method for finding a specific station.
                                Returns:
                                    list: all connected stations in the same direction and on the same line colour

        """
        all_stations = []
        for station in Station.stations_graph:
            if station[0] == self.current_station[0]:  # finding the current station in the map structure

                for connection in station[2:]:  # checking all the connected stations to the current train station
                    if connection.direction == self.direction:  # check if direction of connection is same as of train
                        if self.colour != "":  # if colour has been set then check for same colour too
                            if connection.link_colour == self.colour:
                                all_stations.append(connection)
                        else:
                            all_stations.append(connection)
        return all_stations

    def next_time_unit(self):  # simulate the train
        """
                                The method for simulating each time unit of the train.
        """
        outputs = [True, False]
        probability = [self.current_station[1], 1 - self.current_station[1]]
        delay_flag = random.choices(outputs, weights=probability, k=1)  # set delay according to probability

        if not delay_flag[0]:  # if there is no delay
            all_stations = self.get_all_stations_in_same_direction_and_line()  # get all connected stations in same
            # direction and line
            if len(all_stations) == 0:
                self.invert_direction()  # if no such station found then invert the train's direction
                all_stations = self.get_all_stations_in_same_direction_and_line()

            index = random.randint(0, len(all_stations) - 1)  # randomly pick the next station the train will move to

            for station in Station.stations_graph:
                if station[0] == all_stations[index].connection:  # find the station the train is moving in the map
                    # structure
                    self.current_station = station  # update the train structure

            all_stations = self.get_all_stations_in_same_direction_and_line()  # check again to determine which
            # direction the train will be moving
            if len(all_stations) == 0:
                self.invert_direction()

        self.delay = delay_flag[0]  # setting the delay

    def print_details(self):  # printing train information
        """
                                The method for printing details of the train.
        """
        to_print = "Train " + str(self.train_number) + " on " + self.colour.upper() + " line is at station " + \
                   self.current_station[
                       0].upper() + " heading in " + self.get_direction() + " direction."
        if self.delay:
            to_print = to_print + " (DELAY)"

        print(to_print)

    def invert_direction(self):
        """
                                The method for inverting the direction of the train.
        """
        if self.direction == 'N':
            self.direction = 'S'
        else:
            self.direction = 'N'

    def get_direction(self):
        """
                                The method for getting the direction name in full.

                                Returns:
                                    String: The full spellings of the direction
        """
        if self.direction == 'N':
            return "North"
        else:
            return "South"


def read_stations_file():
    """
                            The function for reading the stations file.

                            Returns:
                                bool: File read successfully or not.

    """
    stations_file = input("Enter the stations file you want to use: ")

    try:
        with open(stations_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                Station.set_delay(row[0], float(row[1]))
            return True
    except IOError:
        print("Error. Could not open file the stations file entered.")
        return False
    except IndexError:
        print("Error. Could not open file the stations file entered.")
        return False

def read_connections_file():
    """
                                The function for reading the connections file.

                                Returns:
                                    bool: File read successfully or not.
    """
    connections_file = input("Enter the connections file you want to use: ")

    try:
        with open(connections_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                Station.create_station(row[0], row[2], row[3], row[1])
            return True
    except IOError:
        print("Error. Could not open the connections file entered.")
        return False
    except IndexError:
        print("Error. Could not open the connections file entered.")
        return False
        
    
def menu():
    """
                                The function for providing the user with a menu interface.
    """
    no_of_trains = input("Enter how many trains to simulate: ")
    if no_of_trains.isnumeric():
        no_of_trains = int(no_of_trains)

        trains = []
        for i in range(0, int(no_of_trains)):
            trains.append(Train())  # creating 'no_of_trains' many Train objects

        choice = ""
        while choice != "q":
            print("\ncontinue simulation [1], train info [2], exit [q].")
            choice = input("Select an option: ")
            if choice == "1":
                for i in range(0, no_of_trains):
                    trains[i].next_time_unit()  # simulate all trains

            elif choice == "2":
                train_choice = input("which train [1 - " + str(no_of_trains) + "]: ")
                if 1 <= int(train_choice) <= int(no_of_trains):  # validating input
                    print()
                    trains[int(train_choice) - 1].print_details()
                else:
                    print("Incorrect train number provided!")
            elif choice == "q":
                print("Thank you and Goodbye!")
            else:
                print("Invalid option provided. Try again")
    else:
        print("Invalid input entered for number of trains.")


if read_connections_file():
    if read_stations_file():
        menu()
