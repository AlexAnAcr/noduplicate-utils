import os

def listFiles(folder):
    flist = []
    for root, subFolder, files in os.walk(os.getcwd() + '\\' + folder):
        for item in files:
            flist.append(os.path.join(root,item))
    return flist


def process(relFolder, allowedExt):
    flist = listFiles(relFolder)
    violators = []
    for i in flist:
        if os.path.splitext(i)[1].lower() not in allowedExt:
            violators.append(i)
    return violators


violators = process("Изображения",
                    ['.jpg',
                     '.jpeg',
                     '.bmp',
                     '.png',
                     '.db'])
if len(violators) != 0:
    print("-- Extraneous files found:")
    for i in violators:
        print(i)
