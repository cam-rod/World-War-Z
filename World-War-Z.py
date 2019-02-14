# Cameron Rodriguez
# DATE GOES HERE
# This program is a game that determines whether humans are kept safe from zombies.

# This module is used to validate the source text file.
import re

"""
Data Dictionary

game: LIST: a 2D array of the game playing field, in format [row][column]
game_setup: LIST/BOOL: returned list of game, x, and y; this is False if setup fails
width: INT: the width of the map
height: INT: the height of the map
x: INT: indicates the row of the zombie being checked for spreading
y: INT: indicates the column of the zombie being checked for spreading

text_file: STR: the location of the file containing the game map
game_source: FILE:  the file that contains the text form of the game map
source_raw: STR: raw form of the entire file, used for verification
source_lines: LIST: a list storing each line of game_source, used to load game
source_line_length: INT: contains the length of the first line, to ensure all lines are the same length
first_zombie: INT: a temporary list indicating the location of one zombie in source_raw
previous_zombies: LIST: a nested array of all zombies in the current branch of invading, allows for checking in reverse
direction: INT: indicates the direction relative to [x][y] of zombie infection or breaking wall
zombie_chain: STR: 15 spaces in one direction, to be checked if they are all zombies
game_str: STR: string form of the current game map
"""

# This function will read the file, verify the data, and return the map and zombies via 2 lists.
# text_file: the directory location of the file
# Returns false if the file location or the file itself is invalid
# Returns the game_map, and coordinates of the first zombie if the file and its location is valid
def load_map(text_file):
    game = []
    first_zombie = 0
    x = 0
    y = 0
    
    # Open and read the file, then split into lines
    try:
        with open(text_file, 'r') as game_source:
            source_raw = game_source.read()
        # End with open(text_file, 'r')
    except IOError:
        return False
    # End try/except
    source_lines = source_raw.splitlines()
    source_line_length = len(source_lines[0])
    
    # Validate game_source has 1 human, only contains valid characters, and is a rectangle
    if len(re.findall('H', source_raw)) == 1:
        if re.search(r'[^HWTZ.\n]', source_raw) is None:
            for l in source_lines[1:]:
                if len(l) == source_line_length:
                    continue
                else:
                    return False
                # End if len(l)
            # End for l, file has been validated
        else:
            return False
        # End if re.search        
    else:
        return False        
    # End if re.findall
    
    # Locate one zombies in the map, and assign to x and y
    try:
        first_zombie += source_raw.index('Z')
        x = first_zombie / source_line_length
        y = first_zombie % source_line_length
    except ValueError:
        # Indicates there are no zombies
        x = -1
    # End try/except

    # Load game data into game, with a list of rows containing a list of characters
    for l in range(len(source_lines)):
        one_row = [source_lines[l][i] for i in range(len(source_lines[l]))]
        game.append(one_row)
    # End for l 

    return [game, x, y]
# End load_map


# This recursive function calls itself to spread zombies until they cannot expand further.
# game: the list containing the game and locations of all components
# x: the row of the current zombie trying to spread
# y: the column of the current zombie trying to spread
# previous_zombies: a nested array of all zombies in the current branch of invading, allows for checking in reverse
def invasion(game, x, y, previous_zombies):
    # Check if any walls should be broken
    game = break_wall(game)

    # Spread zombies across the map recursively
    if game[x-1][y] not in ['Z', 'T', 'W']: # Zombie spread up
        if not_border(game, x, y, 0): # Checks if value changed
            game[x-1][y] = 'Z'
            previouus_zombies.append([x-1, y])
            print_map(game)
            invasion(game, x-1, y, previous_zombies)
        else:
            pass
        # End if not_border
    elif game[x+1][y] not in ['Z', 'T', 'W']: # Zombie spread down
        if not_border(game, x, y, 1):
            game[x+1][y] = 'Z'
            previouus_zombies.append([x+1, y])
            print_map(game)
            invasion(game, x+1, y, previous_zombies)
        else:
            pass
        # End if not_border
    elif game[x][y-1] not in ['Z', 'T', 'W']: # Zombie spread left
        if not_border(game, x, y, 2):
            game[x][y-1] = 'Z'
            previouus_zombies.append([x, y-1])
            print_map(game)
            invasion(game, x, y-1, previous_zombies)
        else:
            pass
        # End if not_border
    elif game[x][y+1] not in ['Z', 'T', 'W']: # Zombie spread right
        if not_border(game, x, y, 3):
            game[x][y+1] = 'Z'
            previouus_zombies.append([x, y+1])
            print_map(game)
            invasion(game, x, y+1, previous_zombies)
        else:
            pass
        # End if not_border
    elif previous_zombies <> []:
        # Try to invade in a different direction from the previous zombie
        x, y = previous_zombies[-1]
        del previous_zombies[-1]
        invasion(game, x, y, previous_zombies)
    else:
        # Finally, check if every zombie only neighbours W/T/Z, else run invasion on that zombie
        for i in range(len(game)):
            for j in range(len(game[i])):
                if all(v in ['W', 'T', 'Z'] for v in [game[i-1][j], game[i+1][j], game[i][j-1], game[i][j+1]]):
                    continue
                else:
                    previous_zombies = []
                    invasion(game, i, j, previous_zombies)
                # End if all()
            # End for j
        # End for i
    # End if game
    endgame(game)
# End invasion

# This function verifies that an movement will not jump to the other side of the map.
# This function uses the global vars width and height.
# game: the list containing the game and locations of all components
# x: the row of the current zombie trying to spread
# y: the column of the current zombie trying to spread
# direction: indicates the direction the zombie is trying to spread
# Returns True if expansion will not jump to other side of map, returns False otherwise
def not_border(game, x, y, direction):
    # Verify new zombie does not jump to other side of map
    if direction == 0: # Spread up
        if game[x-1] is game[height-1]:
            return False
        else:
            return True
        # End if game[x-1]
    elif direction == 1: # Spread down
        if game[x+1] is game[0]:
            return False
        else:
            return True
        # End if game[x+1]
    elif direction == 2: # Spread left
        if game[x][y-1] is game[x][width-1]:
            return False
        else:
            return True
        # End if game[x][y+1]
    elif direction == 3: # Spread up
        if game[x][y+1] is game[x][0]:
            return False
        else:
            return True
        # End if game[x][y+1]
    # End if direction
# End not_border

# This function checks for 15 zombies to break a wall, and re-checks if one is broken.
# This function uses the global vars width and height.
# game: the list containing the game and locations of all components
# Returns the updated game map
def break_wall(game):
    for i in range(len(game)):
        for j in range(len(game[i])):
            zombie_chain = ''
            if game[i][j] == 'W':
                # Check for 15 zombies in each direction, then recursively call the program
                # After completing a full run, return the game map along each recursion to keep program from staying trapped in if/for statements
                if i + 1 >=15: # Scan up
                    for c in range(len(15)):
                        zombie_chain += game[i-c][j]
                    # End for c
                    if re.search(r'[^Z]', zombie_chain):
                        try:
                            if re.search('.', game[i+1][j]):
                                game[i][j] = 'W'
                                print_map(game)
                                game = break_wall(game)
                                return game
                            # End if re.search
                        except IndexError:
                            game[i][j] = 'W'
                            print_map(game)
                            game = break_wall(game)
                            return game
                        # End try/except
                    # End if re.search
                # End if i
                if height - i + 1 >= 15: # Scan down
                    for c in range(len(15)):
                        zombie_chain += game[i+c][j]
                    # End for c
                    if re.search(r'[^Z]', zombie_chain):
                        if re.search('.', game[i-1][j]) and game[i-1][j] is not game[height-1][j]:
                            game[i][j] = 'W'
                            print_map(game)
                            game = break_wall(game)
                            return game
                        # End if re.search
                    # End if re.search
                # End if height
                if j + 1 >= 15: # Scan left
                    for c in range(len(15)):
                        zombie_chain += game[i][j-c]
                    # End for c
                    if re.search(r'[^Z]', zombie_chain):
                        try:
                            if re.search('.', game[i][j+1]):
                                game[i][j] = 'W'
                                print_map(game)
                                game = break_wall(game)
                                return game
                            # End if re.search
                        except IndexError:
                            game[i][j] = 'W'
                            print_map(game)
                            game = break_wall(game)
                            return game
                        # End try/except
                    # End if re.search
                # End if j
                if width - j + 1 >= 15: # Scan right
                    for c in range(len(15)):
                        zombie_chain += game[i][j+c]
                    # End for c
                    if re.search(r'[^Z]', zombie_chain):
                            if re.search('.', game[i][j-1]) and game[i][j-1] is not game[i][width-1]:
                                game[i][j] = 'W'
                                print_map(game)
                                game = break_wall(game)
                                return game
                            # End if re.search
                    # End if re.search
                # End if width
            # End if game[i][j]
        # End for j
    # End for i
    return game
# End break_wall

# This function joins the 2D array game into a string and prints it.
# game: the list containing the game and locations of all components
def print_map(game):
    game_str = ''
    for i in range(len(game)):
        game_str += ''.join(game[i])
        game_str += '\n'
    # End for i

    print game_str
# End print_map

# This function determines if any humans survived, and prints an appropriate message.
# game: the list containing the game and locations of all components
def endgame(game):
    pass
# End endgame

game = []
x = 0
y = 0
previous_zombies = []
game_setup = False

print '==========WORLD WAR Z==========\n'

# Generate the game map
while True:
    text_file = raw_input('Please enter the directory location of your map: ')
    game_setup = load_map(text_file)
    if game_setup is False:
        print 'This is not a valid file, please try again.\n'
        continue
    else:
        game, x, y = game_setup
        break
    # End if game_setup
# End while True

print_map(game)

width = len(game[0])
height = len(game)

if x == -1:
    print '\nThere were never any zombies.'
    print 'You survived!'
else:
    print '\nLET THE INVASION BEGIN!\n'
    invasion(game, x, y, previous_zombies)
# End if x
