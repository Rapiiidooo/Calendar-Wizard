#!/bin/sh
#!/bin/bash

USUALPATH="/usr/share/scribus/scripts/"
USUALPATHIMG="/usr/share/scribus/scripts/img/"

if [ $# -lt 1 ]
then
    if cp ${PWD}/src/CalendarWizard2.py ${USUALPATH}
    then
        if [ ! -d "$USUALPATHIMG" ]; then
            mkdir ${USUALPATHIMG}
        fi
        if cp ${PWD}/src/img/croix.png ${USUALPATHIMG}
        then
            if cp -R ${PWD}/src/format/ ${USUALPATH}
            then
                if cp -R ${PWD}/src/models/ ${USUALPATH}
                then
                    echo "Success"
                    echo "Installation Done !"
                    echo "You can run Scribus and use CalendarWizard2 script."
                else
                    echo "Failure, exit status $?"
                fi
            fi
        fi
    fi
fi

if [ $# -ne 2 ]
then
    if [ "$1" = "remove" ]
    then
        if rm ${USUALPATH}CalendarWizard2.py
        then
            if rm -r ${USUALPATHIMG}croix.png
            then
                if [ -n "$(ls -A ${USUALPATHIMG})" ]
                then
                    if rm -R ${USUALPATH}format/
                    then
                        if rm -R ${USUALPATH}models/
                        then
                            echo "Success"
                            echo "Remove Done !"
                            echo "You now can not use CalendarWizard2 script anymore."
                        fi
                    fi
                else
                    if rm -r ${USUALPATHIMG}
                    then
                        if rm -R ${USUALPATH}format/
                        then
                            if rm -R ${USUALPATH}models/
                            then
                                echo "Success"
                                echo "Remove Done !"
                                echo "You now can not use CalendarWizard2 script anymore."
                            fi
                        fi
                    fi
                fi
            fi
        fi
    fi
else
    echo "Wrong usage : sudo $0 or sudo $0 remove"
fi