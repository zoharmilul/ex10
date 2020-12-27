from screen import Screen
import sys
import ship
import math
import random
import asteroid

DEFAULT_ASTEROIDS_NUM = 5
START_ASTEROID_SIZE = 3

X_AXIS = 0
Y_AXIS = 1
DELTA = {X_AXIS: Screen.SCREEN_MAX_X - Screen.SCREEN_MIN_X,
         Y_AXIS: Screen.SCREEN_MAX_Y - Screen.SCREEN_MIN_Y}
CLOCKWISE = 1
COUNTER_CLOCKWISE = 0
class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__start_x_ship = random.randint(self.__screen_min_x, self.__screen_max_x) ###
        self.__start_y_ship = random.randint(self.__screen_min_y, self.__screen_max_y) ###
        self.__main_ship = ship.Ship(self.__start_x_ship, 0, self.__start_y_ship, 0, 0, 3)

        self.__asteroids_lst = []
        while len(self.__asteroids_lst) < asteroids_amount:
            start_x_asteroid = random.randint(self.__screen_min_x, self.__screen_max_x)
            start_y_asteroid = random.randint(self.__screen_min_y, self.__screen_max_y)
            start_x_speed = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            start_y_speed = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            new_asteroid = asteroid.Asteroid(start_x_asteroid, start_x_speed,
                                             start_y_asteroid, start_y_speed, START_ASTEROID_SIZE)

            if not new_asteroid.has_intersection(self.__main_ship):
                # only if there is no intersection with the ship, the asteroid is added to the game
                self.__asteroids_lst.append(new_asteroid)
                self.__screen.register_asteroid(new_asteroid, START_ASTEROID_SIZE)

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        self.__screen.draw_ship(self.__main_ship.get_location()[0],
                                self.__main_ship.get_location()[1],
                                self.__main_ship.get_direction())
        if self.__screen.is_right_pressed():
            change_heading(self.__main_ship, CLOCKWISE)
        if self.__screen.is_left_pressed():
            change_heading(self.__main_ship, COUNTER_CLOCKWISE)
        if self.__screen.is_up_pressed():
            speed_up_ship(self.__main_ship)
        self.__main_ship.set_location((calc_new_position(self.__main_ship, X_AXIS), calc_new_position(self.__main_ship, Y_AXIS)))

        self.__main_ship.set_location((calc_new_position(self.__main_ship, X_AXIS),
                                       calc_new_position(self.__main_ship, Y_AXIS)))

        for ast in self.__asteroids_lst:  # drawing the asteroids
            self.__screen.draw_asteroid(ast, ast.get_location()[0], ast.get_location()[1])

        for ast in self.__asteroids_lst:  # check about intersections
            if ast.has_intersection(self.__main_ship):
                self.__main_ship.reduce_life(1)
                self.__screen.show_message("Warning! ", "There was a intersection between the ship and the asteroid")
                self.__screen.remove_life()
                self.__screen.unregister_asteroid(ast)
        # TODO: Your code goes here
        pass


def calc_new_position(game_obj, axis):
    old_pos = game_obj.get_location()[axis]
    if axis == X_AXIS:
        return Screen.SCREEN_MIN_X + (old_pos + game_obj.get_speed()[axis] - Screen.SCREEN_MIN_X) % DELTA[axis]
    if axis == Y_AXIS:
        return Screen.SCREEN_MIN_Y + (old_pos + game_obj.get_speed()[axis] - Screen.SCREEN_MIN_Y) % DELTA[axis]

def change_heading(ship, direction):
    if direction == CLOCKWISE:
        ship.set_direction(ship.get_direction() - 7)
    if direction == COUNTER_CLOCKWISE:
        ship.set_direction(ship.get_direction() + 7)

def speed_up_ship(ship):
    speed_x = ship.get_speed()[0] + math.cos(math.radians(ship.get_direction()))
    speed_y = ship.get_speed()[1] + math.sin(math.radians(ship.get_direction()))
    ship.set_speed((speed_x,speed_y))

def main(amount):
    runner = GameRunner(amount)

    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
