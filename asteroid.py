class Asteroid:
    def __init__(self, x_location, x_speed, y_location, y_speed, size):

        self.__asteroid = {"location": [x_location, y_location], "speed": [x_speed, y_speed]}
        #size is int between 1 and 3
        self.__size = size

    def get_location(self):
        return self.__asteroid["location"]

    def get_speed(self):
        return self.__asteroid["speed"]

    def set_location(self, location):
        self.__asteroid["location"][0] = location[0]
        self.__asteroid["location"][1] = location[1]



