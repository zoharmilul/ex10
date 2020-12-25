from screen import Screen
import sys
import ship
import random

DEFAULT_ASTEROIDS_NUM = 5

X_AXES = 0
Y_AXES = 1
DELTA = {X_AXES: Screen.SCREEN_MAX_X - Screen.SCREEN_MIN_X,
         Y_AXES :Screen.SCREEN_MAX_Y - Screen.SCREEN_MIN_Y}
class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__start_x = random.randint(Screen.SCREEN_MIN_X, Screen.SCREEN_MAX_X)
        self.__start_y = random.randint(Screen.SCREEN_MIN_Y, Screen.SCREEN_MAX_Y)
        self.__main_ship = ship.Ship(self.__start_x, 0, self.__start_y, 0, 0)

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

        self.__main_ship.set_location((calc_new_position(self.__main_ship, X_AXES), calc_new_position(self.__main_ship, Y_AXES)))
        # TODO: Your code goes here
        pass


def calc_new_position(game_obj, axes):
    old_pos = game_obj.get_location()[axes]
    if axes == X_AXES:
        return Screen.SCREEN_MIN_X + (old_pos + game_obj.get_speed()[axes] - Screen.SCREEN_MIN_X) % DELTA[axes]
    if axes == Y_AXES:
        return Screen.SCREEN_MIN_Y + (old_pos + game_obj.get_speed()[axes] - Screen.SCREEN_MIN_Y) % DELTA[axes]

def main(amount):
    runner = GameRunner(amount)

    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
