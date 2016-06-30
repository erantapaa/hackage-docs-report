#!/bin/sh

exec >&2
echo Downloading index.tar.gz
curl 'https://hackage.haskell.org/packages/index.tar.gz' > $3

