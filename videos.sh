#!/bin/bash
declare -a arr=("bkg" "sig")


for type in "${arr[@]}";
do
    for ((i=1; i<=27; i++)); do
        ffmpeg -y -loop 1 -i images/$type/$type"_"$i.png -i output/$type/$type"_"$i.wav -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest videos/$type/$type"_"$i.mp4
    done
done