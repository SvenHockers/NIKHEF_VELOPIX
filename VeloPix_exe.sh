#!/usr/bin/env bash                    
set -e                                  

# Unpack all the files
tar xzf velopix.tar.gz
   
# build env 
python3 -m venv env
source env/bin/activate
pip install velopix

mkdir -p "velopix/output"
# run the Python analysis script
for cfg in velopix/configurations/*.json; do
    python3 velopix/VeloPix_HyperParamHandler.py --config "$cfg"
    mv velopix/result.json velopix/output/result_$(basename "$cfg")
done
# deactivate venv
deactivate                                
