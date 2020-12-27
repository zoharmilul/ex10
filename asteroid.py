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
        self.__asteroid["location"] = [location[0], location[1]]

    def get_radius(self):
        return self.__size * 10 - 5

    def has_intersection(self, obj):
        """
        Calculates the distance between an object and the asteroid, and checks if there is an intersection.
        :return: True if there is an intersection, False if not.
        """
        distance = ((obj.get_location()[0] - self.get_location()[0])**2 +
                    (obj.get_location()[1] - self.get_location()[1])**2) ** 0.5
        if distance <= self.get_radius() + obj.get_radius():
            return True
        else:
            return False


