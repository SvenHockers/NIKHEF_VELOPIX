#!/usr/bin/env bash
set -e

# expect exactly one argument: the JSON config
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <config.json>"
  exit 1
fi
cfg="$1"

# unpack everything
tar xzf velopix.tar.gz

# create & activate venv
python3 -m venv env
source env/bin/activate
pip install velopix

# ensure output dir
mkdir -p velopix/output

# run only the passed config
python3 velopix/VeloPix_HyperParamHandler.py --config "$cfg"
mv history.jsonl velopix/output/result_$(basename "$cfg" .json).jsonl

# teardown
deactivate
