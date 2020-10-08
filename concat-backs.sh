#!/usr/bin/env bash
#
# process photos coming off Epson FF-680W
#

numphotos=`ls -l *_a.jpg | wc -l`
echo "found $numphotos photos"

filename=`ls -1 *.jpg | head -1`
prefix=`echo $filename | cut -d'_' -f 1`

rm -f -r RAW/ DOUBLESIDED/ BACK/
mkdir RAW DOUBLESIDED BACK

for i in $(seq -f "%04g" 1 $numphotos)
do
  #rename files
  raw="${prefix}_${i}.jpg"
  front="${prefix}_${i}_a.jpg"
  back="${prefix}_${i}_b.jpg"
  mv ${raw} RAW/${prefix}-${i}-raw.jpg
  mv ${front} ${prefix}-${i}-front.jpg
  mv ${back} ${prefix}-${i}-back.jpg

  echo -n "reducing resolution of back of photo ${prefix}-${i}-back.jpg ..."
  convert ${prefix}-${i}-back.jpg  -quality 75  ${prefix}-${i}-back-smaller.jpg
  echo " "

  echo -n "creating ${prefix}${i}-doublesided.jpg ..."
  convert ${prefix}-${i}-front.jpg  ${prefix}-${i}-back-smaller.jpg  -append  DOUBLESIDED/${prefix}-${i}-doublesided.jpg
  echo " "

  mv ${prefix}-${i}-front.jpg ${prefix}-${i}.jpg
done

echo "cleaning up..."
mv *-back.jpg BACK
rm *-back-smaller.jpg
