class Torpedo:
    def __init__(self, x_location, x_speed, y_location, y_speed, direction):
        self.__torpedo = {"location": [x_location, y_location], "speed": [x_speed, y_speed]}
        #direction in degress (float)
        self.__direction = direction

    def set_location(self, location):
        self.__torpedo["location"][0] = location[0]
        self.__torpedo["location"][1] = location[1]

    def set_direction(self, direction):
        self.__direction = direction

    def get_location(self):
        return self.__torpedo["location"]

    def get_speed(self):
        return self.__torpedo["speed"]

    def get_direction(self):
        return self.__direction



