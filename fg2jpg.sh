#!/bin/bash

# Batch-generates jpg files from fg file
#
# created on 20 july 2023
# last update: 20 july 2023
# DongWon Oh (dongwonohphd@gmail.com) (National University of Singapore)
#
# Usage:
#  fg2jpg.sh [source path] [target path]
#
# [source path]: path in which fg files are stored
# [target path]: path in which jpg files will be saved
#
# Prerequisit: FaceGen Main SDK CLI 3 (fg3), FaceGen Base Library CLI 3 (fgbl)
# Place this file (fg2jpg.sh) under the sdk bin folder with other FaceGEn functions (fg3, fgbl)

# Defines emergency exit function
die() { echo >&2 "$0 ERROR: $@";exit 1;}

# Exit unless argument submitted
[ "$1" ] || die "Argument missing. Please specify the path to a directory with FG files."

# Exit if argument is not dir
[ -d "$1" ] || die "Arg '$1' is not a directory. Please specify the path to a directory with FG files."   

# Exit unless access dir.
cd "$1" || die "Can't access '$1'."

# All files names in array $files
files=(*)                                           
# Exit if no files found
[ -f "$files" ] || die "No files found in the directory. Please specify the path to a directory with FG files."

for fgfile in "$1"/*.fg ;do
	echo "source path: $1"
	echo "target path: $2"
	
	file=$(echo $fgfile| cut -d'.' -f 1)

	./fg3 apply ssm ~/sdk/data/csam/Animate/Head/HeadHires ${fgfile} tempHead.tri
	./fg3 apply scm ~/sdk/data/csam/Animate/Head/HeadHires ${fgfile} tempHead.jpg
	./fgbl morph anim RestingExpression tempHead.tri "Expression SmileOpen" 0
	./fgbl render setup tempRender.txt tempHeadRestingExpression.tri tempHead.jpg 
	./fgbl render run tempRender.txt ${file}.jpg
	echo Done - $fgfile
done;

# remove temporary mesh and parameter files
rm temp*.tri
rm temp*.jpg
rm temp*.txt
rm ${file}-*
echo All done.

