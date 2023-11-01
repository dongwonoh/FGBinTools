# FGBinTools

**FGBinTools** is a collection of functions and scripts designed to create, manipulate, and analyze FaceGen faces and face models. The repository provides tools to automate various tasks associated with FaceGen, making it easier for researchers and developers to work with FaceGen files.

## Features
- Automate tedious aspects of generating and manipulating faces.
- Conversion tools between csv and FaceGen-specific file formats.
- Scripts to build data-driven models based on rater responses.

## Contents

- `FGBinTools.py`: Functions to read and write data from binary FaceGen files.
- `csv2ctl.py`: Script to convert csv to FaceGen control file (.ctl).
- `ctl2csv.py`: Script to convert FaceGen control file (.ctl) to csv.
- `csv2fg.py`: Script to convert csv to FaceGen face file (.fg).
- `fg2csv.py`: Script to convert FaceGen face files (.fg) to csv.
- `fg2jpg.sh`: Script to batch-generate jpg files from fg file.
- `build_model.r`: Script to build data-driven models based on rater responses.
- `generate_identities.r`: Script to generate multiple identities based on facial information.
- `si.ctl`: The original FaceGen control file.
- `si-todorov.ctl` / `si-todorov.csv`: Control files related to face-based social trait judgments.

## Authors
- Developed by [Ron Dotsch](mailto:rdotsch@gmail.com)
- Tweaks and additions by [DongWon Oh](mailto:dongwonohphd@gmail.com)

## Prerequisites
- FaceGen Modeller SDK

## References
- [Oosterhof, N. N., & Todorov, A. (2008)](https://doi.org/10.1073/pnas.0805664105). The functional basis of face evaluation. _Proceedings of the National Academy of Sciences, 105_(32), 11087–11092.
- [Todorov, A., & Oh, D. (2021)](https://doi.org/10.1016/bs.aesp.2020.11.004). The structure and perceptual basis of social judgments from faces. In B. Gawronski (Ed.), _Advances in experimental social psychology_ (Vol. 63, pp. 189–245). Academic Press.

