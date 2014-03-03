#!/bin/bash
. ~/.bash_profile

exiftool -Orientation=1 -r -n "$@"
