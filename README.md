
### Synopsis

```sh
$ ./clean-all
$ redo report.json
$ open html/report.html
```

These scripts generate a report of Hackage packages whose documentation
status is "Docs pending" -- i.e. packages for which no attempts to
generate documentation have been made.

Intermediate build products created for this report include:

    index.tar.gz    - the current index.tar.gz from Hackage
    all-packages    - a list of all packages in the index.tar.gz archive
    docstats.db     - a sqlite3 database fof all the doc status for each package
    report.json     - JSON version of docstatus.db

### Dependencies

- redo
- python 2.7
- python packages: requests, json, sqlite3
- curl
- basic Haskell installation (runhaskell, core HP libraries)

