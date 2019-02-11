# Cameron Rodriguez
# DATE GOES HERE
# This program is a game that determines whether humans are kept safe from zombies.

# This module is used to validate the source text file.
import re

"""
This function will read the file, verify the data, and save it to a list.

text_file: STR: the location of the file containing the game map

game_source: FILE:  the file that contains the text form of the game map
source_raw: STR: raw form of the entire file, used for verification
source_lines: LIST: a list storing each line of game_source, used to load game_map
source_line_length: INT: contains the length of the first line, to ensure all lines are the same length
all_zombies: LIST: contains data on the location of all zombies
one_zombie: INT: keeps track while adding location of zombies to all_zombies

game_map: LIST: the returned list that stores the game map
"""
def load_map(text_file):
    game_map = []
    all_zombies = []
    one_zombie = 0
    
    # Open and read the file, then split into lines
    with open(text_file, 'r') as game_source:
        source_raw = game_source.read()
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
            one_zombie += source_raw.find('Z', one_zombie)
            line = (one_zombie / source_line_length)
            all_zombies.append([line, one_zombie-(line*source_line_length)])
            one_zombie += 1
        except ValueError:
            break
    # End while True

    # Load game data into all_zombies, with a list of rows containing a list of characters
    for l in range(len(source_lines)):
        one_row = [source_lines[l][i] for i in range(len(source_lines[l]))]
        game_map.append(one_row)
    # End for l 
    game_map.append(all_zombies)

    return game_map
# End def load_map

'''
This recursive function calls itself to spread zombies until they cannot expand further.

game: LIST: the nested list of locations on the map
first: LIST: contains the location of the first zombie, with the first slot telling which zombie to use
current: LIST: identifies the current zombie being spread, in format [row][column]
broken: LIST: a temporary list used to replace all broken walls with dots
x: INT: indicates the row of the current zombie
y: INT: indicates the column of the current zombie
'''
def invasion(game, first, current):
    broken = []
    if current == []:
        current = first[first[0]]
    # End if current
    x, y = current
    
    # Spread zombies across the map
    if game[x-1][y] not in ['Z', 'T']: # Zombie spread up
        if game[x-1][y] in ['.', 'H']:
            game[x-1][y] = invade_human_dot(game, current, 0)
            if game[x-1][y] in ['.', 'H']: # Checks if valuwe changed
                pass
            else:
                invasion(game, first, [x-1, y])
            # End if game[x-1][y]
        else:
            broken = break_wall(game, current)
        # End if game[x-1][y]
    elif game[x+1][y] not in ['Z', 'T']: # Zombie spread down
        if game[x+1][y] in ['.', 'H']:
            game[x+1][y] = invade_human_dot(game, current, 1)
            if game[x+1][y] in ['.', 'H']: # Checks if valuwe changed
                pass
            else:
                invasion(game, first, [x+1, y])
            # End if game[x+1][y]            
        else:
            broken = break_wall(game, current)
        # End if game[x+1][y]
    elif game[x][y-1] not in ['Z', 'T']: # Zombie spread left
        if game[x][y-1] in ['.', 'H']:
            game[x][y-1] = invade_human_dot(game, current, 2)
            if game[x][y-1] in ['.', 'H']: # Checks if valuwe changed
                pass
            else:
                invasion(game, first, [x, y-1])
            # End if game[x][y-1]            
        else:
            broken = break_wall(game, current)
        # End if game[x][y-1]
    elif game[x][y+1] not in ['Z', 'T']: # Zombie spread right
        if game[x][y+1] in ['.', 'H']:
            game[x][y+1] = invade_human_dot(game, current, 3)
            if game[x][y+1] in ['.', 'H']: # Checks if valuwe changed
                pass
            else:
                invasion(game, first, [x, y+1])
            # End if game[x][y+1]            
        else:
            broken = break_wall(game, current)
        # End if game[x][y+1]
        
'''
This function fills a human or empty spot if that spot is not on the opposite side of the map to the original point.

game: LIST: the nested list of locations on the map
current: LIST: identifies the current zombie being spread, in format [row][column]
direction: INT: identifies which way the zombie would spread, in format 0=up 1=down 2=left 3=right
x: INT: indicates the row of the current zombie
y: INT: indicates the column of the current zombie
width: INT: indicates the width of the map
height: INT: indicates the height of the map
'''
def invade_human_dot(game, current, direction):
    x, y = current
    width = len(game[0])
    height = len(game)
    
    # Verify new zombie does not jump to other side of map
    if direction == 0: # Spread up
        if game[x-1] is game[height-1]:
            return game[x-1][y]
        else:
            return 'Z'
        # End if game[x-1]
    elif direction == 1: # Spread down
        if game[x+1] is game[0]:
            return game[x+1][y]
        else:
            return 'Z'
        # End if game[x+1]
    elif direction == 2: # Spread left
        if game[x][y-1] is game[x][width-1]:
            return game[x][y-1]
        else:
            return 'Z'
        # End if game[x][y+1]
    elif direction == 3: # Spread up
        if game[x][y+1] is game[x][0]:
            return game[x][y+1]
        else:
            return 'Z'
        # End if game [x][y+1]
    # End if direction
# End def invade_human_dot

'''
This function checks if 15 zombies are present to break down a wall, and also checks if nearby walls also can break.

game: LIST: the nested list of locations on the map
current: LIST: identifies the current zombie being spread, in format [row][column]
'''
def break_wall(game, current):
    pass
