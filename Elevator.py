INTERVAL = 30


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

    def toString(self):
        return "id:" + str(self.id) + " speed:" + str(self.speed) + " minFloor:" + str(
            self.minFloor) + " maxFloor:" + str(self.maxFloor) + " closeTime:" + str(
            self.closeTime) + " openTime:" + str(self.openTime) + " startTime:" + str(
            self.startTime) + " stopTime:" + str(self.stopTime) + "position: " + str(self.position)

    def clearCompleteCalls(self, call):
        count = 0
        for i in self.callsQueue:
            if (float(i.time) < float(call.time) - INTERVAL):
                count += 1
        for i in range(count):
            self.callsQueue.pop(0)