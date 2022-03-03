#!/bin/bash

# Parameters:
# - path to mp3 file
# - an integer (1 to 9999)
# - optional: `--nonfc` flag to not create an nfc csv file
#
# Example:
# ./storyland_encrypter.sh /path/to/file.mp3 17
# ./storyland_encrypter.sh /path/to/file.mp3 17 --nonfc
#
# Inspired by @filiatrag
# see https://www.insomnia.gr/forums/topic/757427-lidl-storyland-figures/page/21/#comment-59031689

if ! hash eyeD3 &> /dev/null
then
  echo "eyed3 needs to be installed (example: 'sudo apt install eyed3')"
  exit
fi

if [ -z "$3" ]
then
  nfc=1
else
  if [ $3 == '--nonfc' ]
  then
    nfc=0
  else
    nfc=1
  fi
fi  

file=$1
name=$(basename $file)
name="${name%.*}"
filenumber=$(printf "%04d\n" $2)

# Prepare NFC code to write in index file (not used in CSV from python script)
nfc_code="02200408${filenumber}"
nfc_code="${nfc_code}00"

# Prepare file and sidecar csv
cp $file L$filenumber.mp3
eyeD3 --to-v2.3 --encoding utf16 -t L$filenumber L$filenumber.mp3 &> /dev/null
../audiocube.py storyland encrypt L$filenumber.mp3
rm L$filenumber.mp3
if [ $nfc == 1 ]
then
  ../audiocube.py storyland create_nfc_file $filenumber
fi

# Create folder for encrypted files if it does not exist and move files
[ ! -d "../encrypted" ] && mkdir "../encrypted"
mv L$filenumber.* ../encrypted/

# Create an index file, to remember what is what
[ ! -f "../encrypted/index.txt" ] && echo "FILE  - NFC CODE       - ORIGINAL SONG" > ../encrypted/index.txt && echo "--------------------------------------" >> ../encrypted/index.txt
echo "L$filenumber - $nfc_code - $name" >> ../encrypted/index.txt
