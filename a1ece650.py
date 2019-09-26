from __future__ import division
import sys
import math
import random
import re


streets_and_cordinates={}
main_V=set()
mid_point=set()
temp_allEdges=set()
temp_Edges=set()
temp_Blindspot=set()
vertex={}
Edges=set()


def validate(text):

    validate=0

    code = text.split('"')

    if (code[0] == 'g' and len(code)==1):
        return True

    if (code[0]=='r ' and len(code)==3):
        fake=code[1]
        bunny=fake.replace(" ","")
        case1 = re.sub("[a-zA-Z]+","",bunny)
        if (case1=='' and code[2]==''):
            return True
        else:
            sys.stderr.write("Error: Invalid Street Name for 'r'\n")
            return False
    else:

        if len(code) ==3:
            validate+=1
        else:
            return False


        if code[0]!='g':
            if len(code[0])!=2:
                sys.stderr.write("Error: Wrong Action command\n")
                return False
            else:
                first=re.compile(r"^[ac]\s")
                if first.match(code[0]):
                    validate +=1
                else:
                    sys.stderr.write("Error: Wrong Action command\n")
                    return False


        second=code[1]
        temp=second.replace(" ","")
        case1 = re.sub("[a-zA-Z]+","",temp)
        if case1 =='':
            validate+=1
        else:
            sys.stderr.write("Error: Wrong Street Name\n")
            return False


        line=code[2]
        cont=0
        for i in range(len(line)):
            if line[0] == " ":
                cont=1
                break

        if cont!=1:
            sys.stderr.write("Error: Wrong coordinate sequence\n")
            return False
        else:
            third = re.sub("([(][0-9(-.+)]+[,][0-9(-.+)]+[)])","",line)
            if third ==" ":
                validate+=1
            else:
                sys.stderr.write("Error: Wrong coordinate sequence\n")
                return False

    if validate != 4:
        sys.stderr.write("Error: Wrong command\n")
        return False
    else:
        lastcheck=structure_cordinates(code[2])
        if ( (code[0]=="a " or code[0]=="c ") and len(lastcheck)>=2):
            return True
        else:
            sys.stderr.write("Error: Coordinate is incomplete or not provided\n")
            return False

    if validate==4:
        return True



def operations(text):
    code = text.split('"')

    if code[0] == 'a ':
        val = streets_and_cordinates.get(code[1].lower(),'Not Found')
        if val == 'Not Found':
            streets_and_cordinates.update({code[1].lower():code[2]})
            print("Output: ")
            print(streets_and_cordinates)
        else:
            sys.stderr.write("Error: Street Name Exist for command 'a'.\n")
    elif code[0] == 'c ':
        val = streets_and_cordinates.get(code[1].lower(),'Not Found')
        if val == 'Not Found':
            sys.stderr.write("Error: Street Name doesn't exist for 'c' command.\n")
        else:
            streets_and_cordinates.update({code[1].lower():code[2]})
            print("Output: ")
            print(streets_and_cordinates)
    elif code[0] == 'r ':
        val = streets_and_cordinates.get(code[1].lower(),'Not Found')
        if val == 'Not Found':
            sys.stderr.write("Error: Street Name doesn't exist. Specify valid street for 'r'.\n")
        else:
            streets_and_cordinates.pop(code[1].lower())
            print("Output: ")
            print(streets_and_cordinates)
    elif code[0] == 'g':
        generate()
    else:
        sys.stderr.write("Error: wrong command\n")


def generate():
    #reset matrix
    main_V.clear()
    mid_point.clear()
    temp_allEdges.clear()
    temp_Edges.clear()
    temp_Blindspot.clear()
    vertex.clear()
    Edges.clear()
    # streets_and_cordinates must have 2 streets


    streets={}
    trial=[]

    for key, value in streets_and_cordinates.items():
        streets.update({key:random.randint(1,10001)})


    for key1, value1 in streets_and_cordinates.items():
        for key2, value2 in streets_and_cordinates.items():
            if key1 != key2:
                val1=streets.get(key1) + streets.get(key2)
                if val1 not in trial:
                    trial.append(val1)
                    analytics(value1,value2)

    matrix()
    #print("Vertex: ")
    #print(main_V)
    #print("MIDPOINT: ")
    #print(mid_point)
    #print("Edges: ")
    #print(temp_allEdges)
    #print('Number: ')
    #print(len(temp_allEdges))
    #print('temp_Edges: ')
    #print(temp_Edges)
    #print('Total temp_Edges: ')
    #print(len(temp_Edges))
    #print('Total temp_Blindspot: ')
    #print(temp_Blindspot)
    #print("'\n'")
    sys.stdout.write("V: ")
    sys.stdout.write(str(vertex))
    sys.stdout.write("\n")
    sys.stdout.write("\n")
    sys.stdout.write("E: ")
    sys.stdout.write(str(list(Edges)))
    sys.stdout.write("\n")





def analytics(value1,value2):
    org_val1 = structure_cordinates(value1)
    org_val2 = structure_cordinates(value2)

    numA=0
    numB=1
    for i in range (0,len(org_val1)-1):
        numC=0
        numD=1
        for i in range (0,len(org_val2)-1):
            ans = intersect(org_val1[numA],org_val1[numB],org_val2[numC],org_val2[numD])
            if ans != 0:
                 store_values(ans,org_val1[numA],org_val1[numB],org_val2[numC],org_val2[numD])
            numC += 1
            numD += 1

        numA += 1
        numB += 1




def structure_cordinates(value):
    cold=[]
    hold1=""
    hold2=""
    start=False
    newVal=False
    temp=value.replace(" ","")

    for i in range (len(temp)):
        if temp[i] == "(":
            start=True
            newVal=False

        if temp[i] == ",":
            newVal=True

        if (start and newVal == False and temp[i] != "(" and temp[i] != ","and temp[i] != ")"):
            hold1 += temp[i]

        if (start and newVal == True and temp[i] != "(" and temp[i] != ","and temp[i] != ")"):
            hold2 += temp[i]

        if temp[i] == ")":
            start=False
            newVal=False
            points=tuple([int(hold1),int(hold2)])
            cold.append(points)
            hold1=""
            hold2=""

    return cold


def intersect(valA,valB,valC,valD):
    xdiff = ((valA[0]-valB[0]),(valC[0]-valD[0]))
    ydiff = ((valA[1]-valB[1]),(valC[1]-valD[1]))

    div = (xdiff[0] * ydiff[1])-( xdiff[1] * ydiff[0])

    if div == 0:
        # Lines do not intersect
        return 0


    d1 = (valA[0] * valB[1])-(valA[1] * valB[0])
    d2 = (valC[0] * valD[1])-(valC[1] * valD[0])
    d = (d1,d2)
    x1 = (d[0] * xdiff[1])-( d[1] * xdiff[0])
    x = round((x1 / div),7)
    y1 = (d[0] * ydiff[1])-(d[1] * ydiff[0])
    y = round((y1 / div),7)

    vector1= round((math.sqrt((valA[0]*valA[0])+(valA[1]*valA[1]))),7)
    vector2= round((math.sqrt((valB[0]*valB[0])+(valB[1]*valB[1]))),7)
    vector1a= round((math.sqrt((valC[0]*valC[0])+(valC[1]*valC[1]))),7)
    vector2a= round((math.sqrt((valD[0]*valD[0])+(valD[1]*valD[1]))),7)
    vectorx= round((math.sqrt(round((x*x),7)+round((y*y),7))),7)
    maximum= max(vector1,vector2)
    minimum= min(vector1,vector2)
    maximumA= max(vector1a,vector2a)
    minimumA= min(vector1a,vector2a)

    if (vectorx>=minimum and vectorx<=maximum and vectorx>=minimumA and vectorx<=maximumA):
        # Lines intersect
        return x,y
    else:
        # Lines do not intersect
        return 0



def store_values(ans,valA,valB,valC,valD):
    mid_point.add(ans)
    main_V.add(ans)
    main_V.add(valA)
    main_V.add(valB)
    main_V.add(valC)
    main_V.add(valD)
    coords=tuple((valA,ans))
    temp_allEdges.add(coords)
    coords=tuple((ans,valB))
    temp_allEdges.add(coords)
    coords=tuple((valC,ans))
    temp_allEdges.add(coords)
    coords=tuple((ans,valD))
    temp_allEdges.add(coords)




def matrix():
    validate=True
    edge=list(temp_allEdges)

    for indx in range(len(temp_allEdges)):
        edge_set=edge[indx]
        validate=True
        for key1, value1 in streets_and_cordinates.items():
            org_street=structure_cordinates(value1)
            numC=0
            numD=1
            for step in range(len(org_street)-1):
                middle_point=middle(edge_set)
                meeting_point=intersect(edge_set[0],edge_set[1],org_street[numC],org_street[numD])
                if meeting_point != 0:
                    if meeting_point not in edge_set:
                        validate=False
                        coords=tuple([middle_point,meeting_point])
                        check_BlindSpot_Duplicate(middle_point,meeting_point)
                numC+=1
                numD+=1
        if validate == True:
            temp_Edges.add(edge_set)

    checkBlindSpots()
    unique_ID()



def unique_ID():
    id=0
    main=list(main_V)
    keep=list(temp_Edges)

    for indx in range(len(main_V)):
        id += 1
        temp=main[indx]
        store=(round(temp[0],2),round(temp[1],2))
        vertex.update({id:store})

    for step in range(len(temp_Edges)):
        fort=keep[step]
        night1=fort[0]
        night2=fort[1]
        winter1=(round(night1[0],2),round(night1[1],2))
        winter2=(round(night2[0],2),round(night2[1],2))
        final1=0
        final2=0
        for key, mate in vertex.items():
            if winter1 == mate:
                final1=key
                break
        for key1, mate1 in vertex.items():
            if winter2 == mate1:
                final2=key1
                break
        xxx = "<{},{}>".format(final1,final2)
        Edges.add(xxx)



def check_BlindSpot_Duplicate(value1,value2):
    validate=True
    if len(temp_Blindspot) != 0:
        bp=list(temp_Blindspot)
        for indx in range(len(temp_Blindspot)):
            bp_set=bp[indx]
            bp_setA=bp_set[0]
            bp_setB=bp_set[1]
            vector1= round((math.sqrt((bp_setA[0]**2)+(bp_setA[1]**2))),7)
            vector2= round((math.sqrt((bp_setB[0]**2)+(bp_setB[1]**2))),7)
            vector1a= round((math.sqrt((value1[0]**2)+(value1[1]**2))),7)
            vector2a= round((math.sqrt((value2[0]**2)+(value2[1]**2))),7)
            maximum= max(vector1,vector2)
            minimum= min(vector1,vector2)
            maximumA= max(vector1a,vector2a)
            minimumA= min(vector1a,vector2a)
            if (maximum==maximumA and minimum==minimumA):
                validate=False

        if validate==True:
            coords=tuple([value1,value2])
            temp_Blindspot.add(coords)
    else:
        coords=tuple([value1,value2])
        temp_Blindspot.add(coords)



def checkBlindSpots():
    validate=True
    edge=list(temp_Blindspot)

    for indx in range(len(temp_Blindspot)):

        edge_set=edge[indx]
        validate=True
        for key1, value1 in streets_and_cordinates.items():
            org_street=structure_cordinates(value1)
            numC=0
            numD=1
            for step in range(len(org_street)-1):
                middle_point=middle(edge_set)
                meeting_point=intersect(edge_set[0],edge_set[1],org_street[numC],org_street[numD])
                if meeting_point != 0:
                    if meeting_point not in edge_set:
                        validate=False
                numC+=1
                numD+=1
        if validate == True:
            temp_Edges.add(edge_set)


def middle(val1):
    mid_p=list(mid_point)
    for index in range(len(mid_p)):
        if mid_p[index] in val1:
            return mid_p[index]


def main():

    while True:
        print('Input Valid Command: ')
        command = raw_input() #raw_input()  #str(sys.stdin.readline())
        if command == '':
            break

        try:
            if validate(command):
                operations(command)
            else:
                sys.stderr.write("Error: wrong command\n")
        except Exception:
            sys.stderr.write("Error: wrong command\n")

    ## return exit code 0 on successful termination
    sys.exit(0)



if __name__ == '__main__':
    main()

