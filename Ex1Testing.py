import unittest
from Elevator import Elevator
from Call import Call

elevators = []


class MyTestCase(unittest.TestCase):
    def test_something(self):


        e1 = Elevator(0, 2, 0, 10, 1, 1, 1, 1)
        e2 = Elevator(1, 1, 0, 10, 1, 1, 1, 1)
        c1 = Call("0",0,10,-1)
        elevators.append(e1)
        elevators.append(e2)
        allocateElevator(c1)
        self.assertEqual(e2.id, c1.allocatedElevator )

"function that gets a call and returns allocated elevator"
def allocateElevator(call):
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

if __name__ == '__main__':
    unittest.main()
