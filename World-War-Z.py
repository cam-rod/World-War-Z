# Cameron Rodriguez
# DATE GOES HERE
# This program is a game that determines whether humans are kept safe from zombies.

# This module is used to validate the source text file.
import re

"""
Data Dictionary

game_map: LIST: a 2D array of the game playing field, in format [row][column]
all_zombies: LIST: stores location of starting zombies; first slot tells game which zombie to use
game_setup: LIST: contains game_map and all_zombies, and verifies if file location is valid
width: INT: the width of the map
height: INT: the height of the map
x: INT: indicates the row of the zombie being checked for spreading
y: INT: indicates the column of the zombie being checked for spreading

text_file: STR: the location of the file containing the game map
game_source: FILE:  the file that contains the text form of the game map
source_raw: STR: raw form of the entire file, used for verification
source_lines: LIST: a list storing each line of game_source, used to load game_map
source_line_length: INT: contains the length of the first line, to ensure all lines are the same length
one_zombie: INT: keeps track while adding location of zombies to all_zombies
direction: INT: indicates the direction relative to [x][y] of zombie infection or breaking wall
"""

# This function will read the file, verify the data, and return the map and zombies via 2 lists.
def load_map(text_file):
    game_map = []
    all_zombies = []
    one_zombie = 0
    
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
    
    # Locate all zombies in the map, and append within a list as the final list value
    while True:
        if one_zombie >= len(source_raw):
            break
        # End if one_zombie
        try:
            one_zombie += source_raw.index('Z', one_zombie)
            line = (one_zombie / source_line_length)
            all_zombies.append([line, one_zombie-(line*source_line_length)])
            one_zombie += 1
        except ValueError:
            break
        # End try/except
    # End while True

    # Load game data into game_map, with a list of rows containing a list of characters
    for l in range(len(source_lines)):
        one_row = [source_lines[l][i] for i in range(len(source_lines[l]))]
        game_map.append(one_row)
    # End for l 

    return [game_map, all_zombies]
# End def load_map


# This recursive function calls itself to spread zombies until they cannot expand further.
def invasion(game_map, all_zombies, x, y):

    # Spread zombies across the map
    if game_map[x-1][y] not in ['Z', 'T']: # Zombie spread up
        if game_map[x-1][y] in ['.', 'H']:
            game_map[x-1][y] = invade_human_dot(game_map, x, y, 0)
            if game_map[x-1][y] in ['.', 'H']: # Checks if value changed
                pass
            else:
                print_map(game_map)
                invasion(game_map, all_zombies, x-1, y)
            # End if game_map[x-1][y]
        else:
            break_wall(game_map, x, y, 0)
        # End if game_map[x-1][y]
    elif game_map[x+1][y] not in ['Z', 'T']: # Zombie spread down
        if game_map[x+1][y] in ['.', 'H']:
            game_map[x+1][y] = invade_human_dot(game_map, x, y, 1)
            if game_map[x+1][y] in ['.', 'H']: # Checks if value changed
                pass
            else:
                print_map(game_map)
                invasion(game_map, all_zombies, x+1, y)
            # End if game_map[x+1][y]            
        else:
            break_wall(game_map, x, y, 1)
        # End if game_map[x+1][y]
    elif game_map[x][y-1] not in ['Z', 'T']: # Zombie spread left
        if game_map[x][y-1] in ['.', 'H']:
            game_map[x][y-1] = invade_human_dot(game_map, x, y, 2)
            if game_map[x][y-1] in ['.', 'H']: # Checks if value changed
                pass
            else:
                print_map(game_map)
                invasion(game_map, all_zombies, x, y-1)
            # End if game_map[x][y-1]            
        else:
            break_wall(game_map, x, y, 2)
        # End if game_map[x][y-1]
    elif game_map[x][y+1] not in ['Z', 'T']: # Zombie spread right
        if game_map[x][y+1] in ['.', 'H']:
            game_map[x][y+1] = invade_human_dot(game_map, x, y, 3)
            if game_map[x][y+1] in ['.', 'H']: # Checks if value changed
                pass
            else:
                print_map(game_map)
                invasion(game_map, all_zombies, x, y+1)
            # End if game_map[x][y+1]            
        else:
            break_wall(game_map, x, y, 3)
        # End if game_map[x][y+1]
        

# This function fills a human/empty spot if it's not on the opposite side of the map.
# This function uses the global vars width and height.
def invade_human_dot(game_map, x, y, direction):
    # Verify new zombie does not jump to other side of map
    if direction == 0: # Spread up
        if game_map[x-1] is game_map[height-1]:
            return game_map[x-1][y]
        else:
            return 'Z'
        # End if game_map[x-1]
    elif direction == 1: # Spread down
        if game_map[x+1] is game_map[0]:
            return game_map[x+1][y]
        else:
            return 'Z'
        # End if game_map[x+1]
    elif direction == 2: # Spread left
        if game_map[x][y-1] is game_map[x][width-1]:
            return game_map[x][y-1]
        else:
            return 'Z'
        # End if game_map[x][y+1]
    elif direction == 3: # Spread up
        if game_map[x][y+1] is game_map[x][0]:
            return game_map[x][y+1]
        else:
            return 'Z'
        # End if game_map[x][y+1]
    # End if direction
# End def invade_human_dot

# This function checks for 15 zombies to break a wall, and then checks nearby walls as well.
# This function uses the global vars width and height.
def break_wall(game_map, x, y, direction):
    pass

# This function joins the 2D array game_map into a string and prints it when called.
def print_map(game_map):
    for i in range(len(game_map)):
        print ''.join(game_map[i])
    # End for i

    print '\n'

game_map = []
all_zombies = []
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
        game_map, all_zombies = game_setup
        print 'Let the invasion begin!'
        break
    # End if game_setup
# End while True

print_map(game_map)

width = len(game_map[0])
height = len(game_map)

try:
    x = all_zombies[1][0]
    y = all_zombies[1][1]
    invasion(game_map, all_zombies, x, y)
except IndexError:
    print 'There were never any zombies, so you survived!'
# End try/except
