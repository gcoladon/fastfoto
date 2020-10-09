#!/usr/bin/env bash
#
# filename-to-exif-timestamp - extract a date like "2020-10-09" from a filename
#    and put that date into the exif metadata
#

SCRIPT_NAME=`basename $0`
USAGE="usage: $SCRIPT_NAME filename"

if [ $# -ne 1 ]; then echo $USAGE; exit 1; fi

filename=$1

if [[ ${filename} =~ ([[:digit:]]{4})-([[:digit:]]{2})-([[:digit:]]{2}) ]]
then
  yr=${BASH_REMATCH[1]}
  mo=${BASH_REMATCH[2]}
  day=${BASH_REMATCH[3]}
  datestring="${yr}:${mo}:${day} 12:00:00"
  exiftool -overwrite_original_in_place -datetimeoriginal="${datestring}" $filename >/dev/null 2>&1
  if [ $? -ne 0 ]; then echo "exiftool could not write date, exiting"; exit; fi
  echo "wrote $datestring into exif metadata of file $filename"
else
  echo "did not find a date YYYY-MM-DD in $filename"
fi
