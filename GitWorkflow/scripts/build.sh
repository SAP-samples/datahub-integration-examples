#!/bin/bash
#
#  CI Helper Script for SAP Data Intelligence Pipeline Solutions
#
#  About
#  -----
#
#  Performs the following build steps for SAP Data Intelligence
#  Pipeline solutions tracked in Git.
#
#  Following steps are performed:
#
#    (1) Package solution (zip) from files tracked in Git repository
#    (2) Install solution on a test tenant
#    (3) Execute a test graph (usually a workflow) and wait
#        until finished
#
#  The work folder should have the following structure:
#
#    <work-folder>/
#         /manifest.json  <- vsolution manifest file
#         /vflow/...      <- pipeline artifacts (graphs, operators)
#         /...            <- all other files ignored
#
#  Parametrization
#  ---------------
#
#  The script needs information to connect to a SAP Data Intelligence
#    test tenant. This information can be provided as parameters in
#    different ways:
#
#    - Directly in the utilized scripts (only recommended for testing)
#    - As environment variables 
#
#  When implementing the process on a build sever, consider to use
#    a 'secret store' provided by the build server for the username 
#    and password parameters to not expose the information to others.
#    E.g., the 'secret binding' of Jenkins can be used to provide 
#    these parameters as environment variables to the script and
#    hide them in the output of the log files.
#
# //////////////////////////////////////////////////////////////////

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Provide build stages as script arguments for local testing
STAGES=("bundle", "install", "test")
if [ "$1" != "" ]; then
  STAGES=( "$@" )
fi

if [[ "${STAGES[@]}" =~ "bundle" ]]; then
  $DIR/bundle-solution.sh || exit 1
fi

if [[ "${STAGES[@]}" =~ "install" ]]; then
  $DIR/install-solution.sh || exit 1
fi

if [[ "${STAGES[@]}" =~ "test" ]]; then
  $DIR/test-pipeline.sh || exit 1
fi
