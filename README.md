# FGBinTools

**FGBinTools** is a collection of functions and scripts designed to create, manipulate, and analyze FaceGen faces and face models. The repository provides tools to automate various tasks associated with FaceGen, making it easier for researchers and developers to work with FaceGen files.

## Latest Updates

**23 Sept 2024**:
- Enhanced `csv2ctl.py`, `ctl2csv.py`, and `fg2csv.py` to support:
  - Command-line arguments for input and output paths
  - Batch processing of multiple files
  - Optional specification of controls to convert (for csv2ctl and ctl2csv)

**9 Sept 2024**:
- Functions for batch conversions now available (`fg2dae.py`, `jpg2fg.py`).

## Features
- Automate tedious aspects of generating and manipulating faces.
- Conversion tools between csv and FaceGen-specific file formats.
- Scripts to build data-driven models based on rater responses or other types of corresponding values.
- Batch conversion capabilities for various file formats.
- Command-line support for easier integration and automation.

## Contents

### Core Functions
- `FGBinTools.py`: Functions to read and write data from binary FaceGen files.

### Conversion Scripts
- `csv2ctl.py`: Convert csv to FaceGen control file (.ctl). Now supports batch processing and command-line arguments.
- `ctl2csv.py`: Convert FaceGen control file (.ctl) to csv. Now supports batch processing and command-line arguments.
- `csv2fg.py`: Convert csv to FaceGen face file (.fg).
- `fg2csv.py`: Convert FaceGen face files (.fg) to csv. Now supports batch processing and command-line arguments.
- `fg2jpg.sh`: Batch-generate jpg files from fg files.
- `fg2dae.py`: Batch-convert fg files to dae files.
- `jpg2fg.py`: Batch-convert jpg files to fg files.

### Model Generation and Manipulation
- `build_model.r`: Build data-driven models based on rater responses or other types of corresponding values.
- `vary_on_model.r`: Vary faces on a model dimension.
- `generate_identities.r`: Generate multiple identities based on facial information.

### Control Files
- `si.ctl`: The original FaceGen control file.
- `si-todorov.ctl` / `si-todorov.csv`: Control files related to face-based social trait judgments.

## Authors
- Updated and maintained by [DongWon Oh](mailto:dongwonohphd@gmail.com) and [Angela Mao](mailto:maoanqiangela@gmail.com)
- Originally developed by [Ron Dotsch](mailto:rdotsch@gmail.com)

## Prerequisites
- FaceGen Modeller SDK

## References
- [Oosterhof, N. N., & Todorov, A. (2008)](https://doi.org/10.1073/pnas.0805664105). The functional basis of face evaluation. _Proceedings of the National Academy of Sciences, 105_(32), 11087–11092.
- [Todorov, A., & Oh, D. (2021)](https://doi.org/10.1016/bs.aesp.2020.11.004). The structure and perceptual basis of social judgments from faces. In B. Gawronski (Ed.), _Advances in experimental social psychology_ (Vol. 63, pp. 189–245). Academic Press.
