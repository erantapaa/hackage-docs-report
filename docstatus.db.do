#!/bin/sh

exec >&2
redo-ifchange all-packages ./scrape-doc-status
echo Building docstatus.db
cat all-packages | time parallel -j20 -m ./scrape-doc-status $3
touch report.timestamp
