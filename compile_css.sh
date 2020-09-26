#!/bin/bash

if ! command -v sass &> /dev/null
then
    sudo npm install -g sass
fi
sass --watch static/stylesheet/src/:static/stylesheet/dist/
