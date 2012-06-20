#!/bin/bash

set -e

# No trailing slash for rsync please
EXTERNAL="/media/external/DCIM"

if [ ! -d "${EXTERNAL}" ]; then
   echo "E: Could not find ${EXTERNAL} directory"
   exit 1
fi

PARTITION=$(df "$EXTERNAL" | sed -ne "s@^/[^ ]* .* \(/.*\)@\1@p")
RW=$(mount | sed -ne "s@.* ${PARTITION} .* (\(rw\|ro\),.*)@\1@p")

echo "$PARTITION is mounted $RW"

if [ "x${RW}" = "xro" ]; then
   # unlock filesystem for the sync
   mount -o remount,rw "$PARTITION"
fi

rsync -av /home/raphink/Pictures/ "$EXTERNAL"


# relock filesystem after sync
mount -o remount,ro "$PARTITION"

