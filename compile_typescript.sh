#!/bin/bash

if ! command -v tsc &> /dev/null
then
    sudo npm install -g typescript
fi

PROJECTROOTDIRECTORY=$(pwd)
SRCDIRECTORY='static/js/src'
COMPONENTDIRECTORY="${SRCDIRECTORY}/components"
LIBSDIRECTORY="${SRCDIRECTORY}/libs"
PAGESDIRECTORY="${SRCDIRECTORY}/pages"

echo "building scripts in ${COMPONENTDIRECTORY}"
cd "${COMPONENTDIRECTORY}"
tsc

cd "${PROJECTROOTDIRECTORY}"
echo "building scripts in ${LIBSDIRECTORY}"
cd "${LIBSDIRECTORY}"
tsc

cd "${PROJECTROOTDIRECTORY}"
echo "building scripts in ${PAGESDIRECTORY}"
cd "${PAGESDIRECTORY}"
tsc
