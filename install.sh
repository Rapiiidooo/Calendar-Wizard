#!/bin/sh

USUALPATH="/usr/share/scribus/scripts/"
set -x

if cp $PWD/CalendarWizard2.py $USUALPATH
then
    if cp $PWD/croix.png $USUALPATH
    then
        if cp -R $PWD/format/ $USUALPATH
        then
            if cp -R $PWD/models/ $USUALPATH
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