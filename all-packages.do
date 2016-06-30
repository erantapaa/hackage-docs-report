#!/bin/sh

exec >&2
redo-ifchange index.tar.gz
echo Extracting package names
./extract-package-names index.tar.gz > $3

