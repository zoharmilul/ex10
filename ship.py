class Ship:
    def __init__(self, x_location, x_speed, y_location, y_speed, direction):
        self.__ship = {'location': [x_location, y_location], 'speed': [x_speed, y_speed]}
        self.__direction = direction

    def set_ship(self, location):
        self.__ship['x'][0] = location[0]
        self.__ship['y'][0] = location[1]

    def set_direction(self, new_direction):
        self.__direction = new_direction

    def get_location(self):
        return self.__ship['location']

    def get_speed(self):
        return self.__ship['speed']

    def get_direction(self):
        return self.__direction
