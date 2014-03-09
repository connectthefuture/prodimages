#!/bin/bash
. ~/.bash_profile

exiftool -Orientation -r -n "$@"
