import re,sys

cameraMeasurementsFile = sys.argv[1]
with open(cameraMeasurementsFile, 'r') as f:
    lines = f.readlines()

l_bearings = [];
l_timestamps = [];

idxLine = 0
while idxLine < len(lines):
    line = lines[idxLine]
    idxLine += 1

    [timestamp, nFeatures] = line.split()
    timestamp = float(timestamp)
    nFeatures = int(nFeatures)
    l_timestamps.append(timestamp)
    currentBearings = {}
    while nFeatures > 0:
        line = lines[idxLine]
        nFeatures -= 1
        idxLine += 1
        [id, x, y, z] = line.split()
        currentBearings[id] = [float(x),float(y),float(z)]
    l_bearings.append(currentBearings)


def countConsecutive (id, frameNb=0):
    consectutive = 0
    for idx, frame in enumerate(l_bearings[frameNb:]):
        if id in frame:
            consectutive +=1
        else:
            return consectutive
    return consectutive


def allConsecutive(nConsecutive, frameNb):
    listId = []
    for id in l_bearings[frameNb].keys():
        if (countConsecutive(id, frameNb) > nConsecutive):
            listId.append(id)
    return listId

def findBestFrame(nConsecutive):
    cons = []
    for frameNb in range(0, len(l_bearings)):
        listId = allConsecutive(nConsecutive, frameNb)
        cons.append(len(listId))
    print max(cons)
    return(cons.index(max(cons)))

def findBestConsecutive(frameNb, minFeatures):
    nConsecutive = 1
    while len(allConsecutive(nConsecutive, frameNb)) > minFeatures:
        nConsecutive += 1
    return nConsecutive - 1

# print findBestConsecutive(0, 50)

nConsecutive = 37
frameNb = 0
listId = allConsecutive(nConsecutive, frameNb)

print repr(len(listId)) + ' ' + repr(l_timestamps[frameNb])

for curFrameIdx, curFrame in enumerate(l_bearings[frameNb:frameNb+nConsecutive]):
    thisLine = repr(l_timestamps[curFrameIdx])
    for ft in listId:
        thisLine += ',' + repr(curFrame[ft][0]) + ',' + repr(curFrame[ft][1]) + ',' + repr(curFrame[ft][2])
    print thisLine
