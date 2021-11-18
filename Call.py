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

    def calcTime(self, elevator):
        calc = elevator.openTime * 15 + elevator.closeTime * 15 + elevator.startTime * 10 + elevator.stopTime * 10 + speed * self.absFloor + abs(
            int(elevator.position) - int(self.source))
        calc = calc * (len(elevator.callsQueue) +5)
        return calc

    def calcTimeMedium(self, elevator):
        calc = elevator.openTime*2  + elevator.closeTime*2 + elevator.startTime*10  + elevator.stopTime*10  + speed * self.absFloor + abs(
            int(elevator.position) - int(self.source))
        calc = calc * (len(elevator.callsQueue)+15)
        return calc