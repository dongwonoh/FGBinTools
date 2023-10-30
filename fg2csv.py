# Script to convert FaceGen face files (.fg) to csv
#
# original code by Ron Dotsch (rdotsch@gmail.com) circa 2017
# made Python-3 compatible by DongWon Oh (dongwonohphd@gmail.com) 2023
#
# prerequisite: FaceGen Modeller SDK, FGBinTools

import FGBinTools
import csv
import os

settings = {
    # FaceGen fg file path containing files to convert
    'fg' : '/path/to/face.fg',
        
    # Target csv file
    'csv' : '/path/to/face.csv',
}

with open(settings['csv'], 'w') as csvfile:
    csvWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    f = settings['fg']
    if '.fg' in f :
        fgdata = FGBinTools.readFG(f)
        row = [f[:-3], f[12:-3], f[6:11]] + fgdata['SS'] + fgdata['TS']
        csvWriter.writerow(row)


print("Done.")
