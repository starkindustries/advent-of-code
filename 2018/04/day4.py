#!/usr/bin/python3.7
# day4

import sys
import datetime 
import copy

# Main Program
if __name__ == "__main__":
    filename = str(sys.argv[1])
    print("Filename: {}". format(filename))

fileObject  = open(filename, "r")
lines = fileObject.read().splitlines()

#print(lines)
data = []

for line in lines:
    array = line.split(" ")
    tempDate = array[0] + " " + array[1]
    tempDate = tempDate.replace("[", "")
    tempDate = tempDate.replace("]", "")    

    # https://docs.python.org/3/library/datetime.html#datetime.datetime.strptime
    # https://stackoverflow.com/questions/2380013/converting-date-time-in-yyyymmdd-hhmmss-format-to-python-datetime    
    tempDate = datetime.datetime.strptime(tempDate,'%Y-%m-%d %H:%M')

    if array[2] == 'Guard':
        guard = array[3]
        #print("{} {} {}".format(date, time, guard))
        data.append((tempDate, guard))
    elif array[2] == 'falls' or array[2] == 'wakes':
        status = array[2]
        #print("{} {} {}".format(date, time, status))
        data.append((tempDate, status))

data = sorted(data, key= lambda tuple: tuple[0])

# WARNING remove this:
# del data[28:]

for d in data:
    print(d)

# find guard who sleeps the most
guardTracker = []

minuteMap = [data[0][0].date(), data[0][1]] # first date and first guard
# print(minuteMap)
# exit()
lastTrackedMinute = 0

for i in range(1, len(data), 1):    
    # data format: (date, guard or wakes/falls)
    date = data[i][0]
    status = data[i][1]  
    # print("STATUS: {}".format(status))  

    if status[0] == "#": # it's a guard                            
        numMinutes = 60 - lastTrackedMinute
        minuteMap.extend(['.' for j in range(0,numMinutes,1)])
        guardTracker.append(minuteMap)
        minuteMap = [date.date(), status] # initialize new array
        lastTrackedMinute = 0
    else: # status is either 'wakes' or 'falls'
        statusMinute = date.time().minute
        numMinutes = statusMinute - lastTrackedMinute
        dotHash = "." if (status == "falls") else "#"            
        minuteMap.extend([dotHash for j in range(0,numMinutes,1)])
        lastTrackedMinute = statusMinute

def printGuardTracker(guardTrackerCopy): 
    print("DATE ID          000000000011111111112222222222333333333344444444445555555555")
    print("                 012345678901234567890123456789012345678901234567890123456789")
    for tracker in guardTrackerCopy:    
        space = [" " for i in range(0,5-len(tracker[1]),1)]
        tracker[1] = "".join(space) + tracker[1]
        dateGuard = str(tracker[0]) + " " + tracker[1]
        del tracker[:2]    
        line = dateGuard + " " + "".join(tracker)
        print(line)

# Make sure to pass a copy so that the list doesn't change
# printGuardTracker(copy.deepcopy(guardTracker))
# print(guardTracker)

# maxSleepTime = 0
# sleepyGuardID = ""
# for tracker in guardTracker:
#     count = tracker.count('#') - 1 # minus 1 for the guard's '#'
#     if count > maxSleepTime:
#         maxSleepTime = count
#         sleepyGuardID = tracker[1]
guardSleepMinutes = {}
for tracker in guardTracker:
    sleepCount = tracker.count('#') - 1 # minus 1 for the guard's '#'
    guardID = tracker[1]
    if guardID in guardSleepMinutes:
        guardSleepMinutes[guardID] += sleepCount
    else:
        guardSleepMinutes[guardID] = sleepCount

sleepyGuardID = max(guardSleepMinutes, key=guardSleepMinutes.get)

print(guardSleepMinutes)
print("Sleepy Guard ID: {}".format(sleepyGuardID))

# Filter out all other guards and get only the sleepy guard's rosters
sleepyGuardRoster = [tracker for tracker in guardTracker if tracker[1] == sleepyGuardID]

printGuardTracker(copy.deepcopy(sleepyGuardRoster))

mostSleepyMinutes = [0 for i in range(0, 60, 1)]
print(mostSleepyMinutes)
for night in sleepyGuardRoster:
    del night[:2]
    for i in range(0, len(night), 1):
        if night[i] == "#":
            mostSleepyMinutes[i] += 1

print(mostSleepyMinutes)
maxSleepTime = max(mostSleepyMinutes)
print("Guard ID: {}".format(sleepyGuardID))
print("Max sleep time: {}".format(maxSleepTime))
maxSleepMinute = mostSleepyMinutes.index(maxSleepTime)
print("Max sleep minute: {}".format(maxSleepMinute))

answer = int(sleepyGuardID[1:]) * maxSleepMinute
print("Part 1 Answer: {}".format(answer))

superSleepyGuardID = ""
mostSleepyMinuteFinal = -1
maxSleepyTimeFinal = 0
for key in guardSleepMinutes:    
    guardRoster = [tracker for tracker in guardTracker if tracker[1] == key]
    #print(guardRoster)
    mostSleepyMinutes = [0 for i in range(0, 60, 1)]
    #print(mostSleepyMinutes)    
    guardID = key    
    for night in guardRoster:  
        del night[:2]
        
        for i in range(0, len(night), 1):
            if night[i] == "#":
                mostSleepyMinutes[i] += 1
    sleepTime = max(mostSleepyMinutes)
    maxSleepMinute = mostSleepyMinutes.index(sleepTime)
    if sleepTime > maxSleepyTimeFinal:
        maxSleepyTimeFinal = sleepTime
        mostSleepyMinuteFinal = maxSleepMinute
        superSleepyGuardID = guardID

guardNum = int(superSleepyGuardID[1:])
answer =  guardNum * mostSleepyMinuteFinal
print("Part 2: #{} {}minutes, minute {}, answer: {}".format(guardNum, maxSleepyTimeFinal, mostSleepyMinuteFinal, answer))