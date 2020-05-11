#!/bin/bash
#
# //////////////////////////////////////////////////////////////////////////////
# Zipping of SAP Data Intelligence Pipeline Solutions
#
# This script zips files of a solution that are tracked in
# a Git project into a vsolution package.
#
# Note: Solutions tracked in Git by following the "Git Workflow" guide
# have a slightly different structure than the native solution structure.
# This script re-organizes the file structure in a temporary folder before
# zipping the files. See the "Git Workflow" guide for more information.
#
# //////////////////////////////////////////////////////////////////////////////

echo "---------------------"
echo "@@ Bundle Solution @@"
echo "---------------------"

if [ ! -f "manifest.json" ] || [ ! -d "vflow" ]; then
  echo "Error: Current path seems not to be a vsolution pipeline project (missing 'manifest.json' file or 'vflow' folder)"
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

# Zip folder in temp space and move back
tmp_dir=$(mktemp -d -t vsol-XXXXXXXXXX)
mkdir -p "$tmp_dir/content/files/"
cp -R vflow "$tmp_dir/content/files/"
cp manifest.json "$tmp_dir/"
pushd . > /dev/null
cd $tmp_dir && zip -r $PACKAGE_NAME content/ manifest.json
popd > /dev/null
mv $tmp_dir/$PACKAGE_NAME .
echo "Created package '$PACKAGE_NAME'"
