#!/usr/bin/env bash

# Any subsequent(*) commands which fail will cause the shell script to exit immediately
set -e

#VERSION=`git describe --tags --long`
VERSION=`git rev-list --count --all`
GITID=`git rev-parse --short HEAD`
BRANCH=`git rev-parse --abbrev-ref HEAD`

# in Jenkins, it will checkout the code based via sha256 directly, no specific branch
# we have to get the branch from global environment variable
if [ $BRANCH == 'HEAD' ]
then
    #
    # http://www.ing.iac.es/~docs/external/bash/abs-guide/string-manipulation.html
    # ${string#substring} :  Strips shortest match of $substring from front of $string.
    #
    # origin/dev_eric  => dev_eric
    #
    BRANCH=${GIT_BRANCH#*/}

    # if the branch is empty, we use "dev" as the default value
    BRANCH=${BRANCH:-"dev"}
fi

if [ $BRANCH == 'master' ]
then
    VERSION="${VERSION}-${GITID}"
else
    VERSION="${VERSION}-${BRANCH}-${GITID}"
fi

echo ${VERSION}
