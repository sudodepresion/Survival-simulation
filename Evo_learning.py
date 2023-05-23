import random
import math
import json

# load the names
with open(r"C:\Users\HpPav\source\repos\Evo-learning\Evo-learning\NameData.json", 'r') as f:
    jsonData = json.load(f)
    NamesForHumans = jsonData["HumanNames"]
    NamesForDisasters = jsonData["DisasterNames"]


#globals:
debugMode = input("Do you want to activate Debug mode? (y/n)") # debug mode only show the yearly overview and the ending

# fundamental functions, be carefull with them!

def randElementOfList(inpList):
    return inpList[random.randint(0, len(inpList)-1)]

def move(object, changeVec):
    object.position = vectorAddition2D(object.position, changeVec)

def vectorAddition2D(vector1,vector2):
    resultVector = []
    resultVector.append(vector1[0] + vector2[0])
    resultVector.append(vector1[1] + vector2[1])  
    return resultVector

def getEuclDistance(vec):
    distance = 0
    for coordinate in vec:
        distance += coordinate ** 2
    distance = math.sqrt(distance)
    return distance

def randomVec(minValue:int,maxValue:int):
    randomVec = [random.randint(minValue, maxValue),random.randint(minValue, maxValue)]
    return randomVec

def vecToStr(inpVec):
    resultStr = ""
    for i in range(len(inpVec)-1):
        resultStr += f"{inpVec[i]}:"
    resultStr += f"{lastElementOf(inpVec)}"
    return resultStr

def lastElementOf(inpList):
    return inpList[len(inpList) - 1]


# lists that sort all beeings
loP = list() # List of people 
lodP = list() # List of dead people

loL = list() # List of lions
lodL = list() # List of dead lions

loH = list() # List of Hybrids
lodH = list() # List of dead Hybrids

class Person:
    def __init__(self,name:str,doB:int, age:int, parent1:object, parent2:object, huntingSkill:int, PosVec:list):
        self.name = name
        self.dateOfBirth = doB
        self.finalAge = age
        self.dr = 0 # dr.. disasterRessistance
        self.parent1 = parent1
        self.parent2 = parent2
        self.children = []
        self.hs = huntingSkill
        self.dateOfDeath = -1
        self.deathReason = ""
        self.position = PosVec

class Lion: # the function createNewLion, and createLionsNoOrigin need to be updated as well!
    def __init__(self,dateOfBirth:int, age:int, huntingSkill:int, posVec:list):
        self.finalAge = age
        self.dateOfBirth = dateOfBirth
        self.hs = huntingSkill
        self.name = "a lion"
        self.dr = 0 # dr.. disasterRessistance
        self.children = []
        self.dateOfDeath = -1
        self.deathReason = ""
        self.position = posVec

class Hybrid():
    def __init__(self,name:str,doB:int, age:int, parent1:object, parent2:object, huntingSkill:int, posVec:list):
        self.name = name
        self.dateOfBirth = doB
        self.finalAge = age
        self.dr = 0 # dr.. disasterRessistance
        self.parent1 = parent1
        self.parent2 = parent2
        self.hs = huntingSkill
        self.dateOfDeath = -1
        self.deathReason = ""
        self.position = posVec


def createLionsNoOrigin(number):
    for i in range(number):
        loL.append(Lion(0,random.randint(180,240),shshLions,randomVec(-10,10)))

def createPeopleNoOrigin(number,minAge,maxAge):
    for i in range(number):
        randomName = NamesForHumans[random.randint(0,len(NamesForHumans)-1)]
        dateOfBirth = 0
        loP.append(Person("OG-"+ randomName,dateOfBirth, random.randint(minAge,maxAge), None, None, shsh, [random.randint(-10,10),random.randint(-10,10)]))


        
def deathHandler(object:object, days:int, years:int, reason:str):
    object.dateOfDeath = years * 365 + days
    object.deathReason = reason
    if isinstance(object, Person):
        lodP.append(object)
        loP.remove(object)
    elif isinstance(object, Lion):
        lodL.append(object)
        loL.remove(object)
    elif isinstance(object, Hybrid):
        lodH.append(object)
        loH.remove(object)
    if debugMode == "y":
        print(f"{object.name} has died!")

def murder(person1, victim, days, years):
    if not isinstance(victim, Hybrid):
        if person1 != victim:
            if debugMode == "y":
                print(f"{person1.name} has killed {victim.name}")
            deathHandler(victim, days, years, f"murder by {person1.name}")
        else:
            if debugMode == "y":
                print(f"{person1.name} has endet their own life.")
            deathHandler(victim, days, years, f"suicide")

def lionEncounter(days, years):
    if len(loP) > 0 and len(loL) > 0:
        if debugMode == "y":
            print("-------------------------------")
            print("A lion has attacked!")
        choosenHuman = randElementOfList(loP)
        choosenLion = randElementOfList(loL)
        if choosenHuman.hs < choosenLion.hs:
            murder(choosenLion,choosenHuman, days, years)
        elif choosenHuman.hs == choosenLion.hs:
            if debugMode == "y":
                print(f"{choosenHuman} and {choosenLion} where an equal match")
            if random.randint(1,2) == 1:
                if debugMode == "y":
                    print("They both died")
                deathHandler(choosenLion, days, years,"battle")
                deathHandler(choosenHuman, days, years,"battle")
            else: 
                if debugMode == "y":
                    print("They both survived")
        elif choosenHuman.hs > choosenLion.hs:
                murder(choosenHuman, choosenLion, days, years)
        if debugMode == "y":
                print("-------------------------------")

def massDeathAnouncement(choosenDisaster, numberOfDeathsLions, numberOfDeathsPeople):
    print("------------------------")
    print(f"Oh no, there was a {choosenDisaster}")
    print(f"{numberOfDeathsPeople} people died!")
    print(f"{numberOfDeathsLions} lions died!")
    print("------------------------")

def massDeath(numberOfDeathsPeople,numberOfDeathsLions, days, years):
    choosenDisaster = randElementOfList(NamesForDisasters)
    if debugMode == "y":
        massDeathAnouncement(choosenDisaster, numberOfDeathsLions, numberOfDeathsPeople)
    for i in range(numberOfDeathsPeople):
        choosenPerson = randElementOfList(loP)
        
        if random.randint(0,1000) > 1000/(1 + choosenPerson.dr):
            if debugMode == "y":
                print(f"{choosenPerson.name} has survived the disaster")
        else: deathHandler(choosenPerson, days, years,f"{choosenDisaster}")
    for i in range(numberOfDeathsLions):
        choosenLion = randElementOfList(loL)
        if random.randint(0,1000) > 1000/(1 + choosenLion.dr):
            if debugMode == "y":
                print(f"{choosenLion.name} has survived the disaster")
        else: deathHandler(choosenLion, days, years,f"{choosenDisaster}")          
    if len(loP) > 0:
        randElementOfList(loP).dr += 1
    if len(loL) > 0:
        randElementOfList(loL).dr += 1




def createNewPerson(days,years,parent1, parent2):
    # creates a new Person
    if debugMode == "y":
        print(f"A new Person! Parents: {parent1.name} & {parent2.name}")
    randomName = NamesForHumans[random.randint(0,len(NamesForHumans)-1)]
    dateOfBirth = days + (years * 365)
    finalAge = (parent1.finalAge + parent2.finalAge)/2 + random.randint(round(-mFac/2),mFac)
    huntingSkill = (parent1.hs + parent2.hs) / 2 + random.randint(round(-hFac/2),hFac)
    child = Person(randomName,dateOfBirth,finalAge, parent1, parent2, huntingSkill, parent1.position)
    loP.append(child)
    # One of two ways to gain dr. The other is through surviving a disaster
    if parent1.dr >= 1 and parent2.dr >= 1:
        child.dr = 2
    elif parent1.dr >= 1 or parent2.dr >= 1:
        child.dr = 1
    # informs parents
    parent1.children.append(child)
    parent2.children.append(child)

def createNewLion(days,years,parent1, parent2):
    # creates a new Lion
    if debugMode == "y":
        print("A new Lion was born")
    dateOfBirth = days + (years * 365)
    finalAge = (parent1.finalAge + parent2.finalAge)/2 + random.randint(round(-mFac/2),mFac)
    huntingSkill = (parent1.hs + parent2.hs) / 2 + random.randint(round(-hFac/2),hFac)
    child = Lion(dateOfBirth,finalAge, huntingSkill, parent1.position)
    loL.append(child)
    # One of two ways to gain dr. The other is through surviving a disaster
    if parent1.dr >= 1 and parent2.dr >= 1:
        child.dr = 2
    elif parent1.dr >= 1 or parent2.dr >= 1:
        child.dr = 1
    # informs parents
    parent1.children.append(child)
    parent2.children.append(child)

def repopulation(days,years):
    if len(loP) >= 2 and len(loP) <= maxHumansAlive : 
        for person in loP:
            if len(person.children) < maxChildren:
                if random.randint(0,1000) < rrc:
                    createNewPerson(days, years, randElementOfList(loP),randElementOfList(loP))
    if len(loL) >= 2 and len(loL) <= maxLionsAlive: 
        for lion in loL:
            if len(lion.children) < maxChildrenLion:
                if random.randint(0,1000) < rrcLion:
                    createNewLion(days,years,randElementOfList(loL),randElementOfList(loL))
    if len(loL) >= 2 and len(loP) >= 2:
        if random.randint(1,1000) < rrcHybrid:
            createNewHybrid(days,years,randElementOfList(loP),randElementOfList(loL))
                  
def createNewHybrid(days,years,parent1,parent2):
    if debugMode == "y":
        print(f"A new Hybrid! Parents: {parent1.name} & {parent2.name}")
    randomName = "Hb-" + randElementOfList(NamesForHumans)
    dateOfBirth = days + (years * 365)
    finalAge = (parent1.finalAge + parent2.finalAge) * 2 + random.randint(round(mFac/2),mFac)
    huntingSkill = (parent1.hs + parent2.hs) * 2 + random.randint(round(hFac/2),hFac)
    newHybrid = Hybrid(randomName,dateOfBirth,finalAge, parent1, parent2, huntingSkill, parent1.position)
    loH.append(newHybrid)
    # One of two ways to gain dr. The other is through surviving a disaster
    if parent1.dr >= 1 and parent2.dr >= 1:
        newHybrid.dr = 2
    elif parent1.dr >= 1 or parent2.dr >= 1:
        newHybrid.dr = 1
    # informs parents
    parent1.children.append(newHybrid)
    parent2.children.append(newHybrid)




def anounceNewDay(days,years):
    print(f"Its the day {days} of the year {years}")

def eventsOfTheDay(days,years):
    if debugMode == "y":
        anounceNewDay(days, years)      
    repopulation(days,years)
    # Collect the dead
    for person in loP:
        if person.finalAge + person.dateOfBirth < days + (years * 365):
            deathHandler(person,days, years, "old age")
    for lion in loL:
        if lion.finalAge + lion.dateOfBirth < days + (years * 365):
            deathHandler(lion, days, years, "old age")
    for Hybrid in loH:
        if Hybrid.finalAge + Hybrid.dateOfBirth < days + (years * 365):
            deathHandler(Hybrid, days, years, "old age")
    # disasters
    if random.randint(0,100) < dpc * (len(loP)**2)/100:
        massDeath(random.randint(round(len(loP)*0.5),round(len(loP)*0.6)),random.randint(round(len(loL)*0.5),round(len(loL)*0.6)), days, years)
    if random.randint(1,100) < murderChance :
        murder(randElementOfList(loP),randElementOfList(loP), days, years)
    if len(loL) > 1 and random.randint(1,100) < murderChance :
        murder(randElementOfList(loL),randElementOfList(loL), days, years)
    if random.randint(1,100) < lec:
        lionEncounter(days, years)
    # movement
    dailyHumanMovement()

def yearlyReport(year):
    print(f"------------------------------------------------------------------")
    print(f"The year {year} is over!")
    print(f"These {len(loP)} people are still alive:")
    for person in loP:
        print(f"{person.name:<12} | life expectancy:{round(person.finalAge):<12} | D-Res: {person.dr}")
    print("------------------------------------------------------------------")

def dailyHumanMovement():
    for person in loP:
        move(person,[random.randint(round(-humanSpeed),humanSpeed),random.randint(round(-humanSpeed),humanSpeed)])

def endOfTheWorld(days,years,special:bool):
    print(f"-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_")
    print("Breaking News! The last person on earth just died!")
    if not special: # special only acours with the killALl() function
        if len(loL) > 0: print(f"The lions won! There are still {len(loL)} lions alive")
        else: print(f"The humans won by {days+(365*years)-lodL[len(lodL) - 1].dateOfDeath} days") 
    print(f"Survived until: {days}-{years}")
    print(f"Number of all humans that ever existed: {len(lodP)}")
    print(f"Number of all lions that ever existed: {len(lodL)}")
    print(f"Number of all Hybrids that ever existed: {len(lodH)}")
    printComparisonStatsHuman()
    printComparisonStatsLion()
    if len(lodH) > 0:
        printComparisonStatsHybrid()
    if input("Get the family tree of the last survivor? (y/n)") == "y":
       getFamilyTree(lodP[len(lodP) - 1])
    if input("Get the family tree of the last Hybrid? (y/n)") == "y":
       getFamilyTree(lodH[len(lodH) - 1])
    if input("Do you want to run the simulation again? (y/n)") == "y":
        resetLists()
        main()
    else:   quit()

def getFamilyTree(person):
    childOfPerson = person
    generationCount = 0
    print(childOfPerson.name)
    while childOfPerson.parent1 != None:
        generationCount += 1
        print(" | ")
        print(f"{childOfPerson.parent1.name}<-{childOfPerson.parent2.name}")
        childOfPerson = childOfPerson.parent1
    print(f"They are the {generationCount}th generation!")

def printComparisonStatsHuman():
    firstHuman = lodP[1]
    lastHuman = lodP[len(lodP)-1]
    print("-------------------------------------------------------------")
    print(f"                    1. human    --  last human")
    print(f"name:               {firstHuman.name:<12}--  {lastHuman.name}")
    print(f"life expectancy:    {round(firstHuman.finalAge,2):<12}--  {round(lastHuman.finalAge,2)}")
    print(f"hunting power:      {firstHuman.hs:<12}--  {round(lastHuman.hs,2)}")
    print(f"death reason:       {firstHuman.deathReason:<12}--  {lastHuman.deathReason}")
    print(f"death time:         {firstHuman.dateOfDeath:<12}--  {lastHuman.dateOfDeath}")
    print(f"death position:     {vecToStr(firstHuman.position):<12}--  {vecToStr(lastHuman.position)}")
    print(f"Distance to origin: {round(getEuclDistance(firstHuman.position),2):<12}--  {round(getEuclDistance(lastHuman.position),2)}")
    print("-------------------------------------------------------------")

def printComparisonStatsLion():
    firstLion = lodL[1]
    lastLion = lodL[len(lodL)-1]
    print("-------------------------------------------------------------")
    print(f"                    1. lion     --  last lion")
    print(f"life expectancy:    {firstLion.finalAge:<12}--  {round(lastLion.finalAge,2)}")
    print(f"hunting power:      {firstLion.hs:<12}--  {round(lastLion.hs,2)}")
    print(f"death reason:       {firstLion.deathReason:<12}--  {lastLion.deathReason}")
    print(f"death time:         {firstLion.dateOfDeath:<12}--  {lastLion.dateOfDeath}")
    print(f"death position:     {vecToStr(firstLion.position):<12}--  {vecToStr(lastLion.position)}")
    print(f"Distance to origin: {round(getEuclDistance(firstLion.position),2):<12}--  {round(getEuclDistance(lastLion.position),2)}")
    print("-------------------------------------------------------------")

def printComparisonStatsHybrid():
    firstHybrid = lodH[1]
    lastHybrid = lodH[len(lodH)-1]
    print("-------------------------------------------------------------")
    print(f"                    1. Hybrid   --  last Hybrid")
    print(f"name:               {firstHybrid.name:<12}--  {lastHybrid.name}")
    print(f"life expectancy:    {firstHybrid.finalAge:<12}--  {round(lastHybrid.finalAge,2)}")
    print(f"hunting power:      {firstHybrid.hs:<12}--  {round(lastHybrid.hs,2)}")
    print(f"death reason:       {firstHybrid.deathReason:<12}--  {lastHybrid.deathReason}")
    print(f"death time:         {firstHybrid.dateOfDeath:<12}--  {lastHybrid.dateOfDeath}")
    print(f"death position:     {vecToStr(firstHybrid.position):<12}--  {vecToStr(lastHybrid.position)}")
    print(f"Distance to origin: {round(getEuclDistance(firstHybrid.position),2):<12}--  {round(getEuclDistance(lastHybrid.position),2)}")

    print("-------------------------------------------------------------")

 
def killAll(days,years):
    for lion in loL:
        deathHandler(lion, days,years,"Killed by a divine force")
    for person in loP:
        deathHandler(person, days,years,"Killed by a divine force")
    endOfTheWorld(days,years, True)

def resetLists():
    lop  = [] 
    lodp = []
    
    lol  = []
    lodl = []
    
    loh  = []
    lodh = []
    
def main():
    createPeopleNoOrigin(saP, 340, 450)
    createLionsNoOrigin(saL)
    for years in range(timeSpan+1):
        for days in range(365):
            if len(loP) != 0:
                eventsOfTheDay(days,years)
            else: endOfTheWorld(days,years, False)
        yearlyReport(years)
        # end the simulation early incase it goes on past the given time span
        if years == timeSpan - 1:
            killAll(days,years)




# Parameters
timeSpan = 100 # in years
# general - Human
rrc = 175 # Repopulation random chance in 1/1000
shsh = 1 # start hunting skill of humans
shshLions = 3 # start hunting skill of lions
maxChildren = 2
maxHumansAlive = 150
humanSpeed = 10
saP = 20 # Starting amount People
# general - Lion
rrcLion = 165 # Repopulation random chance in 1/1000 for lions
maxChildrenLion = 2
maxLionsAlive = 150
saL = 20 # starting amount Lions
# general - Hybrid
rrcHybrid = 150 # Repopulation random chance in 1/1000 for Hybrids
# mutation
hFac = 2 # hunting skill mutation Factor
mFac = 25 # age mutation Factor
# death
dpc = 15 # disaster random chance
murderChance = 10 # in Percent
lec = 1 # lion encounter chance in percent



main()