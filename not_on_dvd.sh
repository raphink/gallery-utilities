#!/bin/bash


SEARCHDIR="$1"
#LISTDIR="/home/media/Pictures/DVD/lists"
CATALOGDIR="/home/media/Pictures/DVD/catalog"

#if [ -z "$SEARCHDIR" ]; then
#   echo "usage: $0 <searchdir>"
#   exit 1
#fi

for i in $(ls $SEARCHDIR); do
   #grep -q "$i" ${LISTDIR}/*.list || echo "$i"
   find $CATALOGDIR -maxdepth 3 ! -path "HD*" | grep -q "$i" || echo "$i"
done








