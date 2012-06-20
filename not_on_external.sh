#!/bin/bash
# Searches for pics on DVD 
#   that are not on the external drive

EXTERNAL="/media/external/DCIM"
LISTDIR="/home/media/Pictures/DVD/lists"

OPT="$1"

if [ "x${OPT}" = "x-h" ]; then
   echo "usage: $0 [dvd|dvd_only]"
   echo "  The "dvd" option reports on DVDs after the full list"
   echo "  The "dvd_only" option stops analyzing a dvd if one file is found missing"
   exit 0
fi

# Dump all files on external
TMPFILE=$(mktemp "/tmp/not_on_external.XXXXXX")
TMPDVD=$(mktemp "/tmp/not_on_external.XXXXXX")
trap "rm -f $TMPFILE $TMPDVD" EXIT TERM QUIT
find "$EXTERNAL" > "$TMPFILE"

for i in ${LISTDIR}/*.list; do
   DVD=$(echo "$i" | sed -e "s@.*/\([^/]*\)\.list@\1@")
   echo -n "Analyzing DVD $DVD... "
   for j in $(cat "$i" | grep -v "^\./*\(\|Pictures\|Videos\|AVCHD\|DCIM\)$"); do
      # keep only the last 2 levels
      echo -n "$DVD: this is real file $j..."
      file=$(echo "$j" | sed -e "s@.*/\([^/]*/[^/]*\)@\1@")
      echo "searched as $file"
      if ! $(grep -q "$file" "$TMPFILE"); then
            echo "$DVD" >> "$TMPDVD"
            echo "found $file"

            if [ "x${OPT}" = "xdvd_only" ]; then
               break
            fi
      fi
   done
   echo "done"
done

if [ "x${OPT}" = "xdvd" ] || [ "x${OPT}" = "xdvd_only" ]; then
   echo
   echo "=================="
   echo "==  DVD REPORT  =="
   echo "=================="
   echo
   cat "$TMPDVD" | uniq
fi


