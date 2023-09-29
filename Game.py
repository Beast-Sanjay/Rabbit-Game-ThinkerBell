import random
import os

rabbit = 'r'
rabbit_with_carrot = 'R'
carrot = 'c'
rabbit_HOLE = 'O'
pathway_stone = '-'

class rabbitGame:
    # Initializations 
    def __init__(self, map_size, num_carrots, num_rabbit_holes):
        self.map_size = map_size
        self.num_carrots = num_carrots
        self.num_rabbit_holes = num_rabbit_holes
        self.map = self.generate_map()
        self.counter = 0

    def generate_map(self):
        # Generate a random map
        game_map = [[pathway_stone for _ in range(self.map_size)] for _ in range(self.map_size)]
        used_coordinates = set()

        def generate_random_coordinates():
            x, y = random.randint(0, self.map_size - 1), random.randint(0, self.map_size - 1)
            return x, y

        # Place random rabbit position
        rabbit_x, rabbit_y = generate_random_coordinates()
        game_map[rabbit_x][rabbit_y] = rabbit
        used_coordinates.add((rabbit_x, rabbit_y))

        # Place random carrots
        for _ in range(self.num_carrots):
            while True:
                carrot_x, carrot_y = generate_random_coordinates()
                if (carrot_x, carrot_y) not in used_coordinates:
                    game_map[carrot_x][carrot_y] = carrot
                    used_coordinates.add((carrot_x, carrot_y))
                    break

        # Place random rabbit holes
        for _ in range(self.num_rabbit_holes):
            while True:
                hole_x, hole_y = generate_random_coordinates()
                if (hole_x, hole_y) not in used_coordinates:
                    game_map[hole_x][hole_y] = rabbit_HOLE
                    used_coordinates.add((hole_x, hole_y))
                    break

        return game_map

    def display_grid(self):
        os.system('cls') 
        for row in self.map:
            print(' '.join(row))

    def is_valid_move(self, x, y):
        if 0 <= x < self.map_size and 0 <= y < self.map_size and self.map[x][y] != carrot and self.map[x][y] != rabbit_HOLE:
            return True
        return False

    # carrot pickup fuctoin when adjacent to carrot in the map
    def pick_carrot(self, x, y):
        if 0 < x < self.map_size - 1 and 0 < y < self.map_size - 1:
            if self.map[x][y] == rabbit_with_carrot:
                adjacent_holes = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
                for hole_x, hole_y in adjacent_holes:
                    if 0 <= hole_x < self.map_size and 0 <= hole_y < self.map_size and self.map[hole_x][hole_y] == rabbit_HOLE:
                        self.map[x][y] = rabbit
                        self.counter += 1

            if self.map[x][y + 1] == carrot and self.map[x][y] == rabbit:
                self.map[x][y] = pathway_stone
                self.map[x][y + 1] = rabbit_with_carrot
                self.counter += 1
            elif self.map[x][y - 1] == carrot and self.map[x][y] == rabbit:
                self.map[x][y] = pathway_stone
                self.map[x][y - 1] = rabbit_with_carrot
                self.counter += 1
            elif self.map[x + 1][y] == carrot and self.map[x][y] == rabbit:
                self.map[x][y] = pathway_stone
                self.map[x + 1][y] = rabbit_with_carrot
                self.counter += 1
            elif self.map[x - 1][y] == carrot and self.map[x][y] == rabbit:
                self.map[x][y] = pathway_stone
                self.map[x - 1][y] = rabbit_with_carrot
                self.counter += 1

    def convert_rabbit(self, x, y):
        if self.map[x][y] == rabbit_with_carrot:
            self.map[x][y] = rabbit

    # jumping the carrot or the hole function {but still work on on it}
    def rabbit_hole_jump(self, x, y):
        possible_moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        possible_holes = [(i, j) for i, j in possible_moves if 0 <= i < self.map_size and 0 <= j < self.map_size and self.map[i][j] == rabbit_HOLE]
        possible_carrots = [(i, j) for i, j in possible_moves if 0 <= i < self.map_size and 0 <= j < self.map_size and self.map[i][j] == carrot]

        if not possible_holes and not possible_carrots:
            return

        if possible_holes:
            random_hole_x, random_hole_y = random.choice(possible_holes)
            self.map[x][y], self.map[random_hole_x][random_hole_y] = self.map[random_hole_x][random_hole_y], self.map[x][y]
        elif possible_carrots:
            random_carrot_x, random_carrot_y = random.choice(possible_carrots)
            self.map[x][y], self.map[random_carrot_x][random_carrot_y] = self.map[random_carrot_x][random_carrot_y], self.map[x][y]

    # used to get the rabbit position
    def rabbit_position(self):
        for i in range(self.map_size):
            for j in range(self.map_size):
                if self.map[i][j] == rabbit or self.map[i][j] == rabbit_with_carrot:
                    return i, j
    # rabbit movement across the the generated map
    def move_rabbit(self):
        try:
            while True:
                if self.counter == self.num_carrots:
                    self.display_grid()
                    print("-------------------------")
                    print("All carrots eaten! You won!")
                    print("-------------------------")
                    break

                self.display_grid()
                rabbit_x, rabbit_y = self.rabbit_position()

                move = input("Enter a move (w/a/s/d to move, p to pick carrot, j for rabbit hole jump, o to put carrot in hole, q to quit): ")

                if move == 'q':
                    print("Exiting the game.")
                    break
                elif move == 'p':
                    os.system('cls')
                    self.pick_carrot(rabbit_x, rabbit_y)
                elif move == 'j':
                    os.system('cls')
                    self.rabbit_hole_jump(rabbit_x, rabbit_y)
                elif move == 'o':
                    os.system('cls')
                    self.convert_rabbit(rabbit_x, rabbit_y)
                elif move in ('w', 'a', 's', 'd'): # working on carrot moving diagonal
                    new_x, new_y = rabbit_x, rabbit_y
                
                    if move == 'a':
                        new_y -= 1
                    elif move == 'd':
                        new_y += 1
                    elif move == 'w':
                        new_x -= 1
                    elif move == 's':
                        new_x += 1

                    if self.is_valid_move(new_x, new_y):
                        current_rabbit = self.map[rabbit_x][rabbit_y]
                        self.map[rabbit_x][rabbit_y] = pathway_stone
                        rabbit_x, rabbit_y = new_x, new_y
                        self.map[rabbit_x][rabbit_y] = current_rabbit
                else:
                    os.system('cls')
                    print("Invalid move. Try again.")
        except KeyboardInterrupt:
            print("\nGame terminated.")

def main():
    print('Instructions:')
    print('Press Enter to play the game; Press any other key to Quit.')
    print('Repeat the same after every play.')
    key = input()
    if key == "":
        map_size = int(input("Enter the size of the grid (minimum 10): "))
        while map_size < 10:
            map_size = int(input("Please enter a grid size of at least 10: "))

        num_carrots = int(input("Enter the number of carrots (greater than 1): "))
        while num_carrots <= 1:
            num_carrots = int(input("Please enter a number of carrots greater than 1: "))

        num_rabbit_holes = int(input("Enter the number of rabbit holes (greater than 1): "))
        while num_rabbit_holes <= 1:
            num_rabbit_holes = int(input("Please enter a number of holes greater than 1: "))

        game = rabbitGame(map_size, num_carrots, num_rabbit_holes)
        game.move_rabbit()

if __name__ == "__main__":
    os.system('cls')
    main()
