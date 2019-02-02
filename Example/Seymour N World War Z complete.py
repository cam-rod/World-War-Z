#Nolan Seymour 
#9/13/18
#World War Z assignment

"""
Data dictonary

changeMade: INT : Tracks number of changes made and activates recursive call if not equal to 0
found: INT : Tracks number of H's remain after spread of Z's
lived: INT : Activates message on survival based off number of H's remaining in the file
zombieCount: INT : Track number of zombies before a wall going left to right
zombieCount2: INT : Tracks number of zombies before wall used in right to left wall breaking code
survive: STR : Holds message on if any humans survived or did not survive
feild: ARRAY : Recieves the field from text file
feildChange: ARRAY : Recieves the field from feild array and holds changes made to it
"""

#This procedure will search for a Z and make all adjacent tiles into Z if it is not a wall
#This procudure will call itself until no more tiles can be changed
def search():
    changeMade=0
    
    for x in range (0,15,1):
        zombieCount=0
        zombieCount2=0
        for y in range (0,40,1):
            
            """Zombie spreading code"""
            ##Left zombie spreading
            if feildChange[x][y]=="Z":
                if feildChange[x][y-1]=="." or feildChange[x][y-1]=="H":
                    if y-1<0:
                        pass
                    else:
                        feildChange[x][y-1]="Z"
                        changeMade=+1
                    #end if y
                #end if feildCahnge 
            #end if feildChange
            
            ##Up zombie spreading
            if feildChange[x][y]=="Z":
                if y+1>39:
                    if x+1>14:
                        x=x-1
                    #end if x
                    if feildChange[x+1][y]=="." or feildChange[x+1][y]=="H":
                            feildChange[x+1][y]="Z"
                            changeMade=+1
                    #end if feildChange
                else:
                    if y+1>39:
                        y=y-1
                    #end if y
                    if feildChange[x][y+1]=="." or feildChange[x][y+1]=="H":
                        feildChange[x][y+1]="Z"
                        changeMade=+1
                        #end if y
                    #end if feildChange
                #end if feildChange
            #end if feildChange
            
            ##Down zombie spreading
            if feildChange[x][y]=="Z":
                if feildChange[x-1][y]=="." or feildChange[x-1][y]=="H":
                    if x-1<0:
                        pass
                    else:
                        feildChange[x-1][y]="Z"
                        changeMade=+1
                    #end if x
                #end if feildChange
            #end if feildChange
            
            ##Right zombie spreading
            if feildChange[x][y]=="Z":
                if x+1>14:
                    if y+1>39:
                        y=y-1
                    #end if y
                    if feildChange[x][y+1]=="." or feildChange[x][y+1]=="H":
                        feildChange[x][y+1]="Z"
                        changeMade=+1
                    #end if feildChange
                else:
                    if x+1>14:
                        x=x-1
                    #end if x
                    if feildChange[x+1][y]=="." or feildChange[x+1][y]=="H":
                        feildChange[x+1][y]="Z"
                        changeMade=+1
                    #end if feild Change
                #end if x
            #end if feildChange
            
            """Zombie breaking walls code"""
            ##Left to right wall breaking
            if feildChange[x][y]=="Z":
                zombieCount+=1
                if feildChange[x][y]=="W" and zombieCount<=15:
                    zombieCount=0
                #end if feildChange                
                if zombieCount>15:
                    if y>=38:
                        if feildChange[x][39]=="W":
                            feildChange[x][39]="Z"
                            changeMade+=1
                        #end if feildChange
                    else:
                        if feildChange[x][y+1]=="W" and feildChange[x][y+2]=="W":
                            zombieCount=0
                        else:
                            pass
                        #end if feildChange
                        if zombieCount>=15 and feildChange[x][y+2]==".":
                            feildChange[x][y+1]="Z"
                            changeMade+=1
                        #end if feildChange
                    #end if y
                #end if zombieCount
                
                ##Right to left wall breaking
                if feildChange[x][y]=="Z":
                    zombieCount2+=1
                #end if zombieCount2
                if zombieCount2>=15:
                    if y-15<0:
                        pass
                    else:
                        if y-16<0:
                            if feildChange[x][y-15]=="W":
                                feildChange[x][0]="Z"
                                changeMade+=1
                            #end if feildChange
                        #end if y
                        if feildChange[x][y-16]=="." and feildChange[x][y-14]=="Z":                        
                            feildChange[x][y-15]="Z"
                            changeMade+=1
                        #end if feildChange
                    #end if y
                elif feildChange[x][y]=="W":
                    zombieCount2=0
                #end if zombieCount2
            #end if feildChange
        #end for y
    #end for x
    
    """Recursive call"""
    if changeMade>=0:
        pass
    else:
        changeMade=0
    #end if changeMade
    
    if changeMade<>0:
        search()
    #end while changeMade
#end def search

lived=0
find=0
survive=""

"""File opening and handling"""
f=open("1.04 World War Z Input.txt")
feild=[]
feildChange=[["" for x in range (40)] for y in range (15)]

string=f.readline()
while (string!=""):
    string=string.strip() 
    feild.append(string)
    string=f.readline()
#end while string

f.close()

for x in range (0,15,1):
    for y in range (0,40,1):
            feildChange[x][y]=feild[x][y]
    #end for y
#end for x

search()

"""Final check and printing of content"""
for x in range (0,15,1):
    print ""
    for y in range (0,40,1):
        print feildChange[x][y],
    #end for y
#end for x

for i in range (0,40,1):
    for j in range (0,len(feild),1):
        find=feildChange[j][i]
        if find=="H":
            lived+=1
        else:
            pass
        #end if find'
    #end for j
#end for i

print ""

if lived<>0:
    survive="You survived!"
else:
    survive="You did not survive!"
#end if lived

print survive