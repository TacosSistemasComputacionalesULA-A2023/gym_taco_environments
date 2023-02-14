import colorama
import numpy

class PrimMazeGenerator:
    def __init__(self, random_state) -> None:
        self.np = random_state

    def print_prim_maze(self, maze, height, width):
    # Initialize colorama
        colorama.init()
        for i in range(0, height):
            for j in range(0, width):
                if maze[i][j] == 'u':
                    print(colorama.Fore.WHITE + str(maze[i][j]), end=" ")
                elif maze[i][j] == 'c':
                    print(colorama.Fore.GREEN + str(maze[i][j]), end=" ")
                else:
                    print(colorama.Fore.RED + str(maze[i][j]), end=" ")

            print('\n')


    def surrounding_cells(self, maze, rand_wall):
        # Find number of surrounding cells
        s_cells = 0
        if maze[rand_wall[0]-1][rand_wall[1]] == 'c':
            s_cells += 1
        if maze[rand_wall[0]+1][rand_wall[1]] == 'c':
            s_cells += 1
        if maze[rand_wall[0]][rand_wall[1]-1] == 'c':
            s_cells += 1
        if maze[rand_wall[0]][rand_wall[1]+1] == 'c':
            s_cells += 1

        return s_cells


    def check_left_wall(self, maze, rand_wall, walls, height) -> bool:
        if rand_wall[1] != 0:
            if maze[rand_wall[0]][rand_wall[1]-1] == 'u' and \
                    maze[rand_wall[0]][rand_wall[1]+1] == 'c':
                # Find the number of surrounding cells
                s_cells = self.surrounding_cells(maze, rand_wall)
                if s_cells < 2:
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    # Upper cell
                    if rand_wall[0] != 0:
                        if maze[rand_wall[0]-1][rand_wall[1]] == 'u':
                            maze[rand_wall[0]-1][rand_wall[1]] = 'w'
                        if [rand_wall[0]-1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0]-1, rand_wall[1]])

                    # Bottom cell
                    if rand_wall[0] != height-1:
                        if maze[rand_wall[0]+1][rand_wall[1]] == 'u':
                            maze[rand_wall[0]+1][rand_wall[1]] = 'w'
                        if [rand_wall[0]+1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0]+1, rand_wall[1]])

                    # Leftmost cell
                    if rand_wall[1] != 0:
                        if maze[rand_wall[0]][rand_wall[1]-1] == 'u':
                            maze[rand_wall[0]][rand_wall[1]-1] = 'w'
                        if [rand_wall[0], rand_wall[1]-1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1]-1])

                # Delete wall
                for wall in walls:
                    if wall == rand_wall:
                        walls.remove(wall)

                return True

        return False


    def check_upper_wall(self, maze, rand_wall, walls, width) -> bool:
        if rand_wall[0] != 0:
            if maze[rand_wall[0]-1][rand_wall[1]] == 'u' and \
                    maze[rand_wall[0]+1][rand_wall[1]] == 'c':

                s_cells = self.surrounding_cells(maze, rand_wall)
                if s_cells < 2:
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    # Upper cell
                    if rand_wall[0] != 0:
                        if maze[rand_wall[0]-1][rand_wall[1]] != 'c':
                            maze[rand_wall[0]-1][rand_wall[1]] = 'w'
                        if [rand_wall[0]-1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0]-1, rand_wall[1]])

                    # Leftmost cell
                    if rand_wall[1] != 0:
                        if maze[rand_wall[0]][rand_wall[1]-1] != 'c':
                            maze[rand_wall[0]][rand_wall[1]-1] = 'w'
                        if [rand_wall[0], rand_wall[1]-1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1]-1])

                    # Rightmost cell
                    if rand_wall[1] != width-1:
                        if maze[rand_wall[0]][rand_wall[1]+1] != 'c':
                            maze[rand_wall[0]][rand_wall[1]+1] = 'w'
                        if [rand_wall[0], rand_wall[1]+1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1]+1])

                # Delete wall
                for wall in walls:
                    if wall == rand_wall:
                        walls.remove(wall)

                return True

        return False


    def check_bottom_wall(self, maze, rand_wall, walls, height, width) -> bool:
        if rand_wall[0] != height-1:
            if maze[rand_wall[0]+1][rand_wall[1]] == 'u' and \
                    maze[rand_wall[0]-1][rand_wall[1]] == 'c':

                s_cells = self.surrounding_cells(maze, rand_wall)
                if s_cells < 2:
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    if rand_wall[0] != height-1:
                        if maze[rand_wall[0]+1][rand_wall[1]] != 'c':
                            maze[rand_wall[0]+1][rand_wall[1]] = 'w'
                        if [rand_wall[0]+1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0]+1, rand_wall[1]])
                    if rand_wall[1] != 0:
                        if maze[rand_wall[0]][rand_wall[1]-1] != 'c':
                            maze[rand_wall[0]][rand_wall[1]-1] = 'w'
                        if [rand_wall[0], rand_wall[1]-1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1]-1])
                    if rand_wall[1] != width-1:
                        if maze[rand_wall[0]][rand_wall[1]+1] != 'c':
                            maze[rand_wall[0]][rand_wall[1]+1] = 'w'
                        if [rand_wall[0], rand_wall[1]+1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1]+1])

                # Delete wall
                for wall in walls:
                    if wall == rand_wall:
                        walls.remove(wall)

                return True

        return False


    def check_right_wall(self, maze, rand_wall, walls, height, width) -> bool:
        if rand_wall[1] != width-1:
            if maze[rand_wall[0]][rand_wall[1]+1] == 'u' and \
                    maze[rand_wall[0]][rand_wall[1]-1] == 'c':

                s_cells = self.surrounding_cells(maze, rand_wall)
                if s_cells < 2:
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = 'c'

                    # Mark the new walls
                    if rand_wall[1] != width-1:
                        if maze[rand_wall[0]][rand_wall[1]+1] != 'c':
                            maze[rand_wall[0]][rand_wall[1]+1] = 'w'
                        if [rand_wall[0], rand_wall[1]+1] not in walls:
                            walls.append([rand_wall[0], rand_wall[1]+1])
                    if rand_wall[0] != height-1:
                        if maze[rand_wall[0]+1][rand_wall[1]] != 'c':
                            maze[rand_wall[0]+1][rand_wall[1]] = 'w'
                        if [rand_wall[0]+1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0]+1, rand_wall[1]])
                    if rand_wall[0] != 0:
                        if maze[rand_wall[0]-1][rand_wall[1]] != 'c':
                            maze[rand_wall[0]-1][rand_wall[1]] = 'w'
                        if [rand_wall[0]-1, rand_wall[1]] not in walls:
                            walls.append([rand_wall[0]-1, rand_wall[1]])

                # Delete wall
                for wall in walls:
                    if wall == rand_wall:
                        walls.remove(wall)

                return True

        return False


    def generate_prim_maze(self, height: int, width: int):
        if height < 3 or width < 3:
            raise Exception('Maze size need to be at least 3x3')

        wall = 'w'
        cell = 'c'
        unvisited = 'u'
        maze = []
        entrance_cell = ()
        exit_cell = ()

        # Denote all cells as unvisited
        for i in range(0, height):
            line = []
            for j in range(0, width):
                line.append(unvisited)
            maze.append(line)

        # Randomize starting point and set it a cell
        starting_height = self.np.randint(1, height-1)
        starting_width = self.np.randint(1, width-1)

        # Mark it as cell and add surrounding walls to the list
        maze[starting_height][starting_width] = cell
        walls = []
        walls.append((starting_height - 1, starting_width))  # Up of cell
        walls.append((starting_height, starting_width - 1))  # Left of cell
        walls.append((starting_height, starting_width + 1))  # Right of cell
        walls.append((starting_height + 1, starting_width))  # Down of cell

        # Denote walls in maze
        maze[starting_height-1][starting_width] = 'w'
        maze[starting_height][starting_width - 1] = 'w'
        maze[starting_height][starting_width + 1] = 'w'
        maze[starting_height + 1][starting_width] = 'w'

        while walls:
            # Pick a random wall
            rand_wall = walls[self.np.randint(0, len(walls))]

            # Check if it is a left wall
            to_next = self.check_left_wall(maze, rand_wall, walls, height)
            if to_next:
                continue

            # Check if it is an upper wall
            to_next = self.check_upper_wall(maze, rand_wall, walls, height)
            if to_next:
                continue

            # Check the bottom wall
            to_next = self.check_bottom_wall(maze, rand_wall, walls, height, width)
            if to_next:
                continue

            # Check the right wall
            to_next = self.check_right_wall(maze, rand_wall, walls, height, width)
            if to_next:
                continue

            # Delete the wall from the list anyway
            for wall in walls:
                if wall == rand_wall:
                    walls.remove(wall)

        # Mark the remaining unvisited cells as walls
        for i in range(0, height):
            for j in range(0, width):
                if maze[i][j] == 'u':
                    maze[i][j] = 'w'

        # Set entrance and exit
        for i in range(0, width):
            if maze[1][i] == 'c':
                maze[0][i] = 'c'
                entrance_cell = (0, i)
                break

        for i in range(width-1, 0, -1):
            if maze[height-2][i] == 'c':
                maze[height-1][i] = 'c'
                exit_cell = (height-1, i)
                break

        return maze, entrance_cell, exit_cell