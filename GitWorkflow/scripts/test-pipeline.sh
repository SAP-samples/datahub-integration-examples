#!/bin/bash

#DI_TEST_URL=
#DI_TEST_USER=
#DI_TEST_PASSWORD=

#DI_TEST_GRAPH=

DI_TEST_NUM_TRIES=20
DI_TEST_WAIT_SECS=2

echo "----------------------"
echo "@@ Testing Solution @@"
echo "----------------------"

if [[ "$DI_TEST_GRAPH" == "" ]]; then
  echo "- No test graph defined"
  exit 1
fi

# --------------------------------------------------------
# Start graph using the Data Pipelines API. Data Pipelines
# Modeler will be started in case not running.
# --------------------------------------------------------

echo "- Starting Pipeline Modeler..."
graphs=$(curl -s -H "x-requested-with: fetch" -u "$DI_TEST_TENANT\\$DI_TEST_USER:$DI_TEST_PASSWORD" "$DI_URL/app/pipeline-modeler/service/v1/repository/graphs") 

echo "- Checking that test graph exists..."
echo $graphs | python -c "import json, sys; o = json.load(sys.stdin); print('\n'.join([g['name'] for g in o]))" | grep $DI_TEST_GRAPH || { >&2 echo "Error: Test graph '$DI_TEST_GRAPH' not found!"; exit 1; }

echo "- Start test graph '$DI_TEST_GRAPH' ..."
graph_response=$(curl -s -X POST -H "x-requested-with: fetch" -u "$DI_TEST_TENANT\\$DI_TEST_USER:$DI_TEST_PASSWORD" $DI_URL/app/pipeline-modeler/service/v1/runtime/graphs -d '{"src": "'"$DI_TEST_GRAPH"'", "name": "'"[Test] $DI_TEST_GRAPH"'"}')
echo $graph_response

echo "- Check if graphs is running..."
graph_id=$(echo $graph_response | python -c "import json, sys; o = json.load(sys.stdin); print(o['handle'])") || { >&2 echo "Error: Graph '$DI_TEST_GRAPH' could not be started!"; exit 1; }

echo "  - Graph handle: '$graph_id'"

# --------------------------------------------------------
# Fetch graph state until dead or completed.
# make sure to output the error in case execution failed
# --------------------------------------------------------

count=0
request=''
end_state=0

while [ $count -lt $DI_TEST_NUM_TRIES ]; do
  count=`expr $count + 1`

  echo "  - Checking graph status (try $count/$DI_TEST_NUM_TRIES)..."
  request=$(curl -s -H "x-requested-with: fetch" -u "$DI_TEST_TENANT\\$DI_TEST_USER:$DI_TEST_PASSWORD" "$DI_URL/app/pipeline-modeler/service/v1/runtime/graphs/$graph_id")
  state=$(echo $request | python -c "import json, sys; o = json.load(sys.stdin); print(o['status'])")
  echo "    $state"

  if [ $state = 'dead' ]; then
    end_state=1
    break
  elif  [ $state = 'completed' ]; then
    end_state=2
    break
  fi

  sleep $DI_TEST_WAIT_SECS
done

# --------------------------------------------------------
# Make sure to output the error in case execution failed
# --------------------------------------------------------

if [ $end_state -eq 1 ]; then
  echo $request | python -m json.tool
  >&2 echo "Error: Graph execution failed!"
  exit 1
elif [ $end_state -eq 2 ]; then
  echo "Graph execution succeeded!"
  exit 0
else
  echo $request | python -m json.tool
  >&2 echo "Error: Graph execution failed (timeout)!"
  exit 1
fi

