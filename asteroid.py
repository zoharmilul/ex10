class Asteroid:
    def __init__(self, x_location, x_speed, y_location, y_speed, size):

        self.__asteroid = {"location": [x_location, y_location], "speed": [x_speed, y_speed]}
        self.__size = int(size)
        if size > 3 or size < 1:
            self.__size = 3
        self.RADIUS = 10 * size - 5


    def get_location(self):
        return self.__asteroid["location"]

    def get_speed(self):
        return self.__asteroid["speed"]

    def set_location(self, location):
        self.__asteroid["location"] = [location[0], location[1]]

    def has_intersection(self, obj):
        """
        Calculates the distance between an object and the asteroid, and checks if there is an intersection.
        :return: True if there is an intersection, False if not.
        """
        distance = ((obj.get_location()[0] - self.get_location()[0])**2 +
                    (obj.get_location()[1] - self.get_location()[1])**2) ** 0.5
        if distance <= self.RADIUS + obj.RADIUS:
            return True
        else:
            return False

    def get_size(self):
        return self.__size
