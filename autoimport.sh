#!/bin/bash

# Pictures
jhead -autorot *.JPG
jhead -n"%Y-%m-%d/%Y-%m-%d_%H:%M" *.JPG

# Movies
YEAR=$(date +'%Y')
while read m d num; do
  month=$(printf '%02d' $m)
  dir="${YEAR}-${month}-${d}"
  file="P${m}${d}${num}.MOV"
  test -d "$dir" || mkdir $dir
  mv $file $dir/
done < <(ls *.MOV | sed -n 's@P\([0-9]\{1,2\}\)\([0-9]\{2\}\)\([0-9]\{4\}\)\.MOV@\1 \2 \3@p')
