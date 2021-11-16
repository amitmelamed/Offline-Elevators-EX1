import subprocess
import sys
import json
import csv
from random import randrange

from tkinter import *

# to run the algorithem
# python3 Ex1_eran.py Ex1_Buildings/B5.json Ex1_Calls/Calls_a.csv output.csv
# to run the tester
# java -jar libs/Ex1_checker_V1.2_obf.jar 1111,2222,3333 data/Ex1_input/Ex1_Buildings/B5.json output.csv out.log


# "function that gets a call and returns allocated elevator"
#
"very stupid algoritem that works good for buildings with 2 elevators"
# def allocateElevatorB3(call):
#     fastElevatorIndex = 0
#     slowElevatorIndex = 1
#     if (elevators[0].speed > elevators[1].speed):
#         fastElevatorIndex = 1
#         slowElevatorIndex = 0
#     floorsCount = maxFloor - minFloor

#     if (int(call.destination) < floorsCount / 3):
#         call.allocatedElevator = slowElevatorIndex
#     else:
#         call.allocatedElevator = fastElevatorIndex
#
#
# "function that gets a call and returns allocated elevator"
# def allocateElevator(call):
#     "we check if we have only 2 elevators we will use better algoritem for small buildings"
#     if (len(elevators) == 2):
#         allocateElevatorB3(call)
#         return
#
#     minTime = call.calcTime(elevators[0])
#     minIndex = 0
#     for i in range(len(elevators)):
#         currentTime = call.calcTime(elevators[i])
#         if (currentTime < minTime):
#             minTime = currentTime
#             minIndex = i
#     call.allocatedElevator = minIndex
#     elevators[minIndex].position = call.destination
#     elevators[minIndex].callsQueue.append(call)
#     for e in elevators:
#         e.clearCompleteCalls(call)


"elevetor class:"
"each elevator has id,speed,minFloor, maxFloor, closeTime, openTime, startTime, stopTime"
class Elevator:
    def __init__(self, id, speed, minFloor, maxFloor, closeTime, openTime, startTime, stopTime, spf, mood):
        self.id = id
        self.speed = speed
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.closeTime = closeTime
        self.openTime = openTime
        self.startTime = startTime
        self.stopTime = stopTime
        self.position = 0
        self.callsQueue = []
        self.arrfloose = []
        self.spf = spf
        self.mood = mood
        "mood up = 1 , mood down = 0, mood idle = 2"

    def toString(self):
        return "id:" + str(self.id) + " speed:" + str(self.speed) + " minFloor:" + str(
            self.minFloor) + " maxFloor:" + str(self.maxFloor) + " closeTime:" + str(
            self.closeTime) + " openTime:" + str(self.openTime) + " startTime:" + str(
            self.startTime) + " stopTime:" + str(self.stopTime) + "position: " + str(self.position)

    def clearCompleteCalls(self, call):
        count = 0
        for i in self.callsQueue:
            if (float(i.time) < float(call.time) - 30):
                count = count + 1
        for i in range(count):
            self.callsQueue.pop(0)


"call class: each call has time, source, destination, allocatedElevator"
class Call:
    def __init__(self, time, source, destination, allocatedElevator):
        self.time = time
        self.source = source
        self.destination = destination
        self.allocatedElevator = allocatedElevator
        self.absFloor = abs(int(source) - int(destination))

    def toString(self):
        return ("time:" + str(self.time) + " source:" + str(self.source) + " destination:" + str(
            self.destination) + " allocatedElevator:" + str(self.allocatedElevator))

    # def calcTime(self, elevator):
    #     calc = elevator.openTime + elevator.closeTime + speed * self.absFloor + abs(
    #         int(elevator.position) - int(call.source))
    #     calc = calc * len(elevator.callsQueue)
    #     return calc


"sys.argv is a function that gets the input from the terminal and puts its in an array"
"buildint will be the string that represent building.json location that we want to use for input"
"calls will be the string that represent calls.csv location that we want to use for input"
"output will be the string that represent outPut.csv location that we want to use fo output"
list = sys.argv
building = list[1]
calls = list[2]
output = list[3]

"we will read building.json file and will get the necessary input to our own variables"
with open(building) as myfile:
    data = myfile.read()

# parse file
obj = json.loads(data)

"now we have our building.json file int obj variable and gets from it minFloor maxFloor and elevators"
minFloor = obj['_minFloor']
maxFloor = obj['_maxFloor']

"elevators is array that contains all the elevators in the building"
"callsArr is an array that contains all the calls that we gets as input"
"arrfloose is an array that tells us where are the elevators at any given second .... hopefully"
elevators = []
callsArr = []



"init elevators"
for i in range(0, len(obj['_elevators'])):
    id = obj['_elevators'][i]['_id']
    speed = obj['_elevators'][i]['_speed']
    minFloor = obj['_elevators'][i]['_minFloor']
    maxFloor = obj['_elevators'][i]['_maxFloor']
    closeTime = obj['_elevators'][i]['_closeTime']
    openTime = obj['_elevators'][i]['_openTime']
    startTime = obj['_elevators'][i]['_startTime']
    stopTime = obj['_elevators'][i]['_stopTime']
    spf = 0
#     spf = float((obj['_elevators'][i]['_speed']*(obj['_elevators'][i]['_maxFloor']
# -obj['_elevators'][i]['_minFloor']))-obj['_elevators'][i]['_startTime']
# -obj['_elevators'][i]['_stopTime']-obj['_elevators'][i]['_openTime']
# -obj['_elevators'][i]['_closeTime'])/(obj['_elevators'][i]['_maxFloor']
# -obj['_elevators'][i]['_minFloor'])
#     " stf = ((speed*(maxFloor-minFloor))-startTime-stopTime-openTime-closeTime)/(maxFloor-minFloor)"
#
    mood = 2
    e = Elevator(id, speed, minFloor, maxFloor, closeTime, openTime, startTime, stopTime,spf,mood)
    elevators.append(e)

    spf = ((e.speed*(e.maxFloor-e.minFloor))-e.startTime-e.stopTime-e.openTime-e.closeTime)/(e.maxFloor-e.minFloor)
    for j in range(0, (e.maxFloor - e.minFloor)+1):
         e.arrfloose.append(spf*j)




"this function initializes the array in second from source floor to destination in up mode"
"so if the elevator took a given call we will know now the elevator floor/time in any given time/floor"
"it doesnt need to go all over evey elevator arr only the one who took the call"
def up(call, i):
    # for i in range(len(elevators)):
    if float(call.time) != elevators[i].arrfloose[int(call.source)-elevators[i].minFloor]:
        elevators[i].arrfloose[int(call.source)-elevators[i].minFloor] += elevators[i].stopTime + elevators[i].openTime + elevators[i].closeTime + elevators[i].startTime + (
                float(call.time) - elevators[i].arrfloose[int(call.source)-elevators[i].minFloor])
    else:
        elevators[i].arrfloose[int(call.source)-elevators[i].minFloor] += elevators[i].closeTime + elevators[i].openTime + elevators[i].stopTime + elevators[i].startTime
    for j in range(int(call.source), elevators[i].maxFloor):
        "the for need to by from call.source to maxfloore"
        elevators[i].arrfloose[(j-elevators[i].minFloor) + 1] = (elevators[i].arrfloose[j-elevators[i].minFloor]+elevators[i].spf)



"this function initializes the array in second from source floor to destination in down mode"
"so if the elevator took a given call we will know now the elevator floor/time in any given time/floor until the elevator will arrive to her destination"
"it doesnt need to go all over evey elevator arr only the one who took the call"
def dowm(call, i):
    # for i in range(len(elevators)):
    if float(call.time) != elevators[i].arrfloose[int(call.source)-elevators[i].minFloor]:
        elevators[i].arrfloose[int(call.source)-elevators[i].minFloor] += elevators[i].stopTime + elevators[i].openTime + elevators[i].closeTime + elevators[i].startTime + (
                float(call.time) - elevators[i].arrfloose[int(call.source)-elevators[i].minFloor])
    else:
        elevators[i].arrfloose[int(call.source)-elevators[i].minFloor] += elevators[i].closeTime + elevators[i].openTime + elevators[i].stopTime + elevators[i].startTime
        'i = i + any'
    for j in range(int(call.source), 0):
        elevators[i].arrfloose[(j-elevators[i].minFloor) - 1] = (elevators[i].arrfloose[j-elevators[i].minFloor]+elevators[i].spf)
        "the for need to by from call.source to minfloore "
        "need to be i-- fixit"


def nearsource(call):
    mintime = float(call.time) - elevators[0].arrfloose[0]
    minindex = 0
    maxcallsQueue = 4
    if int(call.source) < int(call.destination):
        for i in range(len(elevators)):
            temp = float(call.time) - elevators[i].arrfloose[int(call.source)-elevators[i].minFloor]
            if temp >= 0:
                if temp <= mintime:
                    if len(elevators[i].callsQueue) < maxcallsQueue:
                        if elevators[i].mood == 1 or elevators[i].mood == 2:
                            minindex = i
        up(call, minindex)
        elevatormood(call,minindex)
        "to know the mood precisely we need the callsArr of amit and with this combination we will allocatedElevator precisely"
    else:
        for i in range(len(elevators)):
            temp = float(call.time) - float(elevators[i].arrfloose[int(call.source)-elevators[i].minFloor])
            if temp >= 0:
                if temp <= mintime:
                    if len(elevators[i].callsQueue) < maxcallsQueue:
                        if elevators[i].mood == 0 or elevators[i].mood == 2:
                            minindex = i
        dowm(call, minindex)
        elevatormood(call, minindex)

    call.allocatedElevator = minindex
    elevators[minindex].callsQueue.append(call)
    clear(call)
    elevatormood2(call, minindex)

"now we want to to say that elevator i took the call and to defin up mode or down mode to elevator until destination"


"we want to go over all elevators to see which one closer to call.source be given call.time and compering it to e[i].arrfloose[correnfloor]"
"we need also to check if the elevator is going to source direction (up or down) so we will know if its worth to this elevator to take the call"
"did not complete"
"i'm tired and can't think"


"this function returns what is the time of elevator in the i elevator and j floor"  "need to be fixed"
"we can also return the curent floor by given call.time"
# def curentFloor(e, i, j):
#     return e[i].arrfloose[j]

def elevatormood(call,i):
        if int(call.source) < int(call.destination):
            elevators[i].mood = 1
        else:
            elevators[i].mood = 0

def elevatormood2(call,i):
    if float(call.time) > elevators[i].arrfloose[(int(elevators[i].callsQueue[(len(elevators[i].callsQueue)-1)].destination))-elevators[i].minFloor]:
        elevators[i].mood == 2
"need to be completed"


def clear(call):
    for e in elevators:
        e.clearCompleteCalls(call)



"if elevator going up we want to initializes the e[i].arrfloose so we can know where the elevator in eny given time"
"i will copmlete tomorrow i dont know what im doing anymore"



"init calls"
with open(calls) as f:
    reader = csv.reader(f)
    for row in reader:
        call = Call(row[1], row[2], row[3], row[4])
        callsArr.append(call)

"row[4] represant allocated elevator"
"we will want to edit row[4] in our output file with the given call as input for allocatedElevator function"
for i in callsArr:
    nearsource(i)

inputData = []
for i in callsArr:
    tempArr = ["Elevator Call", i.time, i.source, i.destination, 3, i.allocatedElevator, " Done", " dt",
               " 164.5625272709607"]
    inputData.append(tempArr)

"write data in the new output.csv file"
with open(output, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(inputData)

subprocess.Popen(["powershell.exe",
                  "java -jar Ex1_checker_V1.2_obf.jar 1111,2222,3333 " + list[1] + " " + list[3] + " out.log"])
"GUI"
# root = Tk()
# C = Canvas(root, bg="yellow", height=600, width=400)
# C.create_rectangle(20, 20, 380, 470)
# numbersOfFloors = abs(minFloor - maxFloor)
# deltaFloor = 500 / numbersOfFloors
# deltaElevators = 360 / len(elevators)
# for i in range(0, numbersOfFloors):
#    C.create_line(20, 20 + deltaFloor * i, 380, 20 + deltaFloor * i)
# for i in range(0, len(elevators)):
#    C.create_line(20 + deltaElevators * i, 20, 20 + deltaElevators * i, 470)

# C.pack()
# mainloop()
