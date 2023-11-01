# FGBinTools
- Useful functions to create and manipulate FaceGen faces and face models.
- Automatizes some tedious aspects of face generating and manipulating.
- Run on command line.
- Developed by Ron Dotsch (rdotsch@gmail.com)
- Minor tweaks and additions by DongWon Oh (dongwonohphd@gmail.com)
- Prerequisite: FaceGen Modeller SDK

## FGBinTools.py
- Functions to read and write data from binary FaceGen files

## csv2ctl.py
- Script to convert csv to FaceGen control file (.ctl)

## ctl2csv.py
- Script to convert FaceGen control file (.ctl) to csv

## csv2fg.py
- Script to convert csv to FaceGen face file (.fg)

## fg2csv.py
- Script to convert FaceGen face files (.fg) to csv

## fg2jpg.sh
- Script to batch-generate jpg files from fg file

## build_model.r
- Script to build data-driven models based on rater responses
- The procedure follows the description in  Oosterhof & Todorov 2008 and Todorov & Oh 2022

## generate_identities.r
- Script to generate multiple identities that randomly varies on facial information
  
## si.ctl
- The original FaceGen control file with original dimensions/models

## si-todorov.ctl / si-todorov.csv
- FaceGEn control file with dimensions related to face-based social trait judgments per Oosterhof & Todorov 2008



### References
Oosterhof, N. N., & Todorov, A. (2008). The functional basis of face evaluation. Proceedings of the National Academy of Sciences, 105(32), 11087–11092. https://doi.org/10.1073/pnas.0805664105
Todorov, A., & Oh, D. (2021). The structure and perceptual basis of social judgments from faces. In B. Gawronski (Ed.), Advances in experimental social psychology (Vol. 63, pp. 189–245). Academic Press. https://doi.org/10.1016/bs.aesp.2020.11.004
