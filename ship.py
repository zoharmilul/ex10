class Ship:
    def __init__(self, x_location, x_speed, y_location, y_speed, heading, life):
        self.__ship = {'location': [x_location, y_location], 'speed': [x_speed, y_speed]}
        self.__heading = heading
        self.__life = life

    def set_location(self, location):
        self.__ship['location'] = [location[0], location[1]]

    def set_direction(self, new_heading):
        self.__heading = new_heading

    def set_speed(self, speed):
        self.__ship["speed"] = [speed[0], speed[1]]

    def reduce_life(self, amount):
        self.__life = self.__life - amount

    def get_location(self):
        return self.__ship['location']

    def get_speed(self):
        return self.__ship['speed']

    def get_direction(self):
        return self.__heading

    def get_radius(self):
        return 1

    def get_life(self):
        return self.__life
