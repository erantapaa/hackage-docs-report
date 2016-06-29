
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

### redo

A quick summary of how `redo` works.

1. The command `redo target` does the following:

    - If `target` exists and nothing is known about its dependencies, `redo` assumes that the file is up-to-date and nothing is done.

    - If the dependencies of `target` are known (because `redo` has been called on it previously) or if `target` does not exist, the build script for `target` is executed. This is usually `target.do` but see the `redo` man page for the complete details.

2. As the build script for `target` is executed, calls to `redo` or `redo-ifchange` will set the dependencies for `target` in
addition to rebuilding `target`. Usually the dependencies for a build target are static, but this process allows the
dependencies to change over time. Thus the dependencies for a target are re-determined every time the target is rebuilt.

3. The equivalent to `make target` is `redo-ifchange target`. Running `redo target` will always execute the build script for `target` (modulo what was stated above in #1.)

The archetypal example is a build script for a .o file from a .c file:

    redo-ifchange $2.c                   # register $2.c as a dependency AND
                                         #   rebuild it if necessary
    gcc -MD -MF $2.d -c -o $3 $2.c       # build the target
    read DEPS <$2.d                      
    redo-ifchange ${DEPS#*:}             # register all used .h files as dependencies AND
                                         #   rebuild them if necessary

Note that the rebuild steps for the .h files are unlikely to happen in practice
if the .c and .h files are static files (i.e. not dynamically generated.)

Note that if a target's dependencies change, they do not take effect until the next
time an up-to-date check is made for the target.
