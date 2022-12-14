#!/bin/bash

# https://www.lifewire.com/pass-arguments-to-bash-script-2200571
# Arguments are accessed inside a script using the variables $1, $2, $3, etc

# https://www.tldp.org/LDP/abs/html/comparison-ops.html
# Conditional If Else statements
if [ -z $1 ]
then
    # If no arguments are given then normal input is ran    
    # echo "String is null."
    python3 day5.py input.txt
else
    # If any argument is given then test input (input2.txt) is ran 
    # echo "String is NOT null."
    python3 day5.py input2.txt
fi