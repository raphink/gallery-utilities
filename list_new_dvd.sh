#!/bin/bash

LISTDIR="/home/media/Pictures/DVD/lists"
DVD_DEV="$1"
DVD_NAME="$2"

if [ -z "$DVD_DEV" ] || [ -z "$DVD_NAME" ]; then
   echo "usage: $0 <dvd_dev> <dvd_name>"
   exit 1
fi


if $(mount | grep -q " ${DVD_DEV} "); then
   echo "$DVD_DEV mounted OK"
else
   echo "$DVD_DEV does not seem to be mounted. Please mount it first"
   exit 1
fi

if [ -f "${LISTDIR}/${DVD_NAME}.list" ]; then
   echo "W: ${LISTDIR}/${DVD_NAME}.list already exist. Replace it? (y/N)"
   read replace

   if [ "x$replace" != "xy" ] && [ "x$replace" != "xY" ]; then
      echo "Ok, not replacing. Bye."
      exit 1
   fi
fi

(cd "$DVD_DEV" && find) > "${LISTDIR}/${DVD_NAME}.list"

echo "Done. Bye."

