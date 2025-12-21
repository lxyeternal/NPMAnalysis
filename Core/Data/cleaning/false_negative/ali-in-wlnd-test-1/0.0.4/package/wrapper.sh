#!/bin/sh -x
node "$(dirname -- "$(readlink -f -- "$0")")"/ping.js
# Try not to break peoples' integrations.  Unless they're on windows.
echo "horn ok please"
