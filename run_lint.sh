#! /bin/bash
# Copyright 2019 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

# Find Python files in subdirectory $1, optionally since date $2
find_python_packages() {
    topdir=$1
    since=$2

    (
    if [ "$since" != "" ]; then
        git ls-files -mo "$topdir/*.py" -x build
        git diff --name-only $since "$topdir/*.py"
    else
        find $topdir -name \*.py
    fi
    ) \
        | sort --unique \
        | git check-ignore --stdin --non-matching --verbose \
        | grep ^:: \
        | sed -e 's/^::\s//' \
        | grep -v /setup.*py$ \
        | grep -v _pb2\.py$
}

# Run lint on subdirectory $1, optionally since date $2.
# Run pycodestyle on Python source if $3 is non-zero.
# Run pylint3 if $4 is non-zero.
lint_module() {
    subdir=$1
    since=$2
    enable_pycodestyle_py=$3
    enable_pylint=$4

    top_dir=$(cd $(dirname $(dirname $0)) && pwd)

    cd $top_dir

    pylintrc=$top_dir/.pylintrc

    error=0

    python_packages=$(find_python_packages "$subdir" "$since")

    if [ "$python_packages" != "" -o "$cpp_packages" != "" ]; then
        [ $VERBOSE = 0 ] && echo "-- $subdir"

        # Check Python with pycodestyle
        if [ "$enable_pycodestyle_py" != 0 -a "$python_packages" != "" ] ; then
            [ $VERBOSE = 0 ] && echo "---- pycodestyle in $subdir"
            [ $VERBOSE = 1 ] && (
                echo "--------------------------------------------------------"
                echo "---- Running pycodestyle Python in $subdir..."
            )

            pycodestyle --config=$top_dir/.pycodestyle $python_packages \
                || error=1

        else
            [ $VERBOSE = 1 ] && (
                echo "--------------------------------------------------------"
                echo "---- Skipping pycodestyle Python in $subdir. " \
                     "(Nothing to do.)"
            )
        fi

        # Check Python with pylint3
        if [ "$enable_pylint" != 0 -a "$python_packages" != "" ] ; then
            [ $VERBOSE = 0 ] && echo "---- pylint in $subdir"
            [ $VERBOSE = 1 ] && (
                echo "--------------------------------------------------------"
                echo "---- Running pylint3 $pylintrc in $subdir..."
            )
            pylint3 \
                --rcfile=$pylintrc \
                --reports=no \
                --score=no \
                --persistent=no \
                $python_packages || error=1

        else
            [ $VERBOSE = 1 ] && (
                echo "--------------------------------------------------------"
                echo "---- Skipping pylint $pylintrc in $subdir. " \
                     "(Nothing to do.)"
            )
        fi

        # Check for unwanted MS-DOS CR/LF-style line endings
        [ $VERBOSE = 1 ] && (
            echo "--------------------------------------------------------"
            echo "---- Checking for CRLF in $subdir..."
        )

        if [ "$python_packages" != "" -a "$cpp_packages" != "" ] ; then
            file $python_packages $cpp_packages | grep CRLF && error=1
        fi

    else
        [ $VERBOSE = 1 ] && (
            echo "--------------------------------------------------------"
            echo "---- Skipping pycodestyle and pylint $pylintrc in $subdir. " \
                 "(Nothing to do.)"
        )
    fi

    return $error
}
# Exhaustive list of modules configured for linting
ALL_MODULES="core"
#
# Parse command line parameters
#
DRY_RUN=0
VERBOSE=0
SINCE=""
while getopts :s:nhv opt
do
    case $opt in
      h)
        usage
        exit 0
        ;;
      n)
        DRY_RUN=1
        ;;
      s)
        SINCE=$OPTARG
        ;;
      v)
        if [ "$VERBOSE" = "1" ]; then
            set -x
        fi
        VERBOSE=1
        ;;
      \?)
        echo "Invalid option: -$OPTARG" >&2
        usage
        exit 2
        ;;
    esac
done

# Default to lint all modules if no module is specified
if [ -z "$@" ]; then
    echo "No target MODULE(s) specified to lint."
    echo "For usage information, type: run_lint -h."
    echo ""
    echo "Lint will run on all modules (default)."
    echo ""
    MODULES=$ALL_MODULES
else
    MODULES=$@
fi

if [ "$DRY_RUN" = "1" ]; then
    for dir in $MODULES
    do
        for package in $(find_packages "$dir" "$SINCE")
        do
            echo $package
        done
    done
    exit 0
fi

top_dir=$(cd $(dirname $(dirname $0)) && pwd)
rv=0

# Print version information
echo "$(pylint3 --version | head -1)"
echo "pycodestyle $(pycodestyle --version)"

# Run pycodestyle or pylint or both for each module.

# Language:                                Python  | C
# Checks:                           pycodestyle    | pycodestyle
#                                           pylint | cppcheck

for MODULE in $MODULES
do
    case $MODULE in
        core)
                lint_module core                    "$SINCE" 1  0  || rv=1
                ;;
        *)
                echo "Module not configured for lint : $MODULE"
                rv=1
                ;;
    esac
done
if [ $rv -eq 0 ]; then
    echo ""
    echo "SUCCESS"
    exit 0
else
    exit $rv
fi

