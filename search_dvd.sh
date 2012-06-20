#!/bin/bash

KEYWORD="$1"
LISTDIR="/home/media/Pictures/DVD/lists"

if [ -z "$KEYWORD" ]; then
   echo "usage: $0 <keyword>"
   echo " You can use grep regexps"
   exit 1
fi

grep "$KEYWORD" ${LISTDIR}/*.list | sed -e "s@^${LISTDIR}/\(.*\)\.list:\./\(.*\)@\1 \2@" | \
       while read dvd file; do
          echo "File $file is on DVD $dvd"
       done

