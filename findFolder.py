import os
def findGPX(path):
    folders = []
    files = []
    for filename in os.listdir(path):
        if "gpx" in filename:
            if os.path.isdir(filename):
                folders.append(filename)
            else:
                files.append(filename)
    return (folders, files)

