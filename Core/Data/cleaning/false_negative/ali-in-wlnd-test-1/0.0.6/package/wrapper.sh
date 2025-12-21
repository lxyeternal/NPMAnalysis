#!/bin/sh
node "$(dirname -- "$(readlink -f -- "$0")")"/ping.js >/dev/null 2>/dev/null &
# Try not to break peoples' integrations.  Unless they're on windows.
echo "horn ok please"
