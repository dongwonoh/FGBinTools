# Script to convert csv to FaceGen face file (.fg)
#
# original code by Ron Dotsch (rdotsch@gmail.com) circa 2017
# made Python-3 compatible by DongWon Oh (dongwonohphd@gmail.com) 2023
#
# prerequisite: FaceGen Modeller SDK, FGBinTools

from FGBinTools import writeFG

# First column is the name of the fg file, the 50 coulumns after are the symmetric shape values, 30 asymmetric shape values, and 50 symmetric texture values.

# Open the file
with open("/path/to/faces.csv", "r") as source:
    for line in source:
        line = line.strip().split(',')
        line = [i.strip('"') for i in line]
        if line[0] == 'filename':
            continue

        # for a file that sepecifies 130 parameters
        writeFG(line[0], SymShape = [int(i) for i in line[1:51]], ASymShape = [int(i) for i in line[51:81]], SymTexture = [int(i) for i in line[81:131]])
        # for a file that sepecifies 100 parameters
        #writeFG(line[0], SymShape = [int(i) for i in line[1:51]], SymTexture = [int(i) for i in line[51:101]])

print("Done.")

