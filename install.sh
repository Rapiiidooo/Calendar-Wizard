#!/bin/sh

USUALPATH="/usr/share/scribus/scripts/"
USUALPATHIMG="/usr/share/scribus/scripts/img"
set -x

mkdir USUALPATHIMG

if cp $PWD/src/CalendarWizard2.py $USUALPATH
then
    if cp $PWD/src/img/croix.png $USUALPATHIMG
    then
        if cp -R $PWD/src/format/ $USUALPATH
        then
            if cp -R $PWD/src/models/ $USUALPATH
            then
                echo "Success"
            else
                echo "Failure, exit status $?"
            fi
        fi
    fi
fi

echo "Installation Done !"
echo "You can run Scribus and use CalendarWizard2 script."