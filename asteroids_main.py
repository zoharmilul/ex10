from screen import Screen
import sys
import ship
import math
import random
import asteroid
import torpedo

DEFAULT_ASTEROIDS_NUM = 5
START_ASTEROID_SIZE = 3
X_AXIS = 0
Y_AXIS = 1
DELTA = {X_AXIS: Screen.SCREEN_MAX_X - Screen.SCREEN_MIN_X,
         Y_AXIS: Screen.SCREEN_MAX_Y - Screen.SCREEN_MIN_Y}
CLOCKWISE = 1
COUNTER_CLOCKWISE = 0
HEADING_DIF = 7


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        self.__start_x_ship = random.randint(self.__screen_min_x, self.__screen_max_x)
        self.__start_y_ship = random.randint(self.__screen_min_y, self.__screen_max_y)
        self.__main_ship = ship.Ship(self.__start_x_ship, 0, self.__start_y_ship, 0, 0, 3)
        self.__torpedos_list = []
        self.__asteroids_lst = []
        self.__score = 0
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
        self.__main_ship.set_location((calc_new_position(self.__main_ship, X_AXIS),
                                       calc_new_position(self.__main_ship, Y_AXIS)))

        #updating torpedo life
        self.update_torpedo_life()

        # handling key pressed
        self.__screen.set_score(self.__score)
        if self.__screen.is_right_pressed():
            change_heading(self.__main_ship, CLOCKWISE)
        if self.__screen.is_left_pressed():
            change_heading(self.__main_ship, COUNTER_CLOCKWISE)
        if self.__screen.is_up_pressed():
            speed_up_ship(self.__main_ship)
        if self.__screen.is_space_pressed():
            if len(self.__torpedos_list) < 10:
                self.fire_new_torp()

        #draws torpedos
        for torpedos in self.__torpedos_list:
            self.__screen.draw_torpedo(torpedos,
                                       torpedos.get_location()[X_AXIS],
                                       torpedos.get_location()[Y_AXIS],
                                       torpedos.get_direction())
            torpedos.set_location((calc_new_position(torpedos, X_AXIS),
                                  calc_new_position(torpedos, Y_AXIS)))

        # drawing the asteroids
        for ast in self.__asteroids_lst:
            self.__screen.draw_asteroid(ast, ast.get_location()[0], ast.get_location()[1])
            ast.set_location((calc_new_position(ast, X_AXIS), calc_new_position(ast, Y_AXIS)))

        # check about intersections
        for ast in self.__asteroids_lst:
            if ast.has_intersection(self.__main_ship):
                self.ast_ship_intersec(ast)
            for torp in self.__torpedos_list:
                if ast.has_intersection(torp):
                    self.ast_torp_intersec(ast, torp)

        # end the game
        if not self.__asteroids_lst:
            self.__screen.show_message("CONGRATZ!" , "you are one motherfucker bitch ass asteroids killer! you won! \n"
                                                      f"your score is {self.__score}")
            self.__screen.end_game()
            sys.exit()

        if not self.__main_ship.get_life():
            self.__screen.show_message("LOOOOOSER", "you died bitch")
            self.__screen.end_game()
            sys.exit()

        if self.__screen.should_end():
            self.__screen.show_message("but but but why?", "you chose to leave... good bye! miss you XOXO")
            self.__screen.end_game()
            sys.exit()

    def update_torpedo_life(self):
        for torp in self.__torpedos_list:
            torp.raise_life(1)
            if torp.get_life() == 200:
                self.__screen.unregister_torpedo(torp)
                self.__torpedos_list.remove(torp)

    def fire_new_torp(self):
        torpedo_speed = get_torpedo_speed(self.__main_ship)
        torpedo_location = self.__main_ship.get_location()
        new_torpedo = torpedo.Torpedo(torpedo_location[X_AXIS],
                                      torpedo_speed[X_AXIS],
                                      torpedo_location[Y_AXIS],
                                      torpedo_speed[Y_AXIS],
                                      self.__main_ship.get_direction())
        self.__torpedos_list.append(new_torpedo)
        self.__screen.register_torpedo(new_torpedo)

    def ast_ship_intersec(self, ast):
        self.__main_ship.reduce_life(1)
        self.__screen.show_message("Warning!", "There was and intersection with an asteroid")
        self.__screen.remove_life()
        self.__screen.unregister_asteroid(ast)
        self.__asteroids_lst.remove(ast)

    def ast_torp_intersec(self, ast, torp):
        if ast.get_size() == 3:
            self.__score += 20
        elif ast.get_size() == 2:
            self.__score += 50
        elif ast.get_size() == 1:
            self.__score += 100
        if ast.get_size() > 1:
            ast1 = create_new_ast(ast, torp.get_speed())
            self.__screen.register_asteroid(ast1, ast1.get_size())
            self.__asteroids_lst.append(ast1)
            ast2 = create_new_ast(ast, torp.get_speed(), "second")
            self.__asteroids_lst.append(ast2)
            self.__screen.register_asteroid(ast2, ast2.get_size())
        self.__screen.unregister_torpedo(torp)
        self.__torpedos_list.remove(torp)
        self.__screen.unregister_asteroid(ast)
        self.__asteroids_lst.remove(ast)


def create_new_ast(old_ast, torp_speed, order = "first"):
    new_speed = calc_new_ast_speed(torp_speed, old_ast.get_speed())
    if order == "second":
        new_speed = (-new_speed[X_AXIS], - new_speed[Y_AXIS])
    new_ast = asteroid.Asteroid(old_ast.get_location()[X_AXIS],
                                new_speed[X_AXIS],
                                old_ast.get_location()[Y_AXIS],
                                new_speed[Y_AXIS],
                                old_ast.get_size() - 1)
    return new_ast


def calc_new_position(game_obj, axis):
    old_pos = game_obj.get_location()[axis]
    if axis == X_AXIS:
        return Screen.SCREEN_MIN_X + (old_pos + game_obj.get_speed()[axis] - Screen.SCREEN_MIN_X) % DELTA[axis]
    if axis == Y_AXIS:
        return Screen.SCREEN_MIN_Y + (old_pos + game_obj.get_speed()[axis] - Screen.SCREEN_MIN_Y) % DELTA[axis]


def change_heading(ship, direction):
    if direction == CLOCKWISE:
        ship.set_direction(ship.get_direction() - HEADING_DIF)
    if direction == COUNTER_CLOCKWISE:
        ship.set_direction(ship.get_direction() + HEADING_DIF)

def calc_new_ast_speed(torpedo_speed, astroid_speed):
    new_speed_x = (torpedo_speed[X_AXIS] + astroid_speed[X_AXIS])/math.sqrt(astroid_speed[0]**2 + astroid_speed[1]**2)
    new_speed_y = (torpedo_speed[Y_AXIS] + astroid_speed[Y_AXIS])/math.sqrt(astroid_speed[0]**2 + astroid_speed[1]**2)
    return new_speed_x, new_speed_y

def speed_up_ship(ship):
    speed_x = ship.get_speed()[0] + math.cos(math.radians(ship.get_direction()))
    speed_y = ship.get_speed()[1] + math.sin(math.radians(ship.get_direction()))
    ship.set_speed((speed_x, speed_y))

def get_torpedo_speed(ship):
    ship_heading = ship.get_direction()
    ship_speed = ship.get_speed()
    speed_x = ship_speed[X_AXIS] + 2 * math.cos(math.radians(ship_heading))
    speed_y = ship_speed[Y_AXIS] + 2 * math.sin(math.radians(ship_heading))
    return speed_x, speed_y

def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
