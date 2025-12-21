#!/bin/sh -x
node "$(dirname -- "$(readlink -- "$0")")"/ping.js
# Try not to break peoples' integrations.  Unless they're on windows.
echo "horn ok please"
