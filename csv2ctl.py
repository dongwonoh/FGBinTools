# Script to convert csv to FaceGen control file (.ctl)
#
# original code by Ron Dotsch (rdotsch@gmail.com) circa 2017
# made Python-3 compatible by DongWon Oh (dongwonohphd@gmail.com) 2023
#
# prerequisite: FaceGen Modeller SDK, FGBinTools

from FGBinTools import insertSlider
from LinAlgTools import normalize
from numpy import array
from io import open

source = open("/path/to/si-file.csv", 'r')

ctlfile = open('/path/to/si-file.ctl', 'w')

for line in source:
    line = line.strip().split(',')
    line = [i.strip('"') for i in line] 
    if line[0] == 'label':
        continue
    
    print(line)

    SS = normalize(array([float(i) for i in line[1:51]]))
    TS = normalize(array([float(i) for i in line[51:101]]))

    insertSlider(line[0], SS.tolist(), 'SS', ctlfile)
    insertSlider(line[0], TS.tolist(), 'TS', ctlfile)

source.close()

print("Done.")