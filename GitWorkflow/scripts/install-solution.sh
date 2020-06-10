#!/bin/bash

#DI_URL='https://your-data-hub-gateway.tld'
#DI_TEST_TENANT='default'
#DI_TEST_USER='admin'
#DI_TEST_PASSWORD='xxx'

echo "-------------------------"
echo "@@ Installing Solution @@"
echo "-------------------------"

# Prevent bash evaluation of single quoted arguments
# i.e., to prevent evaluation of $ characters in passwords
function CIRUN {
  arr=("$@")
  #echo "${arr[*]}"
  "${arr[@]}"
  return $?
}

if [ ! -f "manifest.json" ]; then
  echo "Error: Current path seems not to be a vsolution pipeline project (missing 'manifest.json' file)"
  exit 1
fi

# Extract solution name from manifest file.
DI_SOLUTION_NAME=$(python -c \
  "import json; o = json.load(open(\"manifest.json\")); print(o['name'])") \
  || exit 1
DI_SOLUTION_VERSION=$(python -c \
  "import json; o = json.load(open(\"manifest.json\")); print(o['version'])") \
  || exit 1
DI_SOLUTION="$DI_SOLUTION_NAME-$DI_SOLUTION_VERSION"
PACKAGE_NAME="$DI_SOLUTION.zip"

if [ ! -f "$PACKAGE_NAME" ]; then
  echo "Error: No solution bundle for solution '$DI_SOLUTION' exists. Please bundle the solution first!"
  exit 1
fi

echo "- Sys login..."
CIRUN vctl login $DI_URL $DI_TEST_TENANT $DI_TEST_USER -p $DI_TEST_PASSWORD || exit 1

STRATEGY=$(vctl tenant get-strategy $DI_TEST_TENANT | head -n 1 | xargs)
echo "- Tenant '$DI_TEST_TENANT' is using strategy '$STRATEGY'"
echo "- Stopping pipeline modeler..."
vctl scheduler stop pipeline-modeler
#vctl scheduler stop --all

EXISTING_SOLUTION=$(vctl strategy get $STRATEGY -o json | python -c "import json, sys; o = json.load(sys.stdin); print('\n'.join([s for s in o[u'layers']]))" | grep tsol)
if [ "$EXISTING_SOLUTION" != "" ]; then
  echo "- Removing existing solution (maybe old version) '$EXISTING_SOLUTION' from strategy '$STRATEGY'..."
  vctl strategy remove $STRATEGY $EXISTING_SOLUTION
fi

echo "- Removing solution '$DI_SOLUTION' from repository (if exists)..."
vctl solution get $DI_SOLUTION_NAME $DI_SOLUTION_VERSION && vctl solution delete $DI_SOLUTION_NAME $DI_SOLUTION_VERSION

echo "- Uploading solution '$DI_SOLUTION' to reposity..."
vctl solution upload $DI_SOLUTION.zip

echo "- Adding solution '$DI_SOLUTION' to strategy '$STRATEGY'..."
vctl strategy add $STRATEGY $DI_SOLUTION

