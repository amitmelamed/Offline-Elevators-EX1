import sys
import json
import csv
from random import randrange

from tkinter import *

"function that gets a call and returns allocated elevator"


def allocateElevator(call):
    minTime=call.calcTime(elevators[0])
    minIndex=0
    for i in range(len(elevators)):
        currentTime=call.calcTime(elevators[i])
        if(currentTime<minTime):
            minTime=currentTime
            minIndex=i
    call.allocatedElevator=minIndex
    elevators[minIndex].position=call.destination
    elevators[minIndex].callsQueue.append(call)
    for e in elevators:
        e.clearCompleteCalls(call)

"elevetor class:"
"each elevator has id,speed,minFloor, maxFloor, closeTime, openTime, startTime, stopTime"


class Elevator:
    def __init__(self, id, speed, minFloor, maxFloor, closeTime, openTime, startTime, stopTime):
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
        # self.arr = [maxFloor - minFloor]

    def toString(self):
        return "id:" + str(self.id) + " speed:" + str(self.speed) + " minFloor:" + str(
            self.minFloor) + " maxFloor:" + str(self.maxFloor) + " closeTime:" + str(
            self.closeTime) + " openTime:" + str(self.openTime) + " startTime:" + str(
            self.startTime) + " stopTime:" + str(self.stopTime) + "position: " + str(self.position)

    def clearCompleteCalls(self,call):
        count=0
        for i in self.callsQueue:
            if (float(i.time)<float(call.time)-25):
                count=count+1
        for i in range (count):
            self.callsQueue.pop(0)


"call class: each call has time, source, destination, allocatedElevator"


class Call:
    def __init__(self, time, source, destination, allocatedElevator):
        self.time = time
        self.source = source
        self.destination = destination
        self.allocatedElevator = allocatedElevator
        self.absFloor=abs(int(source)-int(destination))

    def toString(self):
        return ("time:" + str(self.time) + " source:" + str(self.source) + " destination:" + str(
            self.destination) + " allocatedElevator:" + str(self.allocatedElevator))
    def calcTime(self,elevator):
        calc=elevator.openTime+elevator.closeTime+speed*self.absFloor+abs(int(elevator.position)-int(call.source))
        calc=calc*len(elevator.callsQueue)
        return calc


"sys.argv is a function that gets the input from the terminal and puts its in an array"
"buildint will be the string that represent building.json location that we want to use for input"
"calls will be the string that represent calls.csv location that we want to use for input"
"output will be the string that represent outPut.csv location that we want to use for output"
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
    # for j in range(0, len(arr)):
    #     arr[j] += speed

    e = Elevator(id, speed, minFloor, maxFloor, closeTime, openTime, startTime, stopTime)
    elevators.append(e)


"init calls"
with open(calls) as f:
    reader = csv.reader(f)
    for row in reader:
        call = Call(row[1], row[2], row[3], row[4])
        callsArr.append(call)

"row[4] represant allocated elevator"
"we will want to edit row[4] in our output file with the given call as input for allocatedElevator function"
for i in callsArr:
    allocateElevator(i)

inputData = []
for i in callsArr:
    tempArr = ["Elevator Call", i.time, i.source, i.destination, 3, i.allocatedElevator, " Done", " dt",
               " 164.5625272709607"]
    inputData.append(tempArr)

"write data in the new output.csv file"
with open(output, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(inputData)

"GUI"
root = Tk()
C = Canvas(root, bg="yellow", height=600, width=400)
C.create_rectangle(20, 20, 380, 470)
numbersOfFloors = abs(minFloor - maxFloor)
deltaFloor = 500 / numbersOfFloors
deltaElevators = 360 / len(elevators)
for i in range(0, numbersOfFloors):
    C.create_line(20, 20 + deltaFloor * i, 380, 20 + deltaFloor * i)
for i in range(0, len(elevators)):
    C.create_line(20 + deltaElevators * i, 20, 20 + deltaElevators * i, 470)

C.pack()
mainloop()
