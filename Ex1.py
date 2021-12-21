import subprocess
import sys
import json
import csv
from Elevator import Elevator
from Call import Call


# to run the algorithm
# python3 Ex1.py data/Ex1_input/Ex1_Buildings/B5.json data/Ex1_input/Ex1_Calls/Calls_a.csv output.csv
# to run the tester
# java -jar libs/Ex1_checker_V1.2_obf.jar 1111,2222,3333 data/Ex1_input/Ex1_Buildings/B5.json output.csv out.log

"function that gets a call and returns allocated elevator for 2 elevators buildings"
def allocateElevatorFor2Elevators(call):
    fastElevatorIndex = 0
    slowElevatorIndex = 1
    if (float(elevators[0].speed) > float(elevators[1].speed)):
        fastElevatorIndex = 1
        slowElevatorIndex = 0
    floorsCount = maxFloor - minFloor

    if (float(call.destination) < float(floorsCount) / 3):
        call.allocatedElevator = slowElevatorIndex
    else:
        call.allocatedElevator = fastElevatorIndex

"function that gets a call and returns allocated elevator for medium buildings"
def allocateElevatorMedium(call):
    minTime = call.calcTimeMedium(elevators[0])
    minIndex = 0
    for i in range(len(elevators)):
        currentTime = call.calcTimeMedium(elevators[i])
        if (currentTime < minTime):
            minTime = currentTime
            minIndex = i
    call.allocatedElevator = minIndex
    elevators[minIndex].position = call.destination
    elevators[minIndex].callsQueue.append(call)
    for e in elevators:
        e.clearCompleteCalls(call)

"function that gets a call and returns allocated elevator"
def allocateElevator(call):
    "we check if we have only 2 elevators we will use better algoritem for small buildings"
    if (len(elevators) == 2 and abs(maxFloor - minFloor) > 80):
        allocateElevatorFor2Elevators(call)
        return
    if(len(elevators)<6):
        allocateElevatorMedium(call)
        return
    minTime = call.calcTime(elevators[0])
    minIndex = 0
    for i in range(len(elevators)):
        currentTime = call.calcTime(elevators[i])
        if (currentTime < minTime):
            minTime = currentTime
            minIndex = i
    call.allocatedElevator = minIndex
    elevators[minIndex].position = call.destination
    elevators[minIndex].callsQueue.append(call)
    for e in elevators:
        e.clearCompleteCalls(call)

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
#if you want to run the simulator after running the program use this line:
subprocess.Popen(["powershell.exe","java -jar Ex1_checker_V1.2_obf.jar 316329069,207640806,209380922 " + list[1] + " " + list[3] + " out.log"])
