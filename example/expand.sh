#!/bin/sh

# Expands the YAML to a valid JSON CloudFormation template in a
# temporary file. Returns the full path of the temporary file.

FILE=`mktemp -u -t cloudformation-XXXXXXXXXX.json`

ext=${1##*\.}
case "$ext" in
    py) python "cloudformation/$1" ${*:2} > "$FILE"
	;;
    yml) yaml2json "cloudformation/$1" | jq 'del(.Anchors)' > "$FILE"
	;;
esac
echo -ne "$FILE"
