class Torpedo:
    def __init__(self, x_location, x_speed, y_location, y_speed, direction, life_span = 0):
        self.__torpedo = {"location": [x_location, y_location], "speed": [x_speed, y_speed]}
        #direction in degress (float)
        self.__direction = direction
        self.RADIUS = 4
        self.__life_span = life_span

    def set_location(self, location):
        self.__torpedo["location"] = [location[0], location[1]]

    def set_direction(self, direction):
        self.__direction = direction

    def raise_life(self, amount):
        self.__life_span += amount

    def get_location(self):
        return self.__torpedo["location"]

    def get_speed(self):
        return self.__torpedo["speed"]

    def get_direction(self):
        return self.__direction

    def get_life(self):
        return self.__life_span


