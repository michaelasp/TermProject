def findSections(data):
    unitW = data.unitW
    unitH = data.unitH
    (_,_,gpxFile,_, min_lat, min_lon, max_lat, max_lon,_) = data.plot
    gpx = gpxpy.parse(gpxFile)
    i=0
    plotNext = False
    last = []
    section = []
    sections = []
    looping = False
    loopDist = 0
    tolerance = 0.001
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                posX = point.latitude - min_lat
                posY = point.longitude - min_lon
                #posX, posY = float("%.3f" % (2 * posX)), float("%.3f" % (2 * posY))
                if i != 0:
                    plotNext = True
                    #checks through all current points to see if a new one can be added or not
                    for (lastX, lastY) in last:
                        if abs(posX - lastX) < tolerance and abs(posY - lastY) < tolerance:
                            plotNext = False
                            curPoint = (lastX, lastY)
                            break
                if i == 0:
                    last.append((posX, posY))
                    section.append((posX, posY))
                elif plotNext == True:
                    last.append((posX, posY))
                    if looping == True:
                        loop = findFloats(section, section[-1])[0]
                        assert(section[loop] == section[-1])
                        loopDist = len(section) - loop
                        #in order not to have short loops
                        if len(section[-loopDist:-1]) > 10: 
                            sections.append(section[-loopDist:])
                            assert(section[-loopDist:][0] == section[-loopDist:][-1])
                            section = section[:-loopDist+1]
                            looping = False
                    section.append((posX, posY))
                    plotNext = False
                else:
                    (segEndX, segEndY) = section[-1]
                    if abs(posX - segEndX) < tolerance and abs(posY - segEndY) < tolerance:
                        pass
                    else:
                        looping = True
                        section.append(curPoint)
                i += 1
    sections.append(section)
    return sections

#https://stackoverflow.com/questions/24935938/how-to-find-a-float-number-in-a-list , modified to use tuples
def findFloats(listOfFloats, value):
    return [i for i, tup in enumerate(listOfFloats)
            if abs(tup[0]-value[0]) < 0.00001 and abs(tup[1]-value[1]) < 0.00001]