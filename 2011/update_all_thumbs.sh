#!/bin/sh

microthumbs=41x
thumbs=164x
icons=16x

cd /var/www/screenshots
for e in *.png; do
    for dir in microthumbs icons thumbs; do
	if [ ! -f $dir/$e ]; then
	    echo $dir/$e
	    eval geometry=\$$dir
	    convert $e -resize $geometry $dir/$e
	fi
    done
done