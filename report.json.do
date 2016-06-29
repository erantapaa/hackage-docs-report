#!/bin/sh

exec >&2
redo-ifchange ./gen-report-json docstatus.db
./gen-report-json docstatus.db > $3
cp "$3" ./html/report.json

