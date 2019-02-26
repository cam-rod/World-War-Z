# Cameron Rodriguez
# DATE GOES HERE
# This program is a game that determines whether humans are kept safe from zombies.

# This module is used to validate the source text file.
import re
import time

"""
Data Dictionary

game: LIST: a 2D array of the game playing field, in format [row][column]
game_setup: LIST/BOOL: returned list of game, x, and y; this is False if setup fails
width: INT: the width of the map
height: INT: the height of the map
x: INT: indicates the row of the zombie being checked for spreading
y: INT: indicates the column of the zombie being checked for spreading
line_length: INT: contains the length of the first line, to ensure all lines are the same length and to verify zombies don't jump across map
"""

# This function will read the file, verify the data, and return the map and zombies via 2 lists.
# text_file: the directory location of the file
# Returns false if the file location or the file itself is invalid
# Returns the game_map, and coordinates of the first zombie if the file and its location is valid
def load_map(text_file):
    """
    Data Dictionary

    game_source: FILE:  the file that contains the text form of the game map
    source_raw: STR: raw form of the entire file, used for verification
    source_lines: LIST: a list storing each line of game_source, used to load game
    first_zombie: INT: a temporary list indicating the location of one zombie in source_raw
    """
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
    line_length = len(source_lines[0])
    
    # Validate game_source has 1 human, only contains valid characters, and is a rectangle
    if len(re.findall('H', source_raw)) >= 1:
        if re.search(r'[^HWTZ.\n]', source_raw) is None:
            for l in source_lines[1:]:
                if len(l) == line_length:
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
        x = first_zombie / line_length
        if first_zombie % line_length == 0:
            x -= 1
        # End if first_zombie
        y = first_zombie % line_length - x
        if y < 0:
            y = line_length + y
        # End if y
    except ValueError:
        # Indicates there are no zombies
        x = -1
    # End try/except

    # Load game data into game, with a list of rows containing a list of characters
    for l in range(len(source_lines)):
        one_row = [source_lines[l][i] for i in range(len(source_lines[l]))]
        game.append(one_row)
    # End for l 

    return [game, x, y, line_length]
# End load_map


# This recursive function calls itself to spread zombies until they cannot expand further.
# game: the list containing the game and locations of all components
# x: the row of the current zombie trying to spread
# y: the column of the current zombie trying to spread
# Returns the updated game map
def invasion(game, x, y):

    # Check if any walls should be broken
    break_wall(game)

    # Spread zombies across the map recursively, by checking for valid move before content of space
    if not_border(game, x, y, 0) and game[x-1][y] not in ['Z', 'T', 'W']: # Zombie spread up
        game[x-1][y] = 'Z'
        print_map(game)
        game = invasion(game, x-1, y)
        # End if not_border
    if not_border(game, x, y, 1) and game[x+1][y] not in ['Z', 'T', 'W']: # Zombie spread down
        game[x+1][y] = 'Z'
        print_map(game)
        game = invasion(game, x+1, y)
    if not_border(game, x, y, 2) and game[x][y-1] not in ['Z', 'T', 'W']: # Zombie spread left
        game[x][y-1] = 'Z'
        print_map(game)
        game = invasion(game, x, y-1)
        # End if not_border
    if not_border(game, x, y, 3) and game[x][y+1] not in ['Z', 'T', 'W']: # Zombie spread right
        game[x][y+1] = 'Z'
        print_map(game)
        game = invasion(game, x, y+1)
    # End if not_border
    
    # Exit this recursion level and check previous zombies
    return game
# End invasion

# This function verifies that an movement will not jump to the other side of the map.
# This function uses the global vars width and height.
# game: the list containing the game and locations of all components
# x: the row of the current zombie trying to spread
# y: the column of the current zombie trying to spread
# direction: indicates the direction the zombie is trying to spread
# Returns True if expansion will not jump to other side of map, returns False otherwise
def not_border(game, x, y, direction):
    # Verify movement does not jump to other side of map
    if direction == 0: # Spread up
        if x-1 == -1:
            return False
        else:
            return True
        # End if game[x-1]
    elif direction == 1: # Spread down
        if x+1 == len(game):
            return False
        else:
            return True
        # End if game[x+1]
    elif direction == 2: # Spread left
        if y-1 == -1:
            return False
        else:
            return True
        # End if game[x][y+1]
    elif direction == 3: # Spread right
        if y+1 == line_length:
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
    """
    Data Dictionary
    
    zombie_chain: STR: 15 spaces in one direction, to be checked if they are all zombies
    """
    zombie_chain = ''
    for i in range(len(game)):
        for j in range(len(game[i])):
            if game[i][j] == 'W':
                # Check for 15 zombies in each direction, then recursively call the program
                # After completing a full run, return the game map to reduce recursion levels
                if i >=15: # Scan up
                    for c in range(1,16):
                        zombie_chain += game[i-c][j]
                    # End for c
                    if not re.search(r'[^Z]', zombie_chain):
                        try:
                            if re.search(r'[.]', game[i+1][j]):
                                game[i][j] = 'Z'
                                print_map(game)
                                game = invasion(game, i, j)
                            # End if re.search
                        except IndexError:
                            game[i][j] = 'Z'
                            print_map(game)
                            game = invasion(game, i, j)
                        # End try/except
                    else:
                        zombie_chain = ''
                    # End if re.search
                # End if i
                if height - i - 1 >= 15: # Scan down
                    for c in range(1,16):
                        zombie_chain += game[i+c][j]
                    # End for c
                    if not re.search(r'[^Z]', zombie_chain):
                        if re.search(r'[.]', game[i-1][j]) or i-1 == -1:
                            game[i][j] = 'Z'
                            print_map(game)
                            game = invasion(game, i, j)
                        # End if re.search
                    else:
                        zombie_chain = ''
                    # End if re.search
                # End if height
                if j >= 15: # Scan left
                    for c in range(1,16):
                        zombie_chain += game[i][j-c]
                    # End for c
                    if not re.search(r'[^Z]', zombie_chain):
                        try:
                            if re.search(r'[.]', game[i][j+1]):
                                game[i][j] = 'Z'
                                print_map(game)
                                game = invasion(game, i, j)
                            # End if re.search
                        except IndexError:
                            game[i][j] = 'Z'
                            print_map(game)
                            game = invasion(game, i, j)
                        # End try/except
                    else:
                        zombie_chain = ''
                    # End if re.search
                # End if j
                if width - j - 1 >= 15: # Scan right
                    for c in range(1,16):
                        zombie_chain += game[i][j+c]
                    # End for c
                    if not re.search(r'[^Z]', zombie_chain):
                        if re.search(r'[.]', game[i][j-1]) or j-1 == -1:
                            game[i][j] = 'Z'
                            print_map(game)
                            game = invasion(game, i, j)
                        # End if re.search
                    else:
                        zombie_chain = ''
                    # End if re.search
                # End if width
            # End if game[i][j]
        # End for j
    # End for i
    return game
# End break_wall

# This function will return the location of a zombie if the current chain can no longer expand
# game: the list containing the game and locations of all components
# Returns the final map
def new_zombie(game):
    # Check if every zombie only neighbours W/T/Z, else run invasion on that zombie
    for i in range(len(game)):
        for j in range(len(game[i])):
            if game[i][j] == 'Z':
                if not_border(game, i, j, 0) and game[i-1][j] not in ['W', 'T', 'Z']: # Check up
                    game = invasion(game, i, j)
                elif not_border(game, i, j, 1) and game[i+1][j] not in ['W', 'T', 'Z']: # Check down
                    game = invasion(game, i, j)
                elif not_border(game, i, j, 2) and game[i][j-1] not in ['W', 'T', 'Z']: # Check left
                    game = invasion(game, i, j)
                elif not_border(game, i, j, 3) and game[i][j+1] not in ['W', 'T', 'Z']: # Check right
                    game = invasion(game, i, j)
                # End if not_border
            # End if game[i][j]
        # End for j
    # End for i

    return game
# End new_zombie

# This function joins the 2D array game into a string and prints it.
# game: the list containing the game and locations of all components
def print_map(game):
    """
    Data Dictionary
    
    game_str: STR: string form of the current game map
    """
    game_str = ''
    for i in range(len(game)):
        game_str += ''.join(game[i])
        game_str += '\n'
    # End for i

    print game_str
    time.sleep(0.05)
# End print_map

# This function determines if any humans survived, and prints an appropriate message.
# game: the list containing the game and locations of all components
def endgame(game):
    """
    Data Dictionary
    
    game_str: STR: string form of the current game map
    survivors: INT: number of humans still on the map
    """
    # Join the map into one string and check for humans
    game_str = ''
    for i in range(len(game)):
        game_str += ''.join(game[i])
    # End for i
    survivors = len(re.findall('H', game_str))

    if survivors == 0:
        print 'All humans were killed in the invasion.'
        print 'You died!'
    else:
        print 'In the end, {} human{} survived the invasion.'.format(survivors, \
                                                                    's' if survivors <> 1 else '')
        print 'You survived!'
    # End if survivors

    print '\nThanks for playing World War Z!'
    time.sleep(3)
# End endgame

game = []
x = 0
y = 0
line_length = 0
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
        game, x, y, line_length = game_setup
        break
    # End if game_setup
# End while True

print_map(game)

width = len(game[0])
height = len(game)

if x == -1:
    print '\nThere were never any zombies.'
    print 'You survived!'

    print '\nThanks for playing World War Z!'
    time.sleep(3)
else:
    print '\nLET THE INVASION BEGIN!\n'
    time.sleep(0.5)
    game = invasion(game, x, y)
    game = new_zombie(game) # Find a new zombie if original zombie is exhausted
    endgame(game)
# End if x
