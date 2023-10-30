# Script to convert FaceGen control file (.ctl) to csv
#
# original code by Ron Dotsch (rdotsch@gmail.com) circa 2017
# made Python-3 compatible by DongWon Oh (dongwonohphd@gmail.com) 2023
#
# prerequisite: FaceGen Modeller SDK, FGBinTools

import FGBinTools
import csv

settings = {
	# FaceGen control file to convert
	'ctl' : '/path/to/ctl/si-todorov.ctl',

	# Controls to convert
    'controls' : ['Attractiveness (300 faces)','Competence (300 faces)','Dominance (300 faces)','Extroverted (300 faces)','Frightening (300 faces)','Likeable (300 faces)','Mean (300 faces)','Threatening (300 faces)','Trustworthiness (300 faces)','PC1 (300 faces)','PC2 (300 faces)'],

	# Target csv file
	'csv' : 'si-todorov.csv',
}

print "Loading control vectors from %s..." % settings['ctl']

# Load ctl file
ctl = FGBinTools.readCtl(settings['ctl'])

controlshapevec = {}
controltexvec = {}

# Shape first (called geometry in .ctl terms)   
for label, vector in FGBinTools.readCtl(settings['ctl'])['GS'] :
    if label in settings['controls'] :
        print "+ Found: shape %s" % label
        controlshapevec[label] = vector      

# Then for texture
for label, vector in FGBinTools.readCtl(settings['ctl'])['TS'] :
    if label in settings['controls'] :
        print "+ Found: texture %s" % label
        controltexvec[label] = vector    

# Write csv
csvfile = file(settings['csv'], 'w')
csvWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

for label in sorted(controltexvec.keys()) :
	row = [label] + controlshapevec[label] + controltexvec[label]
	csvWriter.writerow(row)

csvfile.close()

print "Done."