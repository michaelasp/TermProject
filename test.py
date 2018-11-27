import gpxpy
import os
print(os.getcwd())
gpx_file = open('gpx/nstar.gpx', 'r').read()
print(gpx_file)
gpx = gpxpy.parse(gpx_file)
tChange = 0
dx = (0,0)
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            #print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))
            
            print(dx[1])
            if dx[0] == 0:
                dx = (point.elevation,0)
            else:
                dx = (point.elevation, abs(dx[0]-point.elevation)+dx[1])
print(dx[1])

