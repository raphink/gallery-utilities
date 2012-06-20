#!/bin/sh

for i in *; do 
   if [ -f "thumb/$i" ]; then
      echo "thumb/$i exists, not converting"
   else
      echo "Converting thumb/$i"
      convert -size 400x400 $i -thumbnail '400x400>' -bordercolor black -border 200 -gravity center -crop 400x400+0+0 +repage thumb/$i
   fi
done
