#!/bin/bash


SEARCHDIR="$1"
#LISTDIR="/home/media/Pictures/DVD/lists"
CATALOGDIR="/home/media/Pictures/DVD/catalog"

#if [ -z "$SEARCHDIR" ]; then
#   echo "usage: $0 <searchdir>"
#   exit 1
#fi

# Find pics
find $CATALOGDIR -maxdepth 2 -name DCIM | while read d; do
   for i in $(ls $d); do
      find $SEARCHDIR -maxdepth 3 | grep -q "$i" || echo "$i"
   done
done









