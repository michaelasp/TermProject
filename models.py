from findFolder import *
def retrieveFiles(data):
    (folders, files) = findGPX(data.path)
    totalPages = (len(files) + len(folders)) // data.pageLength
    start = data.currentPage * data.pageLength
    if start > len(files) - 1:
        fileStart = start - len(files)
        return folders[fileStart:fileStart+data.pageLength]
    else:
        if len(files) - start >= data.pageLength:
            return files[start:start+data.pageLength]
        else:
            end = len(files) - start
            return files[start:start+end] + folders[:(start+data.pageLength-end)]


