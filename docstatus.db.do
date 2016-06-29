#!/bin/sh

exec >&2
redo-ifchange all-packages ./scrape-doc-status
cat all-packages | parallel -j20 -m ./scrape-doc-status $3
touch report.timestamp
