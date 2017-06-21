

import random
trials=20

WIDTH = 25
HEIGHT = 25
NUMSTATES = 5

class Program(object):
    def __init__(self):
        ''' initializes the Picobot program '''
        self.rules = {}

    def __repr__(self):
        ''' returns the string representation of the program '''
        Keys = list( self.rules.keys() )
        SortedKeys = sorted( Keys )
        s = ''
        for i in SortedKeys:
            s += str(i[0]) + ' ' + str(i[1]) + ' -> ' + str(self.rules[i][0]) + ' ' + str(self.rules[i][1])
            s += '\n'
        return s

    def randomize(self):
        ''' makes a completely random set of Picobot rules '''
        pattern = ['xxxx','Nxxx','NExx','NxWx','xxxS','xExS','xxWS','xExx','xxWx']
        POSSIBLE_MOVES = ['x','N','E','W','S']
        states = [0,1,2,3,4]
        for i in states:
            for j in pattern:
                movedir = random.choice( POSSIBLE_MOVES )
                movestr = random.choice( states )
                while movedir in j:
                    movedir = random.choice( POSSIBLE_MOVES )
                self.rules[(i,j)] = (movedir, movestr)

    def getMove(self, state, surroundings):
        ''' returns the next move '''
        return self.rules[(state, surroundings)]

    def mutate(self):
        POSSIBLE_MOVES = ['x','N','E','W','S']
        states = [0,1,2,3,4]
        key = random.choice(list(self.rules.keys()))
        movedir = random.choice( POSSIBLE_MOVES )
        movestr = random.choice( states )

        while movedir in key[1]:
            movedir = random.choice( POSSIBLE_MOVES )

        self.rules[key] = (movedir, movestr)

    def __gt__(self,other):
        ''' greater than operator - works randomly, but works! '''
        return random.choice( [ True, False ] )

    def __lt__(self,other):
        ''' less than operator - works randomly, but works! '''
        return random.choice( [ True, False ] )

    def crossover(self, other):
        offspringDict = {}
        pattern = ['xxxx','Nxxx','NExx','NxWx','xxxS','xExS','xxWS','xExx','xxWx']
        POSSIBLE_MOVES = ['x','N','E','W','S']
        states = [0,1,2,3,4]
        cstate = random.choice([1,2,3])

        for i in range(cstate + 1): 
            for j in pattern:
                offspringDict[i,j] = self.rules[i,j]

        for i in range(cstate, 5):
            for j in pattern:
                offspringDict[i,j] = other.rules[i,j]

        offspringProgram = Program()
        offspringProgram.rules = offspringDict

        return offspringProgram

class World(object):
    def __init__(self, initialRow, initialCol, program):
        ''' initializes the Picobot world '''
        self.prow = initialRow
        self.pcol = initialCol
        self.state = 0
        self.prog = program
        self.room = [ [' ']*WIDTH for row in range(HEIGHT) ]
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if i == self.prow and j == self.pcol:
                    self.room[i][j] = 'P'
                elif i == 0 or i == HEIGHT-1 or j == 0 or j == HEIGHT-1:
                    self.room[i][j] = '+'

    def __repr__(self):
        ''' returns the string representation of the world '''
        world = ''
        for i in range(HEIGHT):
            for j in range(WIDTH):
                world += self.room[i][j]
            world += '\n'
        return world

    def getCurrentSurroundings(self):
        ''' this method returns a surrounding string'''
        surr = ''

        if self.room[self.prow-1][self.pcol]=="+":
            surr = surr + 'N'
        else:
            surr = surr + 'x'  


        if self.room[self.prow][self.pcol+1]=="+":
            surr = surr + 'E'
        else:
            surr = surr + 'x'  

        if self.room[self.prow][self.pcol-1]=="+":
            surr = surr + 'W'
        else:
            surr = surr + 'x'

        if self.room[self.prow+1][self.pcol]=="+":
            surr = surr + 'S'
        else:
            surr = surr + 'x'    

        return surr





        # if self.room[self.prow+1][self.pcol]=="+":
        #     return "xxxS"

        # if self.room[self.prow][self.pcol-1]=="+":
        #     return 'xExx'

        # if self.room[self.prow][self.pcol+1]=='+':
        #     return 'xxWx'
        # if self.room[self.prow-1][self.pcol]=="+" and self.room[self.prow][self.pcol-1]=="+":
        #     return "NExx"

        # if self.room[self.prow-1][self.pcol]=="+" and self.room[self.prow][self.pcol+1]=='+':
        #     return "NxWx"

        # if self.room[self.prow+1][self.pcol]=="+" and self.room[self.prow][self.pcol-1]=="+":
        #     return "xExS"

        # if self.room[self.prow+1][self.pcol]=="+" and self.room[self.prow][self.pcol+1]=='+':

        #     return "xxWS"

        # else:
        #     return 'xxxx'

    def step(self):
        ''' this method moves picobot one step'''

        surr= self.getCurrentSurroundings()
        nextMove= self.prog.getMove(self.state,surr)
        #print(nextMove)

        if nextMove[0]== 'N':                                 # ask if get move returns a list
            self.room[self.prow-1][self.pcol]='P'
            self.room[self.prow][self.pcol]='o'
            self.prow-=1
        elif nextMove[0]== 'S':
            self.room[self.prow+1][self.pcol]='P'
            self.room[self.prow][self.pcol]='o'
            self.prow+=1

        elif nextMove[0]=='W':
            self.room[self.prow][self.pcol-1]='P'
            self.room[self.prow][self.pcol]='o'
            self.pcol-=1
        elif nextMove[0]=='E':
            self.room[self.prow][self.pcol+1]='P'
            self.room[self.prow][self.pcol]='o'
            self.pcol+=1
        else:
              self.room[self.prow][self.pcol]='P'

        self.state = nextMove[1]


    def run(self,steps):
        ''' this method executes the number of steps the picobot should move'''
        for i in range(steps):
            self.step()


    def fractionVisitedCells(self):
        ''' this method returns the fraction of cells that had been visited by the picobot P'''
        TotalSquares= HEIGHT*WIDTH
        numVisited=0
        for i in range(HEIGHT):
            for j in range(WIDTH):

                if self.room[i][j]=="o" or self.room[i][j]=='P':
                    numVisited= numVisited+1
                else:
                    numVisited=numVisited+0

        return numVisited/(23*23)


def population(popsize):
    ''' this function returns a list of popsize Picobot programs'''

    L=[]
    for i in range(popsize):
        prog= Program() 
        prog.randomize()
        
        L= L+[prog]

    return L

def evalutateFitness(program,trials,steps):
    ''' this function measures the fitness of a given picobot program'''
    steps=800
    Total=0
    for i in range(trials):
        randRow= random.choice(list(range(1,HEIGHT-1)))
        randCol= random.choice(list(range(1,HEIGHT-1)))
        WORLD= World(randRow,randCol,program)  
        WORLD.run(steps) 
        fract=WORLD.fractionVisitedCells()
        Total= Total+fract

    return Total/trials

def GA(popsize,numgens):
    ''' this is the main function, which returns the best and fittest picobot set of rules'''
    steps=800
    RANGE= int((20/100)*(popsize))

    prog= population(popsize)
    L=[]
    P = []
    OFFSPRINGS=[]

    
    for j in range(numgens):
        print("gen number ", j)
        

        for i in range(popsize):

            fitness= evalutateFitness(prog[i],trials,steps)
            L=L+[(fitness,prog[i])]

        

            


        SL= sorted(L)
        
        
       # print("Best:", SL[-1])
        print("Best Fitness:", SL[-1][0])
        
        
        ExtractedPrograms= SL[-RANGE:]
        P = []
        for programs in ExtractedPrograms:
            p1 = programs[1]
            if random.choice(range(10)) == 0:
                p1.mutate()
            P= P + [ p1 ]

        OFFSPRINGS = []
        for x in range(180):
            randomParent1= random.choice(P)
            randomParent2= random.choice(P)

            offspring= randomParent1.crossover(randomParent2)

            #FITNESS= evalutateFitness() 
            OFFSPRINGS= OFFSPRINGS+ [offspring]

        prog = P + OFFSPRINGS

    return SL[-1]


        







    


program = Program()
program.randomize()

world = World(10,1,program)
print(program)
print(world)
# surr = world.getCurrentSurroundings()
# print("surr is",surr)
# world.step()
# print(world)
for i in range(10):
     world.step()
     print(world)

v= world.fractionVisitedCells()
print(v)
